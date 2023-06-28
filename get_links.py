import requests
import wikipedia


def get_random_article():
    url = "https://ru.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "list": "random",
        "rnnamespace": "0",
        "rnlimit": "1"
    }

    response = requests.get(url, params=params)
    data = response.json()
    random_page_title = data["query"]["random"][0]["title"]
    random_page_url = "https://ru.wikipedia.org/wiki/" + random_page_title.replace(" ", "_")
    random_page =[random_page_title, random_page_url]
    return random_page


def get_five_pages():
    url = "https://ru.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "list": "recentchanges",
        "rcnamespace": "0",
        "rclimit": "5"
    }

    response = requests.get(url, params=params)
    data = response.json()

    recent_changes = data["query"]["recentchanges"]
    return recent_changes


def get_five_theme_pages(theme):
    # устанавливаем язык по умолчанию
    wikipedia.set_lang("ru")

    # получаем страницы по запросу с тегом география
    pages = wikipedia.search(theme, results=5)

    # выводим ссылки и заголовки страниц
    for page in pages:
        try:
            # получаем объект страницы
            wiki_page = wikipedia.page(page)

            # выводим заголовок и ссылку
            print(wiki_page.title)
            print(wiki_page.url)
            print()
        except wikipedia.exceptions.DisambiguationError as e:
            # если страница не найдена, выводим ошибку
            print(f"Страница '{page}' не найдена.\n")
    return pages
