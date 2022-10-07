import requests
import datetime
from bs4 import BeautifulSoup
import json
import time
#import csv

def get_data():
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    headers = {
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 YaBrowser/22.9.2.1495 Yowser/2.5 Safari/537.36'
    }

    books = []
    url = 'https://www.labirint.ru/genres/2308/?display=table'
    responce = requests.get(url=url, headers=headers)
    #print(responce)
    soup = BeautifulSoup(responce.text, 'lxml')
    page_count = int(soup.find('div', class_='pagination-numbers').find_all('a')[-1].text)

    count_books = 0

    for page in range(1, page_count+1):
        #print(f'СТАНИЦА {page}')
        url = f'https://www.labirint.ru/genres/2308/?page={page}&display=table'
        responce = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(responce.text, 'lxml')
        books_items = soup.find('tbody', class_='products-table__body').find_all('tr')
        for book in books_items:
            try:
                book_title = book.find('td', class_='col-sm-4').text.strip()
            except:
                book_title = "Нету"

            try:
                author = book.find('td', class_='col-sm-2').text.strip()
            except:
                author ="Нету"

            try:
                price_after = book.find('span', class_='price-val').text.replace('₽', '').strip()
            except:
                price_after = "Нету"

            try:
                sell = book.find('span', class_='price-val')['title'].strip()
            except:
                sell = "Нету"

            try:
                price_before = book.find('span', class_='price-old').text.strip()
            except:
                price_before = "Нету"

            url = f'https://www.labirint.ru{book.find("td", class_="col-sm-4").find("a")["href"]}'
            #print(price_after, sell, price_before, url)
            #break
            count_books += 1

            books.append(
                {
                    'title': book_title,
                    'author': author,
                    'price_befor': price_before,
                    'price_after': price_after,
                    'sell': sell,
                    'url': url,
                }
            )
    with open(f'labirint_{cur_time}.json', 'w', encoding='UTF-8') as file:
        json.dump(books, file, indent=4, ensure_ascii=False)

    print(f'Всего книг собрали{count_books}')

def main():
    get_data()

if __name__ == '__main__':
    main()

