# -*- coding: utf-8 -*-
import telebot
import random
import requests
import re
import true_channels
from telebot import types
from bs4 import BeautifulSoup

TOKEN = '1816922959:AAEZ84tdBD4TeCN6yRox4lJzeS9qTtnbLbI'
bot = telebot.TeleBot(TOKEN)
likes = []
basket = []
mark = ''


def menu():
    mark = types.ReplyKeyboardMarkup(resize_keyboard = True)
    go_button = types.KeyboardButton(text = '📰 Запустить ленту')
    catalog_button = types.KeyboardButton(text = '🔝 Топ 5 каналов')
    interesting_button = types.KeyboardButton(text = '🍉 Выбрать категорию')
    basket = types.KeyboardButton(text = '❤️ Понравившееся')
    mark.row(go_button, catalog_button).row(interesting_button).add(basket)
    return mark


@bot.message_handler(commands = ['start'])
def firstmessage(message):
    bot.send_message(message.chat.id, 'Выберите нужное действие на панели снизу 👇: \n\n📰 Запустить ленту - показ 5 любых статей с разных каналов, без ограниения по темам \n\n🔝 Топ 5 каналов - показ 5 телеграм-каналов без ограничения по темам (важно понимать, что "топ" в данном случае не означает рейтинг среди множества каналов, а подразумевает список случайно выбранных) \n\n🍉 Выбрать категорию - возможность выбрать интерсующую вас тематику публикаций \n\n🆕 Новые статьи - показ новых публикаций случайных каналов \n\n❤️ Понравившееся - бибилиотека понравившихся вам статей', reply_markup = menu())

