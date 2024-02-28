import requests
import xml.etree.ElementTree as ET

# Отправляем GET-запрос на сервер Центрального банка России
response = requests.get("https://www.cbr.ru/scripts/XML_daily.asp")

# Парсим XML-данные
tree = ET.fromstring(response.content)

# Ищем элемент с кодом валюты CNY (китайский юань)
for valute in tree.findall('.//Valute'):
    char_code = valute.find('CharCode').text
    if char_code == 'CNY':
        # Извлекаем значение курса юаня
        value = valute.find('Value').text
        # Заменяем запятую на точку и преобразуем во float
        value_float = float(value.replace(',', '.'))
        print(type(value_float))