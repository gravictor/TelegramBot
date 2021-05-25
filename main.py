import mongodb
import telebot

from pyowm import OWM
from telebot import types
from bittrex import BittrexClient
from private_info import token

bot = telebot.TeleBot(token)
owm = OWM('4136767328e7320b9b54e9f338b8cd38')
mgr = owm.weather_manager()

ETH = "USD-ETH"
BTC = "USD-BTC"
XRP = "USD-XRP"
DOGE = "USD-DOGE"
ADA = "USD-ADA"
LTC = "USD-LTC"
ATOM = "USD-ATOM"


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Погода')
    button2 = types.KeyboardButton('Криптовалюта ₿')
    button3 = types.KeyboardButton('')
    button4 = types.KeyboardButton('Админка')
    markup.add(button2)
    markup.add(button3)
    markup.add(button1, button4)
    bot.send_message(message.chat.id, "<b>Доброго времени суток, {0.first_name}!</b>\n"
                                      "Ниже находятся кнокпи для управления ботом.\n"
                                      "Если появились проблемы - /help".format(
        message.from_user), reply_markup=markup, parse_mode='html')
    mongodb.check_and_add_user(message)


@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == 'Криптовалюта ₿':
        markup = types.InlineKeyboardMarkup(row_width=3)
        item1 = types.InlineKeyboardButton('Курс топовых криптомонет', callback_data='course')
        item2 = types.InlineKeyboardButton('Список всех монет на Bittrex', callback_data='crypto_list')
        markup.add(item1)
        markup.add(item2)
        bot.send_message(message.chat.id, 'Выберите, что вас интересует:', reply_markup=markup)
    elif message.text == 'Админка':
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


@bot.message_handler(commands=['help'])
def helpmess(message):
    print('tyt')
    bot.send_message(message.chat.id, "В данный момент бот находится в разработке. Доступные команды: "
                                      "\nЧтобы начать с самого начала - нажми /start"
                                      "\nЧтобы узнать текущую погоду - нажми /weather"
                                      "\nЧтобы узнать курс Bitcoin - нажми /crypto")


@bot.message_handler(commands=['crypto'])
def send_welcome(message):
    client = BittrexClient()
    current_price = client.get_last_price(pair=ETH)
    text = "*Курс валюты:*\n\n*{}* = {}$".format(ETH, current_price)
    bot.send_message(message.chat.id, text)
    bot.send_message(message.chat.id, client.get_all_names())


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


@bot.message_handler(content_types=['text'])
def send_weather(message):
    bot.send_message(message.chat.id, "Бот тебя не понимает, нажми /help)")


bot.polling(none_stop=True)
