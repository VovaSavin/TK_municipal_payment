import requests
from bs4 import BeautifulSoup as bs
from tkinter import messagebox


def take_tariff_electro():
    """
    Получает цену за 1 кВт електроенергии
    С помощью парсинга сайта minfin.com.ua
    """
    try:
        url = "https://index.minfin.com.ua/ua/tariff/electric/"

        html = requests.get(url).text

        soup = bs(html, "html.parser")
        main = soup.find('main', class_='mfz-page-wrap mfz-section')
        warng = main.find('article', id='idx-content')
        trff = warng.select('p:nth-child(1) > big:nth-child(1)')
        old = trff[0].text
        new = old.replace(',', '.')
        return float(new)
    except requests.exceptions.ConnectionError:
        return 1.68


def take_tariff_water():
    """
    Получает цену за 1 куб.см воды
    С помощью парсинга сайта minfin.com.ua
    """
    try:
        url = "https://index.minfin.com.ua/ua/tariff/kiev/water/"

        html = requests.get(url).text

        soup = bs(html, "html.parser")
        main = soup.find('main', class_='mfz-page-wrap mfz-section')
        tbl = main.find('table', class_='grid')
        trff = tbl.select('td.bg-grey')[1]
        old = trff.text
        new = old.replace(',', '.')
        return float(new)
    except requests.exceptions.ConnectionError:
        return 21.756
