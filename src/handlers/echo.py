from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from src.models.users.dao import add_user
from src.keyboards.keyboards import keyboard

import requests
import xml.etree.ElementTree as ET

# Send a GET request to the Central Bank of Russia server
response = requests.get("https://www.cbr.ru/scripts/XML_daily.asp")

# Parse XML data
tree = ET.fromstring(response.content)

# Initialize the variable to store the exchange rate of CNY
value = None

# Find the element with the currency code CNY (Chinese Yuan)
for valute in tree.findall('.//Valute'):
    char_code = valute.find('CharCode').text
    if char_code == 'CNY':
        # Extract the exchange rate of the Chinese Yuan
        value = float(valute.find('Value').text.replace(',', '.'))
        break  # Exit the loop once the value is found

router = Router()


@router.message(Command(commands=["start"]))
async def start(message: Message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    user_id = message.from_user.id
    await add_user(first_name, last_name, username, user_id)
    await message.reply(
        text='Thank you, we have added you to the list. We will send this list to the president.',
        reply_markup=keyboard
    )


@router.message()
async def echo_message(message: Message):
    try:
        text = float(message.text)
        if value is not None:
            value_markup = text * (value + value * 0.2) + 1200
            round_value = round(value_markup)
            await message.reply(text=str(round_value))
        else:
            await message.reply(text="Извините, не удалось получить данные о валюте")
    except ValueError:
        await message.reply(text="Пожуйста введите стоимость в Юанях.")
