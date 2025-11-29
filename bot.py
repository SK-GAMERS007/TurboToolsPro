from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import os
from downloader import download_audio
from converter import convert_to_pdf

TOKEN = "7953030889:AAG1BGzpqhnCDlrMWYdYN8PjbcqQzI6AN6k"

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎵 YouTube Audio Download", callback_data="yt_audio")],
        [InlineKeyboardButton("📄 File to PDF Convert", callback_data="file_pdf")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)

# Button Handler
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "yt_audio":
        await query.edit_message_text("Send me YouTube video link.")
        context.user_data["mode"] = "yt_audio"

    elif query.data == "file_pdf":
        await query.edit_message_text("Send any file (image/doc) to convert into PDF.")
        context.user_data["mode"] = "file_pdf"

# Message Handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get("mode")

    if mode == "yt_audio":
        link = update.message.text
        await update.message.reply_text("Downloading... wait 5–10 sec.")
        file_path = download_audio(link)
        await update.message.reply_document(open(file_path, "rb"))
        os.remove(file_path)

    elif mode == "file_pdf":
        file = await update.message.document.get_file()
        input_path = "input." + update.message.document.file_name.split(".")[-1]
        await file.download_to_drive(input_path)

        output = convert_to_pdf(input_path)
        await update.message.reply_document(open(output, "rb"))

        os.remove(input_path)
        os.remove(output)

def main():
    # ApplicationBuilder use karo
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers add karo
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))

    # Start bot
    app.run_polling()




