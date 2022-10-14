# Импортируем библиотеки
import requests
import datetime
from bs4 import BeautifulSoup
import json
import time
from openpyxl.workbook import Workbook

def get_data_html(url):  # Получение url
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 YaBrowser/22.9.2.1495 Yowser/2.5 Safari/537.36'
    }
    responce = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(responce.text, 'lxml')
    return soup

# Основная функция где собирается: количество страниц, количество книг и информация о собранных книгах, которая позже сохраняется в файле(json)
def get_books(url):
    books = []
    #cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M") # Переименование файла(json)
    html_for_number_page = get_data_html(url)
    page_count = int(html_for_number_page.find('div', class_='pagination-numbers').find_all('a')[-1].text) # Количество страниц
    count_books = 0
    for page in range(1, page_count+1): # Подсчет количество книг и собираем информацию о собранных книгах
        url_page = f'{url}?display=table&page={page}'
        soup = get_data_html(url_page)
        books_items = soup.find('tbody', class_='products-table__body').find_all('tr')

        for k, book in enumerate(books_items):
            try:
                book_title = book.find('td', class_='col-sm-4').text.strip() # Название книги
            except:
                book_title = "Нету"

            try:
                author = book.find('td', class_='col-sm-2').text.strip() # Автор
            except:
                author ="Нету"

            try:
                price_after = book.find('span', class_='price-val').text.replace('₽', '').replace(' ', '').strip() # Цена после скидки
            except:
                price_after = "Нету"

            try:
                sell = int(book.find('span', class_='price-val')['title'].strip().split()[0][1:-1]) # Скидка
            except:
                sell = "Нету"

            try:
                price_before = int(book.find('span', class_='price-old').text.strip().replace(' ', '')) # Цена до скидки
            except:
                price_before = "Нету"

            a = book.find()
            url_book = f'https://www.labirint.ru{book.find("td", class_="col-sm-4").find("a")["href"]}' # url адрес на отдельную книгу
            count_books += 1
            books.append(
                {
                    'title': book_title,
                    'author': author,
                    'price_befor': price_before,
                    'price_after': price_after,
                    'sell': sell,
                    'url_book': url_book,
                }
            )

    m = url.split('/')[-2]
    books.append(m)
    print(f'Категория {m}')
    print(f'Всего книг собрали{count_books}')  # Всего книг собрали
    return books

def save_json(data: list):# Переименование файла(json) по дате(чило_месяц_год_часы_минуты) и жанру книг
    file_name = get_file_name(data[-1]) + '.json'
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data[:-1], file, indent=4, ensure_ascii=False)

def save_excel(data: list):
    headers = list(data[0].keys())
    file_name = get_file_name(data[-1]) + '.xlsx'

    wb = Workbook()
    page = wb.active
    page.title = 'data'
    page.append(headers)
    for book in data[:-1]:
        row = []
        for k, v in book.items():
            row.append(v)
        page.append(row)
    wb.save(filename=file_name)

def get_file_name(m):
    return time.strftime("%d_%m_%Y_%H_%M")+ '_' + m
def main(url):
    books_data = get_books(url)
    save_excel(books_data)
    save_json(books_data)

if __name__ == '__main__':
    main('https://www.labirint.ru/genres/2308/')