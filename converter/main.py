import telebot
import requests
import json

exchanges = {
    'Доллар': 'USD',
    'Евро': 'EUR',
    'Рубль': 'RUB'
}
TOKEN = "5589818618:AAE6tr3Ev0wOaFQAVxtRMmOBn7QhZugVWhw" #Передаем токен

bot = telebot.TeleBot(TOKEN) #присваиваем библиотеку


@bot.message_handler(commands=['start', 'help']) #Задаем базовые команды бота
def start(message: telebot.types.Message):
    text = "Добро пожаловать в обменник !"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text) #Помечаем прочитанный текст. Метод reply_to

    @bot.message_handler(content_types=['text'])
    def converter(message: telebot.types.Message):
        base, sym, amount = message.text.split()
        r = requests.get(f"https://api.exchangeratesapi.io/latest?base={base}&symbols={sym}")
        resp = json.loads(r.content)
        new_price = resp['rates'][sym] * float(amount)
        bot.reply_to(message, f"Цена {amount} {base} в {sym} : {new_price}") #Отвечаем методом по форме

bot.polling()
