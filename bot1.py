# -*- coding: utf-8 -*-
import telebot
import random
from telebot import types
from bs4 import BeautifulSoup
import requests
import urllib.parse
import re
import os, time

TOKEN = '1816922959:AAEZ84tdBD4TeCN6yRox4lJzeS9qTtnbLbI'
bot = telebot.TeleBot(TOKEN)
likes = []
basket = []

@bot.message_handler(commands = ['start'])
def firstmessage(message):
    mark = types.ReplyKeyboardMarkup(resize_keyboard = True)
    go_button = types.KeyboardButton(text = '📰 Запустить ленту')
    catalog_button = types.KeyboardButton(text = '🔝 Топ 5 каналов')
    interesting_button = types.KeyboardButton(text = '🍉 Выбрать категорию')
    new_post = types.KeyboardButton(text = '🆕 Новые статьи')
    basket = types.KeyboardButton(text = '❤️ Понравившееся')
    mark.row(go_button, catalog_button).row(interesting_button, new_post).add(basket)
    bot.send_message(message.chat.id, "Выберите нужное действие на панели снизу 👇: \n\n📰 Запустить ленту - показ 5 любых статей с разных каналов, без ограниения по темам \n\n🔝 Топ 5 каналов - показ 5 телеграм-каналов без ограничения по темам (важно понимать, что 'топ' в данном случае не означает рейтинг среди множества каналов, а подразумевает список случайно выбранных) \n\n🍉 Выбрать категорию - возможность выбрать интерсующую вас тематику публикаций \n\n🆕 Новые статьи - показ новых публикаций случайных каналов \n\n❤️ Понравившееся - бибилиотека понравившихся вам статей", reply_markup = mark)

@bot.message_handler(content_types = ['text'])
def answer(message):
    if message.text == '📰 Запустить ленту':
        list_book = ['https://t.me/s/history_0o/', 'https://t.me/s/National_Geograph1c/', 'https://t.me/s/slifcloud/',
        'https://t.me/s/TriviaGames/', 'https://t.me/s/PopularNauka/']
        #file = open('channels.txt', 'r')
        true_list_book = []
        bot.send_message(message.chat.id, 'Пожалуйста, подождите: 0/5')
        global likes
        likes = []
        for i in 1, 2, 3, 4, 5:
            new_book = random.choice(list_book)
            list_book.remove(new_book)
            true_list_book.append(new_book)
        for j in 0, 1, 2, 3,:
            url = true_list_book[j]
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "lxml")
            string_1 = soup.find_all('div', class_='tgme_widget_message_wrap js-widget_message_wrap')[-1]
            string_2 = string_1.find('div', class_='tgme_widget_message js-widget_message')
            end = string_2.get('data-post')
            ster = end.split('/')
            def five_articles(): 
                max_book = random.randint(1, int(ster[1]))
                split = true_list_book[j].split('s/', 1)
                true_book = split[0] + split[1] + str(max_book)
                r = requests.get(true_book)
                cumpot = re.search('checkActionsPosition()', r.text)
                if cumpot == None:
                    return five_articles()
                else:
                    global likes
                    likes.append(true_book)
                    complete = types.InlineKeyboardMarkup()
                    open_book = types.InlineKeyboardButton(text = 'Открыть статью', url = true_book)
                    like = types.InlineKeyboardButton(text = 'Понравилось ❤️', callback_data = 'like' + str(j))
                    complete.add(open_book, like)
                    bot.send_message(message.chat.id, '\n\nСсылка на статью: ' + true_book + 
                        '\n\nСсылка на канал: ' + split[0] + split[1],  reply_markup = complete)
                    bot.edit_message_text(chat_id=message.chat.id, text = "Пожалуйста, подождите: " + str(j+1) + "/5".format(message.text), message_id=message.message_id + 1)
                    if j+1 == 5:
                        bot.edit_message_text(chat_id=message.chat.id, text = "Пожалуйста, подождите: 5/5 ✅".format(message.text), message_id=message.message_id + 1)
            five_articles()
    elif message.text == '🔝 Топ 5 каналов':
        list_channel = ['Итсория - https://t.me/history_0o', 'National Geographic - https://t.me/National_Geograph1c', 
        'Вселенная приложений - https://t.me/vseapps', 'Мозговой штурм - загадки и викторины - https://t.me/TriviaGames', 
        'КотОблако - https://t.me/slifcloud']
        true_list_channel = []
        for i in 1,2,3,4,5:
            new_channel = random.choice(list_channel)
            list_channel.remove(new_channel)
            true_list_channel.append(new_channel)
        for element in true_list_channel:
            bot.send_message(message.chat.id, element)
    elif message.text == '🍉 Выбрать категорию':
        category = types.InlineKeyboardMarkup()
        history_post = types.InlineKeyboardButton(text = '👨‍🎨 История', callback_data = 'history')
        geography_post = types.InlineKeyboardButton(text = '🌎 География', callback_data = 'geography')
        cracker_post = types.InlineKeyboardButton(text = '🍪 Полезное', callback_data = 'cracker')
        poll_post = types.InlineKeyboardButton(text = '🎱 Викторины', callback_data = 'poll')
        category.row(history_post, geography_post).add(cracker_post, poll_post)
        bot.send_message(message.chat.id, '🍒 Выберите категорию', reply_markup = category)
    elif message.text == '🆕 Новые статьи':
        list_book = ['https://t.me/s/history_0o/', 'https://t.me/s/National_Geograph1c/', 'https://t.me/s/vseapps/',
        'https://t.me/s/TriviaGames/', 'https://t.me/s/slifcloud/', 'https://t.me/s/PopularNauka/']
        true_list_book = []
        bot.send_message(message.chat.id, 'Пожалуйста, подождите: 0/5')
        for i in 1, 2, 3, 4, 5:
            new_book = random.choice(list_book)
            list_book.remove(new_book)
            true_list_book.append(new_book)
        for j in 0, 1, 2, 3, 4:
            url = true_list_book[j]
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "lxml")
            string_1 = soup.find_all('div', class_='tgme_widget_message_wrap js-widget_message_wrap')[-1]
            string_2 = string_1.find('div', class_='tgme_widget_message js-widget_message')
            end = string_2.get('data-post')
            try:
                complete = types.InlineKeyboardMarkup()
                open_book = types.InlineKeyboardButton(text = 'Открыть статью', url = 'https://t.me/' + end)
                complete.add(open_book)
                bot.send_message(message.chat.id, '\n\nСсылка на статью: https://t.me/' + end + 
                    '\n\nСсылка на канал: ' + true_list_book[j],  reply_markup = complete)
                bot.edit_message_text(chat_id=message.chat.id, text = "Пожалуйста, подождите: " + str(j+1) + "/5".format(message.text), message_id=message.message_id + 1)
                if j+1 == 5:
                    bot.edit_message_text(chat_id=message.chat.id, text = "Пожалуйста, подождите: 5/5 ✅".format(message.text), message_id=message.message_id + 1)
            except UnicodeEncodeError:
                return five_articles()
    elif message.text == '❤️ Понравившееся':
        forward = '❤️ Понравившееся:\n'
        if len(basket) == 0:
            bot.send_message(message.chat.id, 'У вас нет понравившихся статей')
        else:
            for i in range(len(basket)):
                forward = forward + str(i + 1) + '. ' + str(basket[i]) + '\n'
            bot.send_message(message.chat.id, str(forward))

