import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import json
from io import BytesIO
from gzip import GzipFile
from botocore.exceptions import ClientError
from pandas.api.types import is_string_dtype
from pandas.api.types import is_object_dtype
from pandas.api.types import is_float_dtype
from pandas.api.types import is_integer_dtype

def load_s3_file(s3_res, s3_bucket_name, s3_key):

	# Download the data from S3
	s3_object = s3_res.Object(s3_bucket_name, s3_key)
	content_body = BytesIO()
	try:
		s3_object.download_fileobj(content_body)
	except ClientError as e:
		return e.response['Error']['Code'], e.response['Error']['Message']

	content_body.seek(0)
	# By default read file as GZIP - if this fails try reading normally
	try:
		# Try reading a line as gzipped data
		GzipFile(None, 'rb', fileobj=content_body).readline()
		content_body.seek(0)
		
		return '200', GzipFile(None, 'rb', fileobj=content_body)
	except:
		content_body.seek(0)
		
		return '200', content_body


def delete_s3_file(s3_res, s3_bucket_name, s3_key):

	s3_object = s3_res.Object(s3_bucket_name, s3_key)
	s3_object.delete()


def load_s3_file_in_parts(s3_res, s3_bucket_name, s3_key, n_lines):

	# Download the data from S3
	s3_object = s3_res.Object(s3_bucket_name, s3_key)
	body = s3_object.get()["Body"]

	lines = []

	for line in body.iter_lines(chunk_size=1024*100):
		line = line.decode('utf-8')
		lines.append(line)
		if len(lines) >= n_lines:
			yield lines
			lines = []
	yield lines


def load_s3_file_prepared(s3_res, s3_bucket_name, s3_key, input_format):
	
	s3_load_result = load_s3_file(s3_res, s3_bucket_name, s3_key)
	if s3_load_result[0] != '200':
		return s3_load_result
	else:
		b_io_buffer = s3_load_result[1]

	parsed_lines = []

	def prepare_json(b_io_buffer):

		lines = []        
		for line in b_io_buffer:
			lines.append(line)
		
		# test if there are any lines in the data
		if len(lines) == 0:
			raise Exception('data seems to be emtpy')

		# test the first 5 lines to verify that content is in an expected format
		# if only the first line is invalid, assume partial event
		try:
			for line in lines[:5]:
				json.loads(line)
		except ValueError as e:
			print(e, str(e))
			raise Exception('data is not in expected format')

		# do the actual parsing of the data		
		for line in lines:
			# line_num = lines.index(line)
			try:
				parsed_lines.append(json.loads(line))
			except ValueError as e:
				print('Not valid JSON. Skipping line.')
				# print('Line number {} in file {} from bucket {} is not valid json, and is skipped'.format(line_num, s3_key, s3_bucket_name))

		return parsed_lines
		
	# Select type
	if input_format == 'json':
		return prepare_json(b_io_buffer)
	if input_format == 'parquet':
		df = pd.read_parquet(b_io_buffer, engine='pyarrow')
		return df.to_dict(orient='records')
	else:
		return b_io_buffer
	

def convert_csv2json(csv_data):
	# TODO
	print('convert_csv2json not yet supported')
	return csv_data


def upload_buffer_to_s3(s3_res, s3_bucket_name, s3_key, b_io_buffer, gzip_it):
	
	if gzip_it:
		# temp buffer for gzipping
		upload_buffer = BytesIO()
		
		s3_object = s3_res.Object(s3_bucket_name, s3_key)
		with GzipFile(fileobj=upload_buffer, mode='wb') as gz:
			gz.write(b_io_buffer.read())
		upload_buffer.seek(0)
		# upload
		s3_object.upload_fileobj(
			upload_buffer,
			ExtraArgs={
				'ContentType':'text/plain',
				'ContentEncoding':'gzip'
			}
		)
	else:
		# upload
		b_io_buffer.seek(0)
		s3_object = s3_res.Object(s3_bucket_name, s3_key)
		s3_object.upload_fileobj(b_io_buffer)


