import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# userlarni vaqtincha saqlaymiz
user_messages = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user_id = message.from_user.id

    # AGAR ADMIN REPLY QILSA
    if user_id == ADMIN_ID and message.reply_to_message:
        replied_msg_id = message.reply_to_message.message_id

        if replied_msg_id in user_messages:
            target_user_id = user_messages[replied_msg_id]

            await context.bot.send_message(
                chat_id=target_user_id,
                text=message.text
            )
        return

    # AGAR ODDIY USER YOZSA
    if user_id != ADMIN_ID:
        forwarded = await context.bot.forward_message(
            chat_id=ADMIN_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )

        # forward qilingan xabar ID sini saqlaymiz
        user_messages[forwarded.message_id] = user_id

        await message.reply_text("Xabaringiz qabul qilindi 🤍")


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
