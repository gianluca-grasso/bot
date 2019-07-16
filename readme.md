Simple bot with threaded downloader for ilgeniodellostreaming.*

Library Requirements:

    - Selenium with Firefox
    - Flask                             
    - Pickle
    - Requests
    - duckpy
    - beautifulsoup
    - json


pip install selenium Flask requests dukpy beautifulsoup4

Application is composed from 2 part:

    - main.py (front-end manage)
    - download_svc.py (back-end)


Other modules:

    - lib.py            bot library: search, capture sources, ecc
    - parallel.py       multithreaded downloaderer
    - index.html        html front-end
    - episodes.py       episode, episodes classes
