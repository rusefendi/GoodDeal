import requests
from bs4 import BeautifulSoup
import re
import csv
from telegram import post
from time import sleep


def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
        total_pages = re.search('[0-9]+', pages).group(0)
    except:
        total_pages = 1

    return int(total_pages)


def get_most_resent_ad():
    with open('avito.csv', 'r') as file:
        reader = csv.reader(file)
        for i in reader:
            data = {'title': i[0], 'price': i[1], 'metro': i[2], 'url': i[3]}
    return data


def write_csv(data):
    with open('avito.csv', 'w') as f:
        writer = csv.writer(f)

        writer.writerow((data['title'], data['price'],
                        data['metro'], data['url']))


# parsing result page
def get_page_data(html, resent_ad):
    soup = BeautifulSoup(html, 'lxml')

    ads = soup.find('div', class_='catalog-list').find_all('div', class_='item_table')

    for ad in ads:
        # title, price, url
        try:
            title = ad.find('h3').text.strip()
        except:
            title = ''

        try:
            url = ad.find('a').get('href')
        except:
            url = ''

        try:
            price = ad.find('div', class_='about').text.strip()
        except:
            price = ''

        try:
            metro = ad.find('div', class_='data').find_all('p')[-1].text
        except:
            metro = ''

        data = {'title': title, 'price': price, 'metro': metro, 'url': 'https://avito.ru' + url}

        if data == resent_ad:
            # if we reach most resent ad, return True to break cycle
            return True

        if ad == ads[0]:
            # writing in csv file most recent ad to prevent duplicates after script reload
            write_csv(data)

        post(data)
        print(data)


def main():
    # url which i decided to use
    # you can use any other

    url = 'https://www.avito.ru/moskva/igry_pristavki_i_programmy/igrovye_pristavki?p=1&pmax=13000&pmin=8000&user=1&bt=1&q=sony+playstation+4&i=1&s=104'
    base_url = 'https://www.avito.ru/moskva/igry_pristavki_i_programmy/igrovye_pristavki?'
    page_part = 'p='
    query_part = '&pmax=13000&pmin=8000&user=1&bt=1&q=sony+playstation+4&i=1&s=104'

    # count number of pages
    total_pages = get_total_pages(get_html(url))

    while True:
        try:
            resent_ad = get_most_resent_ad()
        except:
            resent_ad = None

        for i in range(1, total_pages + 1):
            # generate valid url
            url_gen = base_url + page_part + str(i) + query_part

            # get valid html file
            html = get_html(url_gen)

            # parsing ads
            if get_page_data(html, resent_ad):
                break

        # sleeping for 1 hour
        sleep(60 * 60 * 1)


if __name__ == '__main__':
    main()
