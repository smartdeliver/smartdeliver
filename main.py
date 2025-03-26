
import os
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

clients = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ברוך הבא לבוט שליחויות - smartdeliver! כתוב 'הוסף לקוח' כדי להתחיל.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "הוסף לקוח":
        await update.message.reply_text("אנא הזן את פרטי הלקוח בפורמט הבא:\nשם, כתובת, טלפון, דירה, קומה, קוד כניסה, הערות")
    elif "," in text:
        parts = text.split(",")
        if len(parts) >= 5:
            name = parts[0].strip()
            clients[name] = {
                "address": parts[1].strip(),
                "phone": parts[2].strip(),
                "apartment": parts[3].strip(),
                "floor": parts[4].strip(),
                "code": parts[5].strip() if len(parts) > 5 else "",
                "notes": parts[6].strip() if len(parts) > 6 else ""
            }
            await update.message.reply_text(f"הלקוח {name} נוסף למערכת.")
        else:
            await update.message.reply_text("פורמט לא תקין. נסה שוב.")
    else:
        await update.message.reply_text("לא זיהיתי את הפקודה. נסה שוב.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling()
