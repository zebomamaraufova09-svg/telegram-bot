import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await context.bot.forward_message(
            chat_id=ADMIN_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )
        await update.message.reply_text("Xabaringiz qabul qilindi 🤍")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))

app.run_polling()
