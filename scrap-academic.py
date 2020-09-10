import sys
import requests
from bs4 import BeautifulSoup
from furl import furl
from pymongo import MongoClient

client = MongoClient()
db = client.sinta
col_universities = db.universities

def main():
    i = 0
    while True:
        i+=1
        page = requests.get('http://sinta.ristekbrin.go.id/affiliations?page=' + str(i) + '&sort=all2')
        soup = BeautifulSoup(page.text, 'html.parser')
        universities = soup.find('tbody').find_all('tr')
        if len(universities) == 0:
            print("Semua data universitas tersimpan!")
            sys.exit()
        for university in universities:
            link = university.find('dt').find('a')

            f = furl(link['href'])

            col_universities.insert_one({
                'id': f.args['id'],
                'name': link.text
            })

            print("Data universitas " + link.text + " tersimpan!")
if __name__ == "__main__":
    main()