def upload_data_to_s3(s3_res, s3_bucket_name, s3_key, data, gzip_it, output_format, **kwargs):
	
	def prepare_for_upload(data,  output_format):

		# Takes data in specified format and makes it into
		# BytesIO in the format specified.

		b_io_buffer = BytesIO()

		# json to json
		if output_format == 'json':
			for item in data:
				b_io_buffer.write("{item}\n".format(item=json.dumps(item, sort_keys=True)).encode())
			b_io_buffer.seek(0)
		# json to parquet
		elif output_format == 'parquet':
			df = pd.DataFrame(data)

			# columns = list(df.columns)
			df_columns = df.dtypes
			# If datatypes are specified: Apply them here and add to pyarrow-table
			# Else: Store everything as string and fill in empty strings for null-values
			if 'dt' in kwargs:
				for key, value in kwargs['dt'].items():
					if key in df_columns:
						try:
							if value == 'datetime':
								df[key] = pd.to_datetime(df[key])
							elif value == 'int64':
								df[key] = df[key].fillna(0).astype(value)
							elif value == 'float64':
								df[key] = df[key].fillna(0.0).astype(value)
							elif value == 'leave_alone':
								pass
							else:
								df[key] = df[key].astype(value)
						except Exception as ex:
							print('failed to set type', key, value)
							print(str(ex))
							pass
						else:
							df_columns = df_columns.drop(key)
			
			# default rest of data to string
			for key in df_columns.keys():
				print(key)
				if is_string_dtype(df[key]):
					print("string")
					df[key] = df[key].fillna("").astype(str)
				elif is_float_dtype(df[key]):
					print("float")
					df[key] = df[key].fillna(0).astype(int).astype(str).replace("0", "")
				elif is_integer_dtype(df[key]):
					print("integer")
					df[key] = df[key].fillna(0).astype(str).replace("0", "")
				elif is_object_dtype(df[key]):
					print("object")
					# df[key] = df[key].fillna("").astype(str)
					try:
						df[key] = df[key].fillna("").apply(json.dumps)
					except:
						df[key] = df[key].fillna("").astype(str)
				else:
					print("else")
					pass

			table = pa.Table.from_pandas(df)
			
			pq.write_table(table, b_io_buffer, coerce_timestamps='ms')
			b_io_buffer.seek(0)
		else:
			# Format not recoginzed, do nothing and return data as received
			return data

		return b_io_buffer
	
	b_io_buffer = prepare_for_upload(data, output_format)
	
	# remove (selected) exsisting line endings
	s3_key = s3_key.replace('.gz', '').replace('.parquet', '').replace('.json', '').replace('.xlsx', '').replace('.xls', '').replace('.csv', '')
	
	# append optinal part number
	if 'part_nr' in kwargs:
		s3_key = '{key}_part{part_nr}'.format(key=s3_key, part_nr=str(kwargs['part_nr']).zfill(3))

	# add new line endings
	if output_format == 'json' and not s3_key.endswith('.json'):
		s3_key = '{}.json'.format(s3_key)
	if output_format == 'parquet' and not s3_key.endswith('.parquet'):
		s3_key = '{}.parquet'.format(s3_key)
	if gzip_it and not s3_key.endswith('.gz'):
		s3_key = '{}.gz'.format(s3_key)
	
	# Upload the data as bytesIO, gzipped or not.
	# If output is 'parquet', skip gzipping
	if gzip_it and output_format != 'parquet':
		# temp buffer for gzipping
		upload_buffer = BytesIO()
		
		s3_object = s3_res.Object(s3_bucket_name, s3_key)
		with GzipFile(fileobj=upload_buffer, mode='wb') as gz:
			gz.write(b_io_buffer.read())
		upload_buffer.seek(0)
		# upload
		s3_object.upload_fileobj(
			upload_buffer,
			ExtraArgs={
				'ContentType':'text/plain',
				'ContentEncoding':'gzip'
			}
		)
	else:
		# upload
		s3_object = s3_res.Object(s3_bucket_name, s3_key)
		s3_object.upload_fileobj(b_io_buffer)