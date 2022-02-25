import config
import telebot
from bs4 import BeautifulSoup
import requests
from telebot import types
import datetime

bot = telebot.TeleBot('5163563504:AAEvMvDVb7uYo0qyVTYcBmL8wfEU26Ta4SM')

url = "https://www.gismeteo.ru/weather-gomel-4918/"
headers = {
        "Accept": "*/*",
                    "user-agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
           }


@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🌦 Погода сейчас")
    item2 = types.KeyboardButton("☔️Погода завтра")
    markup.add(item1, item2)
    try:
        bot.send_message(m.chat.id, f"Hello,{m.from_user.last_name}!", parse_mode='html', reply_markup=markup)

    except BaseException as e:
        print(repr(e))


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.chat.type == 'private':
        if message.text == "🌦 Погода сейчас":
            try:
                req_now = requests.get(url, headers=headers)
                soup_now = BeautifulSoup(req_now.content, 'lxml')
                text = soup_now.find('div', class_="date")
                text1 = soup_now.find('span', class_="unit unit_temperature_c")
                text2 = soup_now.find('div', class_="weather-feel").find('span', class_="unit unit_temperature_c")
                div = soup_now.find('a', class_="weathertab weathertab-block tooltip")
                bot.send_message(message.chat.id,
                                 f"{div.get('data-text')}\n{text.text}:    {text1.text}\n По ощущению:    {text2.text}",
                                 parse_mode='html')

            except BaseException:
                bot.send_message(message.chat.id, "Something goes wrong...")

        elif message.text == "☔️Погода завтра":
            try:
                req_tomorrow = requests.get(url, headers=headers)
                soup_tomorrow = BeautifulSoup(req_tomorrow.content, 'lxml')
                tomorrow = soup_tomorrow.find('a', class_="weathertab weathertab-link tooltip").find_next('a')
                date = datetime.datetime.today() + datetime.timedelta(days=1)
                tom_date = date.strftime("%w")
                date_tomorrow = soup_tomorrow.find('div', class_=f'date date-{tom_date}')
                tomorrow_night = soup_tomorrow.find('div', class_="tab-temp tab-charts") \
                    .find('span', class_="unit unit_temperature_c") \
                    .find_next(class_="unit unit_temperature_c") \
                    .find_next(class_="unit unit_temperature_c")
                tomorrow_day = tomorrow_night.find_next(class_="unit unit_temperature_c")
                bot.send_message(message.chat.id,
                                 f"{date_tomorrow.text}\n {tomorrow.find_next('a').get('data-text')}\n"
                                 f" Ночью:    {tomorrow_night.text}\n Днем:    {tomorrow_day.text}",
                                 parse_mode='html')
            except BaseException as e:
                print(repr(e))
                bot.send_message(message.chat.id, "Something goes wrong...")


    # else:
    #     bot.send_message(message.from_user.id, "I don't understand. Please, write '/help'")


bot.polling(none_stop=True, interval=0)

