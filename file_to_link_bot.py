import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("Please set BOT_TOKEN in your .env file")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! Send me any file (photo, video, document, etc.) and I'll give you a direct download link!"
    )

async def get_file_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    file = None

    # Detect file type
    if message.document:
        file = message.document
    elif message.photo:
        file = message.photo[-1]  # last = highest resolution
    elif message.video:
        file = message.video
    elif message.audio:
        file = message.audio
    elif message.voice:
        file = message.voice
    else:
        await message.reply_text("Please send a valid file 📁")
        return

    # Get file info
    file_obj = await file.get_file()
    file_path = file_obj.file_path
    download_link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

    # Reply with link
    await message.reply_text(
        f"✅ File received!\n\n📎 File name: `{getattr(file, 'file_name', 'N/A')}`\n"
        f"🔗 Direct download link:\n{download_link}\n\n⚠️ Keep this link private; "
        f"anyone with it can access your file.",
        parse_mode="Markdown"
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(
        filters.Document.ALL | filters.Video.ALL | filters.Audio.ALL |
        filters.Photo.ALL | filters.Voice.ALL, get_file_link))

    print("🤖 File-to-Link Bot is running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
