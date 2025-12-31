import re
import asyncio
from google.oauth2 import service_account
from googleapiclient.discovery import build
from Backend.config import Telegram
from Backend.logger import LOGGER

class GDrive:
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/drive.readonly']
        self.creds = None
        self.service = None
        try:
            self.creds = service_account.Credentials.from_service_account_file(
                Telegram.GDRIVE_SECRET, scopes=self.scopes
            )
            self.service = build('drive', 'v3', credentials=self.creds)
        except Exception as e:
            LOGGER.error(f"GDrive Auth Error: {e}")

    def get_file_id(self, url: str):
        patterns = [
            r'/file/d/([a-zA-Z0-9_-]+)',
            r'id=([a-zA-Z0-9_-]+)',
            r'open\?id=([a-zA-Z0-9_-]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    async def get_file_metadata(self, file_id: str):
        loop = asyncio.get_running_loop()
        try:
            file = await loop.run_in_executor(
                None, 
                lambda: self.service.files().get(
                    fileId=file_id, 
                    fields="id, name, size, mimeType"
                ).execute()
            )
            return file
        except Exception as e:
            LOGGER.error(f"GDrive Metadata Error: {e}")
            return None

gdrive_client = GDrive()