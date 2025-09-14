from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import yt_dlp  # ضفناها هنا

TOKEN = "8403565084:AAHFuSUe4oVNQDvTYxQ4g2Y0jqRoVLOk1o0"

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل لي رابط يوتيوب")

async def handle_link(update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['url'] = update.message.text
    keyboard = [
        [InlineKeyboardButton("MP4 720p", callback_data="mp4_720")],
        [InlineKeyboardButton("MP3 128kbps", callback_data="mp3_128")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("اختر الصيغة:", reply_markup=reply_markup)

# هنا بقى الدالة الجديدة بتاعتك بالكامل:
async def button(update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    url = context.user_data.get('url')
    fmt = query.data

    await query.edit_message_text(f"هيتم تحميل: {url}\nبصيغة: {fmt}")

    ydl_opts = {}
    if fmt == "mp4_720":
        ydl_opts = {"format": "best[ext=mp4][height<=720]", "outtmpl": "%(title)s.%(ext)s"}
    elif fmt == "mp3_128":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "%(title)s.%(ext)s",
            "postprocessors": [
                {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "128"},
            ],
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    await query.message.reply_document(open(filename, "rb"))

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()
