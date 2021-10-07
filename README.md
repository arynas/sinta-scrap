# Sinta Scrap

### Mengambil data publikasi universitas dari [Sinta](https://sinta.ristekbrin.go.id/).

#### Syarat
- Python 3.6 ke atas

#### Fitur
- Proses scrap dapat dipantau melalui Telegram
- Hasil scrap langsung disimpan ke MongoDB

#### Instalasi
- ``cp config.py.example config.py``
- ``pip install -r requirements.txt``

#### Ambil data seluruh Universitas
- ``python scrap-academic.py``

#### Ambil data seluruh Publikasi dari seluruh Universitas
- ``python scrap-google-scholar.py``

#### Ambil data seluruh Publikasi dari Universitas tertentu
- ``python scrap-google-scholar.py``
