import json


class Idealista:
    def __init__(self, config):
        self.config = config
        self.mode = None
        self.house_types = None
        self.locations = None
        self.max_price = None
        self.set_attributes(config)
        self.search_urls = self.build_urls()
        self.results = []

    def set_attributes(self, config):
        if config["mode"] == "buy":
            self.mode = "venta"
        elif config["mode"] == "rent":
            self.mode = "alquiler"
        else:
            raise ValueError(f'Not a valid mode: {config["mode"]}')

        # # Prueba para acortar los detalles de la localización (burgos>s3)
        # loc_collection = [
        #     "capiscol-gamonal",
        #     "casco-antiguo",
        #     "centro",
        #     "fuentecillas-s7-s8",
        #     "illera",
        #     "plantio-alcampo",
        #     "san-pedro-de-la-fuente",
        #     "universidad-las-huelgas",
        #     "villafria-la-ventilla-castanares",
        #     "villatoro",
        #     "villimar-v1-v2-s3-s4-san-cristobal",
        #     "yague-villalonquejar",
        #     "zona-sur-bo-cortes"
        # ]

        locations = []
        for loc in config["locations"]:
            loc_parts = loc.split(">")
            main_loc, detail_loc = loc_parts[0], None
            if len(loc_parts) == 2:
                detail_loc = loc_parts[1]
            elif len(loc_parts) > 2:
                raise ValueError(f'The location "{loc}" must contain only one ">" separator)')
            locations.append((main_loc, detail_loc))
        if locations:
            self.locations = locations
        else:
            raise ValueError(f'At least 1 location must be provided')

        house_types = []
        for house_type in config["house_types"]:
            if house_type == "new":
                house_types.append("obranueva")
            elif house_type == "used":
                house_types.append("viviendas")
            elif house_type == "terrain":
                house_types.append("terrenos")
            else:
                raise ValueError(f'Not a valid house_type: {house_type}')
        if house_types:
            self.house_types = house_types
        else:
            raise ValueError(f'At least 1 house_type must be provided')

        try:
            if int(config["max_price"]) >= 0:
                self.max_price = int(config["max_price"])
            else:
                raise ValueError(f'The price must be equals or higher than 0')
        except:
            raise TypeError(f'The price must be an integer number')

    def build_urls(self):
        urls = []
        for loc in self.locations:
            for house_type in self.house_types:
                if not loc[1]:
                    urls.append(
                        f'https://www.idealista.com/{self.mode}-{house_type}/{loc[0]}-{loc[0]}/'
                    )
                else:
                    urls.append(
                        f'https://www.idealista.com/{self.mode}-{house_type}/{loc[0]}/{loc[1]}/'
                    )

        return urls

    @staticmethod
    def add_result(data):
        with open("results.json") as json_read:
            json_results = json.load(json_read)

        site = [f'{__class__.__name__}']
        
        # regex on url to extract id
        result_id = data["url"]

        json_results[site][result_id] = data

        with open("results.json", "w+") as json_write:
            json.dump(json_results, json_write)

    def search(self):
        """API, Beautiful soup, or Selenium requests here"""

        for url in self.search_urls:
            # TODO Extraer código con requests & beautiful soup
            # TODO Quizás buscar info con NLT a parte de BS tags
            web_code = """<html>...</html>"""
            if "elemento paginación" == True:
                for page in "paginación":
                    for article in "url_page_code":
                        if filter == "ok":
                            match = {
                                "url": None,
                                "title": None,
                                "price": None,
                                "location": None,
                                "size": None,
                                "pictures": [],
                            }
                            self.add_result(match)
            else:
                for article in "url_code":
                    if filter == "ok":
                        # TODO Si pasa todos los filtros: creamos "match" y lo añadimos al json
                        match = {
                            "url": None,
                            "title": None,
                            "price": None,
                            "location": None,
                            "size": None,
                            "pictures": [],
                        }
                        self.add_result(match)
