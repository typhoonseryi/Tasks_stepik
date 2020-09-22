from bs4 import BeautifulSoup
from decimal import Decimal
import requests


def convert(amount, cur_from, cur_to, date):
    payload = {'date_req': date}
    response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp', params=payload)  # Использовать переданный requests
    soup = BeautifulSoup(response.content, 'xml')
    if cur_from == 'RUR':
        first = Decimal(1)
    else:
        first_str = soup.find('CharCode', text=cur_from).find_next_sibling('Value').string.replace(',', '.')
        nom_first = soup.find('CharCode', text=cur_from).find_next_sibling('Nominal').string
        first = Decimal(first_str) / Decimal(nom_first)
    if cur_to == 'RUR':
        second = Decimal(1)
    else:
        second_str = soup.find('CharCode', text=cur_to).find_next_sibling('Value').string.replace(',', '.')
        nom_second = soup.find('CharCode', text=cur_to).find_next_sibling('Nominal').string
        second = Decimal(second_str) / Decimal(nom_second)
    result_raw = amount * Decimal(first / second)
    result = Decimal(result_raw).quantize(Decimal('.0001'))
    return result

print(convert(1000, 'USD', 'RUR', ''))