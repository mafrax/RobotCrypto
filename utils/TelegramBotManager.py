from telegram import Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from telegram.update import Update
import logging


class TelegramBotManager:
    def __init__(self, token: str):
        self.token = token
        self.bot = Bot(token=self.token)
        self.updater = Updater(token=self.token, use_context=True)
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

    def send_message(self, chat_id: str, message: str):
        self.bot.send_message(chat_id=chat_id, text=message)

    def start_listening(self, message_handler):
        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), message_handler))
        self.updater.start_polling()

    def stop_listening(self):
        self.updater.stop()
