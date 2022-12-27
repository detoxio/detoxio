import requests
import json
from config import keys


class ConvertionExeption(Exception):
    pass

class Curconverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionExeption(f"Невозможно перевести одинаковые валюты {base}.")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionExeption('Не удалось обработать значение {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionExeption("Не удалось обработать значения {base}.")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExeption("Не удалось обработать количество {amount}.")
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        text = total_base * amount
        return text