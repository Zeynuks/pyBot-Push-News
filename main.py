# -*- coding: utf-8 -*-
from random import choice, sample
from telebot import types

from bot import bot, basket
from channels import available_channels_url
from functions.function import *
from keyboards.keyboard import *

@bot.message_handler(commands = ['start'])
def start_handler(message):
    bot.send_message(message.chat.id, 'Выберите нужное действие на панели снизу 👇:\
        \n\n📰 <b>Лента</b> - показ пяти любых статей с разных каналов, без ограниения по темам\
        \n\n🔝 <b>Каналы</b> - показ пяти телеграм-каналов без ограничения по темам\
        \n\n🍉 <b>Категории</b> - возможность выбрать интерсующую вас тематику публикаций\
        \n\n🆕 <b>Новые статьи</b> - показ новых публикаций случайных каналов\
        \n\n❤️ <b>Понравившееся</b> - бибилиотека понравившихся вам статей',
    parse_mode='HTML', reply_markup = keyboard_menu())

@bot.message_handler(content_types = ['text'])
def main_handler(message):
    if message.text == '📰 Лента':
        bot.send_message(message.chat.id, 'Выберите нужное действие', reply_markup = sub_keyboard_menu())
    elif message.text == '🔝 Каналы':
        bot.send_message(message.chat.id, 'Пожалуйста, подождите: 0/5')
        channels_url = sample(available_channels_url, 5)
        for i in range(len(channels_url)):
            url = channels_url[i]
            page = requests.get(url)
            url = channels_url[i].split('/s')[0] + channels_url[i].split('/s')[1]
            channel_parsing(message, page, i, url)
    elif message.text == '🍉 Категории':
        bot.send_message(message.chat.id, '🍒 Выберите категорию', reply_markup = category_keyboard())
    elif message.text == '❤️ Понравившееся':
        global basket
        if len(basket) == 0:
            bot.send_message(message.chat.id, 'У вас нет понравившихся статей')
        else:
            bot.send_message(message.chat.id, '❤️')
            legendary_potatoes(message, 0, 5, 1)
    else:
        sub_handler(message)

def sub_handler(message):
    if message.text == '🎲 5 случайных':
        channels_url = sample(available_channels_url, 5)
        bot.send_message(message.chat.id, 'Пожалуйста, подождите: 0/5')
        article_parsing(message, channels_url)
    elif message.text == '🆕 Новые статьи':
        bot.send_message(message.chat.id, 'Пожалуйста, подождите: 0/5')
        for i in 0, 1, 2, 3, 4:
            try:
                def process():
                    url = choice(available_channels_url)
                    page = requests.get(url)
                    soup = BeautifulSoup(page.text, 'lxml')
                    string_1 = soup.find_all('div', class_='tgme_widget_message_wrap js-widget_message_wrap')[-1]
                    string_2 = string_1.find('div', class_='tgme_widget_message js-widget_message')
                    end = string_2.get('data-post')
                    article_linc = 'https://t.me/' + end
                    request_to_article_linc = requests.get(article_linc)
                    parsing_output(message, request_to_article_linc, i, article_linc)
                process()
            except AttributeError:
                process()
            except IndexError:
                process()
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Выполнено', reply_markup = keyboard_menu())

@bot.callback_query_handler(func = lambda call: True)
def callback_handler(call):
    global basket
    check = call.data.split()
    if check[0] == 'like':
        basket.append(check[1])
        bot.answer_callback_query(callback_query_id=call.id, text='Добавлено')
        keyboard = types.InlineKeyboardMarkup()
        open_book = types.InlineKeyboardButton(text = 'Открыть', url = check[1])
        like = types.InlineKeyboardButton(text = '❤️', callback_data = f'liked delete {check[1]}')
        keyboard.add(open_book, like)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
        #basket = list(set(basket))
    elif check[0] == 'category':
        if check[1] == 'history':
            list_book = ['https://t.me/s/history_0o/']*5
        elif check[1] == 'geography':
            list_book = ['https://t.me/s/National_Geograph1c/']*5
        elif check[1] == 'cracker':
            list_book = ['https://t.me/s/vseapps/']*5
        elif check[1] == 'poll':
            list_book = ['https://t.me/s/TriviaGames/']*5
        bot.answer_callback_query(callback_query_id=call.id, text='Производится подбор')
        bot.send_message(call.message.chat.id, 'Пожалуйста, подождите: 0/5')
        article_parsing(call.message, list_book)
    elif check[0] == 'liked':
        liked_page(call, check)

def liked_page(call, check):
    if check[1] == 'element':
        page = requests.get(check[2])
        soup = BeautifulSoup(page.text, 'lxml')
        string_1 = soup.find('head')
        string_2 = string_1.find('meta', property="og:description")
        article_text = string_2.get('content')
        keyboard = types.InlineKeyboardMarkup()
        open_book = types.InlineKeyboardButton(text = 'Открыть', url = check[2])
        like = types.InlineKeyboardButton(text = '❤️', callback_data = f'liked delete {check[2]}')
        keyboard.add(open_book, like)
        bot.answer_callback_query(callback_query_id=call.id)
        bot.edit_message_text(chat_id=call.message.chat.id, text=f'{article_text}\n\n<a href="{check[2]}">Источник</a>',
        parse_mode='HTML',message_id=call.message.message_id, reply_markup= keyboard)
    elif check[1] == 'delete':
        basket.remove(check[2])
        bot.answer_callback_query(callback_query_id=call.id, text='Удалено 🗑')
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup= article_keyboard(check[2]))
    elif check[1] == 'turn':
        bot.answer_callback_query(callback_query_id=call.id)
        if check[2] == 'right':
            maximum = (int(check[3])+1)*5
            minimum = int(check[3])*5
            if maximum > len(basket) + 5 - len(basket) % 5:
                maximum = int(check[3])*5
                minimum = (int(check[3])-1)*5
            legendary_potatoes(call.message, minimum, maximum, 0)
        elif check[2] == 'left':
            minimum = (int(check[3])-2)*5
            if minimum < 0:
                minimum = 0
                maximum = 5
            else:
                maximum = (int(check[3])-1)*5
            legendary_potatoes(call.message, minimum, maximum, 0)
    elif check[1] == 'menu':
        spis = types.InlineKeyboardMarkup()
        for stran in range((len(basket) + 5 - len(basket) % 5) // 5):
            spis.add(types.InlineKeyboardButton(text = f'{stran + 1}', callback_data = f'liked spis {stran + 1}'))
        bot.edit_message_text(chat_id=call.message.chat.id, text='Выберите страницу:  ', message_id=call.message.message_id, reply_markup = spis)
    elif check[1] == 'spis':
        minimum = (int(check[2])-1)*5
        maximum = int(check[2])*5
        legendary_potatoes(call.message, minimum, maximum, 0)

bot.infinity_polling()
