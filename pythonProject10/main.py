import telebot
from config import keys, TOKEN
from extensions import ConvertionExeption, Curconverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    text = f"Привет\n\n" \
        f"Привет, я бот складывающий курсы твоих любимых валют\n" \
        f"Просто введи данные по форме: биткойн рубль 100\n" \
        f"И твоя жизнь станет немного проще\n" \
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
           f"(Можно использовать точку)\n\n" \
           f"Пример: доллар рубль 100.5\n\n" \
           f"Важно! Все пишется с маленьких букв\n\n" \
           f"Список команд:\n" \
           f"/start - Обратно в начало\n" \
           f"/values - Список доступных валют\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionExeption(f"Слишком много параметров.")

        quote, base, amount = values
        total_base = Curconverter.convert(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")

    except Exception as e:
        bot.reply_to(message, f"Извините, но я не могу этого сделать\n{e}")
    else:
        text = f"Цена {amount} {quote} в {base} - {total_base}"
        bot.send_message(message.chat.id, text)

bot.polling(non_stop=True)