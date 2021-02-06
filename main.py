import requests
from bs4 import BeautifulSoup
import telebot
import config
from telebot import types

bot = telebot.TeleBot(config.TOKEN)

keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('iphone 5', 'iphone X', 'iphone 6', 'iphone 7')

@bot.message_handler(content_types=['text'])
def start(message):
    bot.send_message(message.from_user.id, "Что будем искать?")
    bot.register_next_step_handler(message, get_name, )  # следующий шаг – функция get_name


def get_name(message):  # получаем название
    global name
    name = 'https://liberti.ru/search/?q=Дисплей%20' + message.text + '&filter_1427=47&price_7_min=&price_7_max='
    url = name
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('div', {'class': 'product-list-item__container'})
    channel_items = {''}
    for i in items:
        itemName = i.find('a', {'class': 'product-list-item__name-link'}).text.strip()
        itemPrice = i.find('div', {'class': 'product-list-item__price-value'})
        items_str = itemName + ' ' + itemPrice.text.strip() + '\n'
        # items_str = itemName + itemPrice.text.lstrip() + '\n`'
        channel_items = items_str
        bot.send_message(message.from_user.id, {channel_items})


bot.polling(none_stop=True, interval=0)
