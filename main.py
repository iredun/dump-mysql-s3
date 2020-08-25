import os
import requests
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

SERVER_NAME = os.environ.get('SERVER_NAME')

AWS_SECRET_ENDPOINT_URL = os.environ.get('AWS_SECRET_ENDPOINT_URL')
AWS_BUCKET = os.environ.get('AWS_BUCKET')

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_USER_NOTIFY = os.environ.get('TELEGRAM_USER_NOTIFY').split(',')


def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    pre_text = "*Server*: `" + SERVER_NAME + '`\n*Error message:* '

    for chat_id in TELEGRAM_USER_NOTIFY:
        payload = {
            "chat_id": chat_id,
            "parse_mode": "MarkdownV2",
            "text": pre_text + '```\n' + text + '\n```'
        }
        requests.post(url, json=payload)


try:
    dir_name = os.path.dirname(os.path.abspath(__file__)) + "/backups/"
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    file_name = f"{DB_NAME}_{date}.sql"

    result = os.system(
        f"mysqldump -h {DB_HOST} -P {DB_PORT} -u{DB_USER} -p{DB_PASSWORD} --opt {DB_NAME} > {dir_name}{file_name}")

    if os.path.exists(f"{dir_name}{file_name}"):
        session = boto3.session.Session()

        s3 = session.client(
            service_name='s3',
            endpoint_url=AWS_SECRET_ENDPOINT_URL
        )

        s3.upload_file(f"{dir_name}{file_name}", AWS_BUCKET, file_name)

        os.remove(f"{dir_name}{file_name}")
except Exception as e:
    if TELEGRAM_BOT_TOKEN:
        send_telegram(str(e))
