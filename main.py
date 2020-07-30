import os
from datetime import datetime
from dotenv import load_dotenv
import boto3


date = datetime.today().isoformat(sep='_')

load_dotenv()

DB_NAME = os.environ.get('DB_NAME')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT', 3306)
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
AWS_SECRET_ENDPOINT_URL = os.environ.get('AWS_SECRET_ENDPOINT_URL')
AWS_BUCKET = os.environ.get('AWS_BUCKET')

dir_name = "./backups/"
file_name = f"{DB_NAME}_{date}.sql"

result = os.system(f"mysqldump -h {DB_HOST} -P {DB_PORT} -u{DB_USER} -p{DB_PASSWORD} --opt {DB_NAME} > {dir_name}{file_name}")

if os.path.exists(f"{dir_name}{file_name}"):
    session = boto3.session.Session()

    s3 = session.client(
        service_name='s3',
        endpoint_url=AWS_SECRET_ENDPOINT_URL
    )

    s3.upload_file(f"{dir_name}{file_name}", AWS_BUCKET, file_name)
