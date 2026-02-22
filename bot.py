import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = update.message
    user_id = message.from_user.id

    # 🔹 Agar ADMIN reply qilayotgan bo‘lsa
    if user_id == ADMIN_ID and message.reply_to_message:
        original_user = message.reply_to_message.forward_from
        if original_user:
            await context.bot.send_message(
                chat_id=original_user.id,
                text=message.text
            )
        return

    # 🔹 Agar oddiy user yozgan bo‘lsa
    if user_id != ADMIN_ID:
        await context.bot.forward_message(
            chat_id=ADMIN_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )

        await message.reply_text("Xabaringiz qabul qilindi 🤍")


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
