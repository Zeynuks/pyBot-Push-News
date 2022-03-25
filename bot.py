import telebot

TOKEN: ${{ secrets.TOKEN }}
bot = telebot.TeleBot(str(TOKEN))
basket = []
