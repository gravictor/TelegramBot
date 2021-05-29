import mongodb
import telebot

from pyowm import OWM
from telebot import types
from bittrex import BittrexClient
from additional.private_data import token
from additional.data import *

owm = OWM('4136767328e7320b9b54e9f338b8cd38')
mgr = owm.weather_manager()
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Погода')
    button2 = types.KeyboardButton('Криптовалюта ₿')
    button3 = types.KeyboardButton('Гороскоп ♑')
    button4 = types.KeyboardButton('Админка 👑')
    markup.add(button2)
    markup.add(button3)
    markup.add(button1, button4)
    bot.send_message(message.chat.id, "<b>Доброго времени суток, {0.first_name}!</b>\n"
                                      "Ниже находятся кнокпи для управления ботом.\n"
                                      "Если появились проблемы - /help".format(
        message.from_user), reply_markup=markup, parse_mode='html')
    mongodb.check_and_add_user(message)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Выбирай что тебя интересует:\nКриптовалюта\nПогода в Одессе"
                                      "\nНу а если ты админ, то можешь просмотреть список зарегестрированных"
                                      " пользователей"
                                      "\n\nНе получается? Попробуй заново /start")


@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == 'Криптовалюта ₿':
        markup = types.InlineKeyboardMarkup(row_width=3)
        item1 = types.InlineKeyboardButton('Курс топовых криптомонет', callback_data='course')
        item2 = types.InlineKeyboardButton('Список торгуемых монет на Bittrex', callback_data='crypto_list')
        markup.add(item1)
        markup.add(item2)
        bot.send_message(message.chat.id, 'Выберите, что вас интересует:', reply_markup=markup)

    elif message.text == 'Гороскоп ♑':
        print('TYT')
        markup = types.InlineKeyboardMarkup(row_width=8)
        item1 = types.InlineKeyboardButton('Овен (21 марта – 20 апреля)', callback_data='ove')
        item2 = types.InlineKeyboardButton('Телец (21 апреля – 21 мая)', callback_data='tel')
        item3 = types.InlineKeyboardButton('Близнецы (22 мая – 21 июня)', callback_data='bli')
        item4 = types.InlineKeyboardButton('Рак (22 июня – 22 июля)', callback_data='rak')
        item5 = types.InlineKeyboardButton('Лев (23 июля – 21 августа)', callback_data='lev')
        item6 = types.InlineKeyboardButton('Дева (22 августа – 23 сентября)', callback_data='dev')
        item7 = types.InlineKeyboardButton('Весы (24 сентября – 23 октября)', callback_data='ves')
        item8 = types.InlineKeyboardButton('Скорпион (24 октября – 23 ноября)', callback_data='sco')
        item9 = types.InlineKeyboardButton('Стрелец (24 ноября – 22 декабря)', callback_data='str')
        item10 = types.InlineKeyboardButton('Козерог (23 декабря – 20 января)', callback_data='koz')
        item11 = types.InlineKeyboardButton('Водолей (21 января – 19 февраля)', callback_data='vod')
        item12 = types.InlineKeyboardButton('Рыбы (20 февраля – 20 марта))', callback_data='rib')
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)
        markup.add(item6)
        markup.add(item7)
        markup.add(item8)
        markup.add(item9)
        markup.add(item10)
        markup.add(item11)
        markup.add(item12)
        bot.send_message(message.chat.id, 'Выберите ваш зоодиак:', reply_markup=markup)

    elif message.text == 'Админка 👑':
        bot.send_message(message.chat.id, mongodb.get_all_users(message))

    elif message.text == 'Погода':
        observation = mgr.weather_at_place('Odessa, Ukraine')
        w = observation.weather
        temp = w.temperature('celsius')["temp"]
        pogoda = w.detailed_status
        bot.send_message(message.chat.id, "Сейчас в " + "Одессе" + " " + pogoda)
        bot.send_message(message.chat.id, "Температура сейчас в приблизительно " + str(temp))
        if temp < 0:
            bot.send_message(message.chat.id, "Сейчас холодно, одевайтесь теплее")
        elif temp < 10:
            bot.send_message(message.chat.id, "Довольно прохладно, куртка точно нужна")
        elif temp < 20:
            bot.send_message(message.chat.id, "Довольно тепло, куртка не нужна")
        else:
            bot.send_message(message.chat.id, "На улице жара - самое время пойти на море)")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    client = BittrexClient()
    try:
        if call.message:
            if call.data == 'course':
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton('Ethereum', callback_data='eth')
                item2 = types.InlineKeyboardButton('Bitcoin', callback_data='btc')
                item3 = types.InlineKeyboardButton('ADA', callback_data='ada')
                item4 = types.InlineKeyboardButton('Ripple', callback_data='xrp')
                item5 = types.InlineKeyboardButton('Dogecoin', callback_data='doge')
                item6 = types.InlineKeyboardButton('Litecoin', callback_data='ltc')
                item7 = types.InlineKeyboardButton('ATOM', callback_data='atom')
                markup.add(item1)
                markup.add(item2)
                markup.add(item3)
                markup.add(item4)
                markup.add(item5)
                markup.add(item6)
                markup.add(item7)
                bot.send_message(call.message.chat.id, 'Выберите, что вас интересует:', reply_markup=markup)

            elif call.data == 'crypto_list':
                bot.send_message(call.message.chat.id, client.get_all_names())

            elif call.data == 'eth':
                current_price = client.get_last_price(pair=ETH)
                text = "Курс валюты:\n\n{} = {}$".format(ETH, current_price)
                bot.send_message(call.message.chat.id, text)

            elif call.data == 'btc':
                current_price = client.get_last_price(pair=BTC)
                text = "Курс валюты:\n\n{} = {}$".format(BTC, current_price)
                bot.send_message(call.message.chat.id, text)

            elif call.data == 'xrp':
                current_price = client.get_last_price(pair=XRP)
                text = "Курс валюты:\n\n{} = {}$".format(XRP, current_price)
                bot.send_message(call.message.chat.id, text)

            elif call.data == 'ada':
                current_price = client.get_last_price(pair=ADA)
                text = "Курс валюты:\n\n{} = {}$".format(ADA, current_price)
                bot.send_message(call.message.chat.id, text)

            elif call.data == 'doge':
                current_price = client.get_last_price(pair=DOGE)
                text = "Курс валюты:\n\n{} = {}$".format(DOGE, current_price)
                bot.send_message(call.message.chat.id, text)

            elif call.data == 'atom':
                current_price = client.get_last_price(pair=ATOM)
                text = "Курс валюты:\n\n{} = {}$".format(ATOM, current_price)
                bot.send_message(call.message.chat.id, text)

            elif call.data == 'ltc':
                current_price = client.get_last_price(pair=LTC)
                text = "Курс валюты:\n\n{} = {}$".format(LTC, current_price)
                bot.send_message(call.message.chat.id, text)

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
