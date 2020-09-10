import sys
import time
import config
import requests
import telegram
from bs4 import BeautifulSoup
from pymongo import MongoClient

bot = telegram.Bot(token='1195345949:AAFBrpXe-tpqgSs0AXmMwVINTUjVf2Z-V-A')
chat_id = '-1001469033921'

client = MongoClient(config.host, username=config.username,  password=config.password)
db = client.sinta
col_google_scholars = db.google_scholars
col_universities = db.universities

university_saved = []
page_saved = [0]

def cleansing_authors(authors):
    if authors[-1] == '...':
        del authors[-1]
        return authors
    return authors

def get_publications(papers, university_id, university_name, page_site):
    for paper in papers:
        link = paper.find('dt').find('a')

        authors = []
        publisher = []
        for no, dd in enumerate(paper.find_all('dd')):
            if no == 0:
                authors.append(cleansing_authors(dd.text.strip().split(", ")))
            else:
                publisher.append(dd.text.strip())

        col_google_scholars.insert_one({
            'university_id': university_id,
            'title': link.text,
            'link': link['href'],
            'authors': authors[0],
            'publisher': publisher[0],
            'citation': paper.find_all("td", class_="index-val uk-text-center")[1].text,
        })

        text = "Publikasi dengan judul '" + link.text + \
               "' dari '" + university_name +\
               "' pada halaman ke-" + str(page_site) + \
               " berhasil disimpan!"

        print(text)
        bot.sendMessage(chat_id=chat_id,
                        text=text)

def request_publication(page_site, university_id):
    page = requests.get(
        'http://sinta.ristekbrin.go.id/affiliations/detail?page=' + str(page_site) + '&id=' + str(
            university_id) +
        '&view=documents')
    soup = BeautifulSoup(page.text, 'html.parser')
    papers = soup.find('tbody').find_all('tr')

    return papers

def main(university_checkpoint=None):
    for university in col_universities.find():
        if university_checkpoint not in university_saved:
            i = page_saved[-1]
            while True:
                i += 1

                try:
                    papers = request_publication(i, university['id'])
                except ConnectionError as e:
                    print(str(e))
                    bot.sendMessage(chat_id=chat_id,
                                    text=str(e))
                    time.sleep(60)
                    main(university['id'])

                if len(papers) == 0:
                    text = "Semua data publikasi dari universitas '" + university['name'] + "' telah tersimpan!"
                    print(text)
                    bot.sendMessage(chat_id=chat_id,
                                    text=text)
                    university_saved.append(university['id'])
                    page_saved.append(0)
                    break

                get_publications(papers, university['id'], university['name'], i)
if __name__ == "__main__":
    main()