@bot.callback_query_handler(func = lambda call: True)
def call_answer(call):
    def selection_articles(list_book):
        true_list_book = []
        for i in 1, 2, 3, 4, 5:
            new_book = random.choice(list_book)
            true_list_book.append(new_book)
        for j in 0, 1, 2, 3, 4:
            url = true_list_book[j]
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "lxml")
            string_1 = soup.find_all('div', class_='tgme_widget_message_wrap js-widget_message_wrap')[-1]
            string_2 = string_1.find('div', class_='tgme_widget_message js-widget_message')
            end = string_2.get('data-post')
            ster = end.split('/')
            def five_articles(): 
                max_book = random.randint(1, int(ster[1]))
                split = true_list_book[j].split('s/', 1)
                true_book = split[0] + split[1] + str(max_book)
                r = requests.get(true_book)
                cumpot = re.search('checkActionsPosition()', r.text)
                if cumpot == None:
                    return five_articles()
                else:
                    complete = types.InlineKeyboardMarkup()
                    open_book = types.InlineKeyboardButton(text = 'Открыть статью', url = true_book)
                    complete.add(open_book)
                    bot.send_message(call.message.chat.id, '\n\nСсылка на статью: ' + true_book + 
                        '\n\nСсылка на канал: ' + split[0] + split[1],  reply_markup = complete)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Пожалуйста, подождите: " + str(j+1) + "/5")
                    if j+1 == 5:
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Пожалуйста, подождите: 5/5 ✅")
            five_articles()
    if call.data == 'history':
        list_book = ['https://t.me/s/history_0o/']
        selection_articles(list_book)
    elif call.data == 'geography':
        list_book = ['https://t.me/s/National_Geograph1c/']
        true_list_book = []
        selection_articles(list_book)
    elif call.data == 'cracker':
        list_book = ['https://t.me/s/vseapps/', 'https://t.me/s/slifcloud/']
        selection_articles(list_book)
    elif call.data == 'poll':
        list_book = ['https://t.me/s/TriviaGames/']
        selection_articles(list_book)
    elif call.data == 'like0':
        basket.append(likes[0])
        bot.answer_callback_query(callback_query_id=call.id, text='Добавлено')
    elif call.data == 'like1':
        basket.append(likes[1])
        bot.answer_callback_query(callback_query_id=call.id, text='Добавлено')
    elif call.data == 'like2':
        basket.append(likes[2])
        bot.answer_callback_query(callback_query_id=call.id, text='Добавлено')
    elif call.data == 'like3':
        basket.append(likes[3])
        bot.answer_callback_query(callback_query_id=call.id, text='Добавлено')
    elif call.data == 'like4':
        basket.append(likes[4])
        bot.answer_callback_query(callback_query_id=call.id, text='Добавлено')

bot.polling(none_stop = True)
