import requests
from bs4 import BeautifulSoup as Soup


def get_coffee_names(url, subpages) -> list:
    """parse landing page for coffee names for url element"""
    homepage_cards = []

    for page in subpages:
        url_string = f"{url}/{page}/varieties"
        r = requests.get(url_string).content
        s = Soup(r, 'html5lib')

        i = 0
        while True:
            try:
                card = s. \
                    body.find_all('div', recursive=False)[1]. \
                    find_all('section', recursive=False)[2]. \
                    div.div.find_all('div', recursive=False)[1]. \
                    find_all('div', recursive=False)[i]

                link = card.a.get('href')

                variety = card.h3.get_text()

                entry = {'varietal': variety, 'species': page, 'link': link}
                homepage_cards.append(entry)

                i += 1
            except IndexError:
                break
            except AttributeError:
                break
    print(homepage_cards)
    return homepage_cards


def get_coffee_info(coffee_names: list[dict]) -> dict:
    """serializes the coffee data into a structure"""
    # flatlist_coffees = [item for sublist in coffee_names.values() for item in sublist]
    # clean_coffee_list = string_methods.clean_coffee_names(flatlist_coffees)

    coffees_dict = {}

    for coffee in coffee_names:
        print(f"scraping {coffee['varietal']}: {coffee_names.index(coffee) + 1} of {len(coffee_names)}")

        url_string = coffee['link']
        r = requests.get(url_string).content
        s = Soup(r, "lxml")

        i = 0
        header_list = []
        values_list = []

        # get main body values
        while True:
            try:
                header_parse_path = s. \
                    body.find_all("div", recursive=False)[1]. \
                    find_all("section", recursive=False)[3].div.div. \
                    find_all("div", recursive=False)[i].div.span.get_text()
                values_parse_path = s. \
                    body.find_all("div", recursive=False)[1]. \
                    find_all("section", recursive=False)[3].div.div. \
                    find_all("div", recursive=False)[i]. \
                    find_all("div", recursive=False)[1].get_text()
                i += 1
                header_list.append(header_parse_path)
                values_list.append(values_parse_path)
            except IndexError:
                i = 0
                break

        # get agronomics values
        agro_values = []
        while True:
            try:
                agro_parse_path = s. \
                    body.find_all("div", recursive=False)[1]. \
                    find_all("section", recursive=False)[4].div.div.div. \
                    find_all("div", recursive=False)[i].div.get_text().strip()
                i += 1
                agro_values.append(agro_parse_path)
            except IndexError:
                i = 0
                break

        background_values = []
        while True:
            try:
                background_parse_path = s. \
                    body.find_all("div", recursive=False)[1]. \
                    find_all("section", recursive=False)[4].div. \
                    find_all("div", recursive=False)[1].div. \
                    find_all("div", recursive=False)[i].div.get_text().strip()
                i += 1
                background_values.append(background_parse_path)
            except IndexError:
                break

        coffees_dict[coffee['varietal']] = {
            'species': coffee['species'],
            'url': url_string,
            'headers': header_list,
            'values': values_list,
            'agro_headers': agro_values[::2],
            'agro_values': agro_values[1::2],
            'background_headers': background_values[::2],
            'background_values': background_values[1::2]
        }
    return coffees_dict
