import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 7508949505

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет!\n"
        "Добро пожаловать в Gacha Realm!\n\n"
        "Я твой новый бот помощник 🤖"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start — запустить бота\n"
        "/help — помощь"
    )

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Сообщение от {user.full_name} (@{user.username})\n"
             f"ID: {user.id}\n\n"
             f"{text}\n\n"
             f"Чтобы ответить, напишите:\n"
             f"/reply {user.id} ваш_текст"
    )

    await update.message.reply_text("Ваше сообщение отправлено. Ожидайте ответа.")

async def reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("У вас нет прав для этой команды.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("Использование: /reply ID текст")
        return

    try:
        user_id = int(context.args[0])
        reply_text = " ".join(context.args[1:])
        await context.bot.send_message(chat_id=user_id, text=reply_text)
        await update.message.reply_text(f"Ответ отправлен пользователю {user_id}.")
    except ValueError:
        await update.message.reply_text("ID должен быть числом.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("reply", reply_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))

    application.run_polling()

if __name__ == '__main__':
    main()
