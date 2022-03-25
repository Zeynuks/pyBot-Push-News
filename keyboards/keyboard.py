from telebot import types

def keyboard_menu():
    """Функция инициализирующая стартовое меню бота"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
    buttons = [('📰 Лента', '🔝 Каналы'), ('🍉 Категории', '❤️ Понравившееся')]
    keyboard.add(*buttons[0]).add(*buttons[1])
    return keyboard

def sub_keyboard_menu():
    """Функция инициализирующая новостное меню бота"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    buttons = [('🎲 5 случайных', '🆕 Новые статьи'), 'Назад']
    keyboard.add(*buttons[0]).add(buttons[1])
    return keyboard

def article_keyboard(url):
    keyboard = types.InlineKeyboardMarkup()
    open_article = types.InlineKeyboardButton(text= 'Открыть', url = url)
    like = types.InlineKeyboardButton(text= '🤍', callback_data= f'like {url}')
    keyboard.add(open_article, like)
    return keyboard

def category_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    history = types.InlineKeyboardButton(text= '👨‍🎨 История', callback_data= 'category history')
    geography = types.InlineKeyboardButton(text= '🌎 География', callback_data= 'category geography')
    cracker = types.InlineKeyboardButton(text= '🍪 Полезное', callback_data= 'category cracker')
    poll = types.InlineKeyboardButton(text= '🎱 Викторины', callback_data= 'category poll')
    keyboard.add(history, geography).add(cracker, poll)
    return keyboard
