from config import Logs

path = {
    "prefix": "/home/krzysztof/Dokumenty/WEDT/vocabulae-adsunt"
}

database = {
    'path': path['prefix'] + '/database/vocabulae.db',
    'name': 'vocabulae.db',
}
wolne_lektury = {
    'host': 'https://wolnelektury.pl',
}
lekser = {
    'stopwords-path': path['prefix'] + '/resources/polish-stopwords.txt',
    'stopwords': []
}


def create_config():
    with open(lekser['stopwords-path'],
          encoding='utf-8') as f:
        lekser['stopwords'] = f.read()

    Logs.setLogLevel()


create_config()