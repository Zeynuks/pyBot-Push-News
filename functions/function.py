import requests
import re

from bs4 import BeautifulSoup
from telebot import types
from random import randint
from bot import bot, basket
from keyboards.keyboard import *

def parsing_output(message, parsing_text, number, url):
    soup = BeautifulSoup(parsing_text.text, 'lxml')
    string_1 = soup.find('head')
    string_2 = string_1.find('meta', property="og:description")
    article_text = string_2.get('content')
    bot.send_message(message.chat.id,f'{article_text}\n\n<a href="{url}">Источник</a>', parse_mode='HTML', reply_markup = article_keyboard(url)) 
    bot.edit_message_text(chat_id=message.chat.id, text = f'Пожалуйста, подождите: {number + 1}/5'.format(message.text), message_id=message.message_id + 1)

def channel_parsing(message, parsing_text, number, url):
    soup = BeautifulSoup(parsing_text.text, 'lxml')
    string_1 = soup.find('head')
    string_2 = string_1.find('meta', property="og:description")
    article_text = string_2.get('content')
    keyboard = types.InlineKeyboardMarkup()
    open_article = types.InlineKeyboardButton(text = 'Открыть', url = url)
    keyboard.add(open_article)
    bot.send_message(message.chat.id,f'{article_text}\n\n<a href="{url}">Источник</a>', parse_mode='HTML', reply_markup = keyboard) 
    bot.edit_message_text(chat_id=message.chat.id, text = f'Пожалуйста, подождите: {number + 1}/5'.format(message.text), message_id=message.message_id + 1)

def article_parsing(message, channels_url):
    for i in range(5):
        def article_generator():
            try:
                article = None
                while article == None:
                    page = requests.get(channels_url[i])
                    soup = BeautifulSoup(page.text, 'lxml')
                    string_1 = soup.find_all('div', class_='tgme_widget_message_wrap js-widget_message_wrap')[-1]
                    string_2 = string_1.find('div', class_='tgme_widget_message js-widget_message')
                    end = string_2.get('data-post')
                    last_article = end.split('/')
                    rand_article = randint(1, int(last_article[1]))  
                    split = channels_url[i].split('s/', 1)
                    article_url = split[0] + split[1] + str(rand_article)
                    requests_to_article = requests.get(article_url)
                    article = re.search('checkActionsPosition()', requests_to_article.text)
                parsing_output(message, requests_to_article, i, article_url)
            except AttributeError:
                article_generator()
            except IndexError:
                article_generator()
        article_generator()

def legendary_potatoes(message, max_article, page_numbers, mayak):
    if mayak == 1:
        bot.edit_message_text(chat_id=message.chat.id, text='Пожалуйста, подождите ⏰', message_id=message.message_id+1)
    else:
        bot.edit_message_text(chat_id=message.chat.id, text='Пожалуйста, подождите ⏰', message_id=message.message_id)
    max_str = str((len(basket) + 5 - len(basket) % 5) // 5)
    spis = types.InlineKeyboardMarkup()
    if page_numbers > len(basket):
        page_numbers = len(basket)
    for j in range(max_article, page_numbers):
        page = requests.get(basket[j])
        soup = BeautifulSoup(page.text, 'lxml')
        string_1 = soup.find('head')
        string_2 = string_1.find('meta', property="og:title")
        name = string_2.get('content')
        element = types.InlineKeyboardButton(text = name, callback_data = f'liked element {basket[j]}')
        spis.add(element)
    if not(page_numbers % 5 == 0):
        mnoj = str((page_numbers + 5 - page_numbers % 5) // 5)
    else:
        mnoj = str(page_numbers // 5)
    element1 = types.InlineKeyboardButton(text = '<-', callback_data = f'liked turn left {mnoj}')
    element3 = types.InlineKeyboardButton(text = f'{mnoj}/{max_str}', callback_data = 'liked menu')
    element2 = types.InlineKeyboardButton(text = '->', callback_data = f'liked turn right {mnoj}')
    spis.add(element1, element3, element2)
    if mayak == 1:
        bot.edit_message_text(chat_id=message.chat.id, text='Понравившееся: ', message_id=message.message_id+1, reply_markup = spis)
    else:
        bot.edit_message_text(chat_id=message.chat.id, text='Понравившееся: ', message_id=message.message_id, reply_markup = spis)
