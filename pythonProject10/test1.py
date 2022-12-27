import telebot
from config import keys, TOKEN
from extensions import ConvertionExeption, Curconverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    text = f"Привет\n\n" \
        f"Я бот, умеющий показывать курсы валют и конвертировать валюты:\n" \
        f"\n Список команд:\n" \
        f"\n/values - список доступных валют\n" \
        f"/help - краткая информация обо мне"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты"
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message):
    text = f"Обрати внимание, что сумму в валюте нужно указывать без запятых\n" \
           f"(Можно использовать точку)\n" \
           f"Пример: доллар рубль 100\n" \
           f"Или USD RUB 100\n\n" \
           f"Список команд:\n" \
           f"\n/values - список доступных валют\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')

    if len(values) != 3:
        raise ConvertionExeption(f"Слишком много параметров.")

    quote, base, amount = values
    total_base = Curconverter.convert(quote, base, amount)

    text = f"Цена {amount} {quote} в {base} - {total_base}"
    bot.send_message(message.chat.id, text)

bot.polling()