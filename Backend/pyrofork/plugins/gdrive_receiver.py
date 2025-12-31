from asyncio import create_task, Queue, Lock
from pyrogram import filters, Client
from pyrogram.types import Message
from Backend import db
from Backend.config import Telegram
from Backend.logger import LOGGER
from Backend.helper.gdrive import gdrive_client
from Backend.helper.metadata import metadata
from Backend.helper.pyro import get_readable_file_size

gdrive_queue = Queue()
db_lock = Lock()

async def process_gdrive_link():
    while True:
        data = await gdrive_queue.get()
        # data: (metadata_info, file_info)
        async with db_lock:
            updated_id = await db.insert_media(
                data[0], 
                source_data=data[1], 
                source_type="gdrive"
            )
            if updated_id:
                LOGGER.info(f"[GDrive] Processed: {data[1]['name']}")
            else:
                LOGGER.warning(f"[GDrive] Failed to insert: {data[1]['name']}")
        gdrive_queue.task_done()

create_task(process_gdrive_link())

@Client.on_message(filters.channel & filters.text & filters.regex(r"drive\.google\.com"))
async def gdrive_handler(client: Client, message: Message):
    if str(message.chat.id) in Telegram.AUTH_CHANNEL:
        url = message.text.strip()
        file_id = gdrive_client.get_file_id(url)
        
        if not file_id:
            return

        file_meta = await gdrive_client.get_file_metadata(file_id)
        if not file_meta:
            await message.reply_text("❌ Could not fetch metadata. Check permissions.")
            return

        # --- FOLDER HANDLING ---
        if file_meta.get('mimeType') == 'application/vnd.google-apps.folder':
            status_msg = await message.reply_text("📂 <b>Folder Detected!</b> Scanning for videos...", quote=True)
            files = await gdrive_client.get_files_in_folder(file_id)
            
            if not files:
                await status_msg.edit_text("❌ No video files found in this folder.")
                return

            count = 0
            for file in files:
                name = file.get('name')
                size = get_readable_file_size(int(file.get('size', 0)))
                id_data = {"gdrive_id": file.get('id')}
                
                # We assume file is a video because get_files_in_folder filters by 'video/'
                metadata_info = await metadata(name, id_data, is_gdrive=True)
                
                if metadata_info:
                    await gdrive_queue.put((metadata_info, {"name": name, "size": size}))
                    count += 1
            
            await status_msg.edit_text(f"✅ <b>Folder Processed!</b>\nQueued {count} video files.")
            return

        # --- SINGLE FILE HANDLING ---
        name = file_meta.get('name')
        size = get_readable_file_size(int(file_meta.get('size', 0)))
        
        id_data = {"gdrive_id": file_id}
        
        metadata_info = await metadata(name, id_data, is_gdrive=True)
        
        if metadata_info:
            await message.reply_text(f"✅ <b>G-Drive Detected:</b>\n{name}", quote=True)
            await gdrive_queue.put((metadata_info, {"name": name, "size": size}))
        else:
            await message.reply_text("❌ Could not parse metadata from filename.")
