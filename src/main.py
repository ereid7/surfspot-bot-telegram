from telegram.ext import Updater, CommandHandler
import logging
from telegram import ParseMode
from bs4 import BeautifulSoup
from handlers import surf
import requests
import re


def main():
  updater = Updater(token='TOKEN')
  dp = updater.dispatcher
  logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

  dp.add_handler(CommandHandler('surf', surf, pass_args=True))
  updater.start_polling()
  updater.idle()

if __name__ == '__main__':
  main()