@bot.message_handler(content_types = ['text'])
def answer(message):
    if message.text == '📰 Запустить ленту':
        sec = types.ReplyKeyboardMarkup(resize_keyboard = True)
        random_post = types.KeyboardButton(text = '🎲 5 случайных')
        new_post = types.KeyboardButton(text = '🆕 Новые статьи')
        canel = types.KeyboardButton(text = 'Назад')
        sec.row(random_post, new_post).add(canel)
        bot.send_message(message.chat.id, 'Выберите нужное действие', reply_markup = sec)
    elif message.text == '🔝 Топ 5 каналов':
        list_channel = true_channels.channels()
        true_list_channel = []
        for i in 1,2,3,4,5:
            new_channel = random.choice(list_channel)
            list_channel.remove(new_channel)
            true_list_channel.append(new_channel)
        for element in true_list_channel:
            part = element.split('/s')
            bot.send_message(message.chat.id, part[0] + part[1])
    elif message.text == '🍉 Выбрать категорию':
        category = types.InlineKeyboardMarkup()
        history_post = types.InlineKeyboardButton(text = '👨‍🎨 История', callback_data = 'category history')
        geography_post = types.InlineKeyboardButton(text = '🌎 География', callback_data = 'category geography')
        cracker_post = types.InlineKeyboardButton(text = '🍪 Полезное', callback_data = 'category cracker')
        poll_post = types.InlineKeyboardButton(text = '🎱 Викторины', callback_data = 'category poll')
        category.row(history_post, geography_post).add(cracker_post, poll_post)
        bot.send_message(message.chat.id, '🍒 Выберите категорию', reply_markup = category)
    elif message.text == '❤️ Понравившееся':
        if len(basket) == 0:
            bot.send_message(message.chat.id, 'У вас нет понравившихся статей')
        else:
            spis = types.InlineKeyboardMarkup()
            for i in range(len(basket)):
                page = requests.get(basket[i])
                soup = BeautifulSoup(page.text, 'lxml')
                string_1 = soup.find('head')
                string_2 = string_1.find('meta', property="og:title")
                name = string_2.get('content')
                element = types.InlineKeyboardButton(text = name, callback_data = f'element {basket[i]}')
                spis.add(element)
            bot.send_message(message.chat.id, 'Понравившееся: ', reply_markup = spis)
    elif message.text == '🎲 5 случайных':
        list_book = true_channels.channels()
        true_list_book = []
        bot.send_message(message.chat.id, 'Пожалуйста, подождите: 0/5')
        global likes
        likes = []
        for i in 1, 2, 3, 4, 5:
            new_book = random.choice(list_book)
            list_book.remove(new_book)
            true_list_book.append(new_book)
        for j in 0, 1, 2, 3, 4:
            try:
                url = true_list_book[j]
                page = requests.get(url)
                soup = BeautifulSoup(page.text, 'lxml')
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
                        page = requests.get(true_book)
                        soup = BeautifulSoup(page.text, 'lxml')
                        string_1 = soup.find('head')
                        string_2 = string_1.find_all('meta')[5]
                        opis = string_2.get('content')
                        complete = types.InlineKeyboardMarkup()
                        open_book = types.InlineKeyboardButton(text = 'Открыть статью', url = true_book)
                        like = types.InlineKeyboardButton(text = 'Понравилось ❤️', callback_data = f'like {j}')
                        complete.add(open_book, like)
                        likes.append(true_book)
                        bot.send_message(message.chat.id, f'{opis}\n__________________________________________________________\n\nСсылка на статью: {true_book}', reply_markup = complete)
                        bot.edit_message_text(chat_id=message.chat.id, text = f'Пожалуйста, подождите: {j + 1}/5'.format(message.text), message_id=message.message_id + 1)
                        if j + 1 == 5:
                            bot.edit_message_text(chat_id=message.chat.id, text = "Пожалуйста, подождите: 5/5 ✅".format(message.text), message_id=message.message_id + 1)
                five_articles()
            except:
                return five_articles()
    elif message.text == '🆕 Новые статьи':
        list_book = true_channels.channels()
        true_list_book = []
        bot.send_message(message.chat.id, 'Пожалуйста, подождите: 0/5')
        likes = []
        for i in 1, 2, 3, 4, 5:
            new_book = random.choice(list_book)
            list_book.remove(new_book)
            true_list_book.append(new_book)
        for j in 0, 1, 2, 3, 4:
            def five_articles():
                url = true_list_book[j]
                page = requests.get(url)
                soup = BeautifulSoup(page.text, 'lxml')
                string_1 = soup.find_all('div', class_='tgme_widget_message_wrap js-widget_message_wrap')[-1]
                string_2 = string_1.find('div', class_='tgme_widget_message js-widget_message')
                end = string_2.get('data-post')
                name = soup.title.string
                try:
                    true_book = 'https://t.me/' + end
                    complete = types.InlineKeyboardMarkup()
                    open_book = types.InlineKeyboardButton(text = 'Открыть статью', url = 'https://t.me/' + end)
                    like = types.InlineKeyboardButton(text = 'Понравилось ❤️', callback_data = f'like {j}')
                    complete.add(open_book, like)
                    page = requests.get(true_book)
                    soup = BeautifulSoup(page.text, 'lxml')
                    string_1 = soup.find('head')
                    string_2 = string_1.find_all('meta')[5]
                    opis = string_2.get('content')
                    likes.append(true_book)
                    bot.send_message(message.chat.id, f'{opis}\n___________________________\n\nСсылка на статью: {true_book}', reply_markup = complete)
                    bot.edit_message_text(chat_id=message.chat.id, text = f'Пожалуйста, подождите: {j + 1}/5'.format(message.text), message_id=message.message_id + 1)
                    if j + 1 == 5:
                        bot.edit_message_text(chat_id=message.chat.id, text = 'Пожалуйста, подождите: 5/5 ✅'.format(message.text), message_id=message.message_id + 1)
                except:
                    return five_articles()
            five_articles()
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Выполнено', reply_markup = menu())
@bot.callback_query_handler(func = lambda call: True)
def call_answer(call):
    check = call.data.split()
    if check[0] == 'like':
        number = int(check[1])
        if not(likes[number] in basket): 
            basket.append(likes[number])
        bot.answer_callback_query(callback_query_id=call.id, text='Добавлено')
    elif check[0] == 'category':
        def choosing_category(call, category):
            if category == 'history':
                list_book = ['https://t.me/s/history_0o/']
            elif category == 'geography':
                list_book = ['https://t.me/s/National_Geograph1c/']
            elif category == 'cracker':
                list_book = ['https://t.me/s/vseapps/', 'https://t.me/s/slifcloud/']
            elif category == 'poll':
                list_book = ['https://t.me/s/TriviaGames/']
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
                        bot.send_message(call.message.chat.id, '\n\nСсылка на статью: ' + true_book,  reply_markup = complete)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Пожалуйста, подождите: " + str(j+1) + "/5")
                        if j+1 == 5:
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Пожалуйста, подождите: 5/5 ✅")
                five_articles()
        choosing_category(call, check[1])
    elif check[0] == 'element':
        def dm(call, link):
            page = requests.get(link)
            soup = BeautifulSoup(page.text, 'lxml')
            string_1 = soup.find('head')
            string_2 = string_1.find('meta', property="og:description")
            opis = string_2.get('content')
            open_book = types.InlineKeyboardButton(text = 'Открыть статью', url = check[1])
            complete = types.InlineKeyboardMarkup()
            like = types.InlineKeyboardButton(text = 'Удалить из понравившихся', callback_data = f'delete {check[1]}')
            complete.add(open_book, like)
            bot.send_message(call.message.chat.id, f'{opis}\n__________________________________________________________\n\nСсылка на статью: {check[1]}', reply_markup = complete)
        dm(call, check[1])
bot.polling(none_stop = True)
