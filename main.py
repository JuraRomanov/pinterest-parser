
import os
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import unquote


home_dir = os.getcwd()
user_name = input("Введите имя пользователя : \t").strip()


def rotate_to_dir(user_name):
    if not os.path.isdir(user_name):
        os.mkdir(user_name)
        os.chdir(user_name)
        return parser(f"https://ru.pinterest.com/{user_name}/")
    else:
        os.chdir(user_name)
        return parser(f"https://ru.pinterest.com/{user_name}/")


def dowlond_data(albome_name, url):
    soup = bs(requests.get(url).text, "html.parser")
    img = soup.find('img')

    if not os.path.isdir(albome_name):
        os.mkdir(albome_name)
        os.chdir(albome_name)

    else:
        os.chdir(albome_name)

    with open(os.path.basename(img['src']), "wb") as f:
        f.write(requests.get(img['src']).content)
    os.chdir("..")
    pass


def get_links_to_pins(url):
    soup = bs(requests.get(url).text, "html.parser")
    albums_names = soup.find_all('div', attrs={"data-test-id": "pin"})
    all_pins = [i.findAll('a', attrs={"aria-label": True})
                for i in albums_names]

    links = set()

    for div in all_pins:
        for a in div:
            links.add(f"https://ru.pinterest.com{a['href']}")

    return list(links)


def parser(url):
    print('\nНачало парсинга')
    r = requests.get(url)
    soup = bs(r.text, "html.parser")

    all_albums = list(
        filter(lambda x:  user_name in x['href'], soup.find_all('a')))
    albums_names = {}
    for i in all_albums[2:]:
        name_album = unquote(i["href"]).strip().split("/")[-2]
        albums_names[name_album] = f'https://ru.pinterest.com{i["href"]}'

    print('\nПоиск пинов ')

    links = list([get_links_to_pins(link_to_albom)
                 for album_name, link_to_albom in albums_names.items()])

    for i in range(len(links)):
        for j in range(len(links[i])):
            dowlond_data(list(albums_names.keys())[i], links[i][j-1])
        print(f'\nАльбом "{list(albums_names.keys())[i]}" скачан')

    return "\nКонец парсинга"


if __name__ == "__main__":
    print(rotate_to_dir(user_name))
