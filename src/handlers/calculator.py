from aiogram.types import Message
from src.filters.filters import *
from src.handlers.user import router

import requests
import xml.etree.ElementTree as ET

# Send a GET request to the Central Bank of Russia server
response = requests.get("https://www.cbr.ru/scripts/XML_daily.asp")
tree = ET.fromstring(response.content)
value = None

# Find the element with the currency code CNY (Chinese Yuan)
for valute in tree.findall('.//Valute'):
    char_code = valute.find('CharCode').text
    if char_code == 'CNY':
        # Extract the exchange rate of the Chinese Yuan
        value = float(valute.find('Value').text.replace(',', '.'))
        break  # Exit the loop once the value is found

@router.message()
async def echo_message(message: Message):
    try:
        text = float(message.text)
        if value is not None:
            value_markup = text * (value + value * 0.2) + 1200
            round_value = round(value_markup)
            await message.reply(text=str(f"{round_value} рублей"))
            print(value)
            return 
        else:
            await message.reply(text="Извините, не удалось получить данные о валюте")
    except ValueError:
        await message.reply(text="Пожуйста введите стоимость в Юанях.")