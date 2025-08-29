from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Load token from Railway environment variable

def start(update, context):
    update.message.reply_text("👋 Hello! Your Railway bot is alive.")

def help_command(update, context):
    update.message.reply_text("Here are my commands:\n/start - Welcome\n/help - Show this message")

def echo(update, context):
    update.message.reply_text(update.message.text)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()