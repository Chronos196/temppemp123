import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials

bot = telebot.TeleBot("6368057963:AAFVQ4SY6OUzppYfybn3Oa1dGLJO1L9kIwE")
bot.parse_mode = 'html'

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
client = gspread.authorize(creds)

spreadsheet_id = '12HhozXFxPVSXS5I5qY_5BqQxH12smpjXNsS0OhIqvlg'

CONTENT_TYPES = ["text", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                 "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                 "migrate_from_chat_id", "pinned_message"]

ADMIN_ID = 1024373582