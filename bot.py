import os
from telegram.ext import Updater, MessageHandler, Filters
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

TOKEN = os.getenv("BOT_TOKEN")
SERVICE_ACCOUNT_FILE = "service_account.json"

creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/drive"]
)

drive_service = build("drive", "v3", credentials=creds)

def upload_to_drive(file_path, filename):
    file_metadata = {"name": filename}
    media = open(file_path, "rb")

    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media
    ).execute()
    
    return uploaded_file.get("id")

def handle_file(update, context):
    tg_file = update.message.document or update.message.video
    file_id = tg_file.file_id
    file_name = tg_file.file_name

    file_obj = context.bot.getFile(file_id)
    file_obj.download(file_name)

    drive_id = upload_to_drive(file_name, file_name)

    update.message.reply_text(f"فایل با موفقیت آپلود شد!\nGoogle Drive ID: {drive_id}")

updater = Updater(TOKEN)
dp = updater.dispatcher

dp.add_handler(MessageHandler(Filters.document | Filters.video, handle_file))

updater.start_polling()
updater.idle()
