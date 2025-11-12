import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set in Render Environment Variables")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! Send me any file and I will give you a direct download link."
    )


# Handle all file uploads
async def get_file_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    file = None

    # Detect file type
    if message.document:
        file = message.document
    elif message.photo:
        file = message.photo[-1]
    elif message.video:
        file = message.video
    elif message.audio:
        file = message.audio
    elif message.voice:
        file = message.voice
    else:
        await message.reply_text("Please send a valid file 📁")
        return

    # Get file object
    file_obj = await file.get_file()
    file_path = file_obj.file_path

    # Create download link
    download_link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

    # Reply to user
    await message.reply_text(
        f"✅ File received!\n\n"
        f"🔗 Download link:\n{download_link}\n\n"
        f"⚠️ Keep this link private."
    )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # FILE FILTERS — compatible with Render version
    app.add_handler(MessageHandler(
        filters.Document.ALL |
        filters.VIDEO |
        filters.AUDIO |
        filters.PHOTO |
        filters.VOICE,
        get_file_link
    ))

    print("🚀 Bot is running on Render ...")
    app.run_polling()


if __name__ == "__main__":
    main()
