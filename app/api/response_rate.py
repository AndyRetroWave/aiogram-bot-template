import requests
import xml.etree.ElementTree as ET


response = requests.get("https://www.cbr.ru/scripts/XML_daily.asp")
tree = ET.fromstring(response.content)
value = None

for valute in tree.findall('.//Valute'):
    char_code = valute.find('CharCode').text
    if char_code == 'CNY':
        value = float(valute.find('Value').text.replace(',', '.'))
        yuan_rate = value + value * 0.1
        formatted_num = "{}\\.{}".format(
                int(yuan_rate), int(yuan_rate * 100) % 100)
        break

