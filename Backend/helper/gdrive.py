import re
import asyncio
from google.oauth2 import service_account
from google.auth.transport.requests import Request
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

    def get_access_token(self):
        """Refreshes and returns the access token."""
        if not self.creds:
            return None
        if not self.creds.valid:
            try:
                self.creds.refresh(Request())
            except Exception as e:
                LOGGER.error(f"Token Refresh Failed: {e}")
                return None
        return self.creds.token

    def get_file_id(self, url: str):
        patterns = [
            r'/file/d/([a-zA-Z0-9_-]+)',
            r'/folders/([a-zA-Z0-9_-]+)',  # Added folder regex support
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
                    fields="id, name, size, mimeType",
                    supportsAllDrives=True  # Support Shared Drives
                ).execute()
            )
            return file
        except Exception as e:
            LOGGER.error(f"GDrive Metadata Error: {e}")
            return None

    async def get_files_in_folder(self, folder_id: str):
        """Recursively fetches video files from a folder."""
        loop = asyncio.get_running_loop()
        
        def _list_files():
            files = []
            page_token = None
            # Query: Not a folder, not trashed, contains 'video' in mimeType
            query = f"'{folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder' and trashed = false and mimeType contains 'video/'"
            
            while True:
                response = self.service.files().list(
                    q=query,
                    fields="nextPageToken, files(id, name, size, mimeType)",
                    pageToken=page_token,
                    includeItemsFromAllDrives=True,
                    supportsAllDrives=True
                ).execute()
                
                files.extend(response.get('files', []))
                page_token = response.get('nextPageToken')
                if not page_token:
                    break
            return files

        try:
            return await loop.run_in_executor(None, _list_files)
        except Exception as e:
            LOGGER.error(f"GDrive Folder Error: {e}")
            return []

gdrive_client = GDrive()
