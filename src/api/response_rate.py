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