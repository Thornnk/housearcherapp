import json
from sites.idealista import *
from notifications import *


def get_config():
    with open("search_config.json") as j:
        return json.load(j)


def main_search():
    idealista.search()


def notify():
    if bool(config["notifications"]) and config["email"]:
        notif.run()


if __name__ == "__main__":
    config = get_config()

    idealista = Idealista(config)
    fotocasa = None
    pisos = None
    yaencontre = None
    redpiso = None
    tecnocasa = None
    milanuncios = None
    # etc

    notif = Notification(config)

    main_search()
    notify()

# TODO Los resultados no se guardan con un ID unico así que al run() varias veces, duplicará
# TODO Coger el ID de un regex de las url
