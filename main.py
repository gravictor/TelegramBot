import mongodb
import telebot
import random

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
    button4 = types.KeyboardButton('Адмiнка 👑')
    markup.add(button2)
    markup.add(button3)
    markup.add(button1, button4)
    bot.send_message(message.chat.id, "<b>Здоровенькi були, {0.first_name}!</b> \n"
                                      "Нижче знаходяться кнокпі для управління ботом.\n"
                                      "Якщо з'явилися проблеми - / help".format(
        message.from_user), reply_markup=markup, parse_mode='html')
    mongodb.check_and_add_user(message)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Вибирай, що тебе цікавить:\nКриптовалюта\nПогода в Одесі"
                                      "\nНу а якщо ти адмін, то можеш переглянути список зареєстрованих "
                                      "користувачів"
                                      "\n\nНе виходить? спробуй заново/start")


@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == 'Криптовалюта ₿':
        markup = types.InlineKeyboardMarkup(row_width=3)
        item1 = types.InlineKeyboardButton('Курс топових кріптомонет', callback_data='course')
        item2 = types.InlineKeyboardButton('Список торгованих монет наBittrex', callback_data='crypto_list')
        markup.add(item1)
        markup.add(item2)
        bot.send_message(message.chat.id, 'Виберіть, що вас цікавить:', reply_markup=markup)

    elif message.text == 'Гороскоп ♑':
        markup = types.InlineKeyboardMarkup(row_width=8)
        item1 = types.InlineKeyboardButton('Овен (21 березня - 20 квітня)', callback_data='horo')
        item2 = types.InlineKeyboardButton('Телець (21 квітня - 21 травня)', callback_data='horo')
        item3 = types.InlineKeyboardButton('Близнюки (22 травня - 21 червня)', callback_data='horo')
        item4 = types.InlineKeyboardButton('Рак (22 червня - 22 липня)', callback_data='horo')
        item5 = types.InlineKeyboardButton('Лев (23 липня - 21 серпня)', callback_data='horo')
        item6 = types.InlineKeyboardButton('Діва (22 серпня - 23 вересня)', callback_data='horo')
        item7 = types.InlineKeyboardButton('Терези (24 вересня - 23 жовтня)', callback_data='horo')
        item8 = types.InlineKeyboardButton('Скорпіон (24 жовтня - 23 листопада)', callback_data='horo')
        item9 = types.InlineKeyboardButton('Стрілець (24 листопада - 22 грудня)', callback_data='horo')
        item10 = types.InlineKeyboardButton('Козеріг (23 грудня - 20 січня)', callback_data='horo')
        item11 = types.InlineKeyboardButton('Водолій (21 січня - 19 лютого)', callback_data='horo')
        item12 = types.InlineKeyboardButton('Риби (20 лютого - 20 березня)', callback_data='horo')
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
        bot.send_message(message.chat.id, 'Виберіть ваш зоодіак:', reply_markup=markup)

    elif message.text == 'Адмiнка 👑':
        bot.send_message(message.chat.id, mongodb.get_all_users(message))

    elif message.text == 'Погода':
        observation = mgr.weather_at_place('Odessa, Ukraine')
        w = observation.weather
        temp = w.temperature('celsius')["temp"]
        pogoda = w.detailed_status
        bot.send_message(message.chat.id, "Зараз в " + "Одесi" + " " + pogoda)
        bot.send_message(message.chat.id, "Температура зараз в приблизно " + str(temp))
        if temp < 0:
            bot.send_message(message.chat.id, "Зараз холодно, одягайтеся тепліше")
        elif temp < 10:
            bot.send_message(message.chat.id, "Досить прохолодно, куртка точно потрібна")
        elif temp < 20:
            bot.send_message(message.chat.id, "Досить тепло, куртка не потрібна")
        else:
            bot.send_message(message.chat.id, "На вулиці спека - саме час піти на море")


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
                bot.send_message(call.message.chat.id, 'Виберіть, що вас цікавить:', reply_markup=markup)

            elif call.data == 'crypto_list':
                bot.send_message(call.message.chat.id, client.get_all_names())

            elif call.data == 'eth':
                current_price = client.get_last_price(pair=ETH)
                text = "Курс валюти:\n\n{} = {}$".format(ETH, current_price)
                bot.send_message(call.message.chat.id, text)

            elif call.data == 'btc':
                current_price = client.get_last_price(pair=BTC)
                text = "Курс валюти:\n\n{} = {}$".format(BTC, current_price)
                bot.send_message(call.message.chat.id, text)

            elif call.data == 'xrp':
                current_price = client.get_last_price(pair=XRP)
                text = "Курс валюти:\n\n{} = {}$".format(XRP, current_price)
                bot.send_message(call.message.chat.id, text)

            elif call.data == 'ada':
                current_price = client.get_last_price(pair=ADA)
                text = "Курс валюти:\n\n{} = {}$".format(ADA, current_price)
                bot.send_message(call.message.chat.id, text)

            elif call.data == 'doge':
                current_price = client.get_last_price(pair=DOGE)
                text = "Курс валюти:\n\n{} = {}$".format(DOGE, current_price)
                bot.send_message(call.message.chat.id, text)

            elif call.data == 'atom':
                current_price = client.get_last_price(pair=ATOM)
                text = "Курс валюти:\n\n{} = {}$".format(ATOM, current_price)
                bot.send_message(call.message.chat.id, text)

            elif call.data == 'ltc':
                current_price = client.get_last_price(pair=LTC)
                text = "Курс валюти:\n\n{} = {}$".format(LTC, current_price)
                bot.send_message(call.message.chat.id, text)

            elif call.data == 'horo':
                horoskope = random.choice(first) + '' \
                            + random.choice(second) + '' + random.choice(
                    second_add) + '' + random.choice(third)
                bot.send_message(call.message.chat.id, horoskope)

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
