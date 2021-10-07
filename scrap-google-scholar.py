import sys
import time
import config
import requests
import telegram
import logging
logging.basicConfig(level=logging.INFO)
from bs4 import BeautifulSoup
from pymongo import MongoClient

bot = telegram.Bot(token='YOURTELEGRAMTOKEN')
chat_id = 'YOURCHATID'

client = MongoClient(config.host, username=config.username,  password=config.password)
db = client.sinta
col_google_scholars = db.google_scholars
col_universities = db.universities
col_university_checkpoint = db.university_checkpoint

page_saved = [16]

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
            'authors': '' if len(authors) == 0 else authors[0],
            'publisher': '' if len(publisher) == 0 else publisher[0],
            'citation': '' if len(paper.find_all("td", class_="index-val uk-text-center")) < 2 else
                            paper.find_all("td", class_="index-val uk-text-center")[1].text
        })

        text = "Publikasi dengan judul '" + link.text + \
               "' dari '" + university_name +\
               "' pada halaman ke-" + str(page_site) + \
               " berhasil disimpan!"

        logging.info(text)

def request_publication(page_site, university_id):
    page = requests.get(
        'http://sinta.ristekbrin.go.id/affiliations/detail?page=' + str(page_site) + '&id=' + str(
            university_id) +
        '&view=documents')
    soup = BeautifulSoup(page.text, 'html.parser')
    papers = soup.find('tbody').find_all('tr')

    return papers

def main():
    for university in col_universities.find():
        check_univ = col_university_checkpoint.find_one({'university_id': university['id']})
        if check_univ == None:
            i = page_saved[-1]
            while True:
                i += 1

                try:
                    papers = request_publication(i, university['id'])
                except ValueError as e:
                    logging.info(str(e))
                    bot.sendMessage(chat_id=chat_id,
                                    text=str(e))
                    time.sleep(60)
                    main(university['id'])

                if len(papers) == 0:
                    col_university_checkpoint.insert_one({
                        'university_id': university['id']
                    })
                    page_saved.append(0)
                    text = "Semua data publikasi dari universitas '" + university['name'] + "' telah tersimpan!"
                    logging.info(text)
                    bot.sendMessage(chat_id=chat_id,
                                    text=text)
                    break

                get_publications(papers, university['id'], university['name'], i)

                text = "Publikasi dari '" + university['name'] + \
                       "' pada halaman ke-" + str(i) + \
                       " berhasil disimpan!"

                bot.sendMessage(chat_id=chat_id, text=text)
if __name__ == "__main__":
    main()
