import json
import requests

from events import Author, Quote, Tag
from logger import logger

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from typing import List, Tuple
from bs4 import BeautifulSoup as bs

base_url = "https://quotes.toscrape.com"
page_url_template = base_url + "/page/{page}/"

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
              'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
}

class Scrap:

    def __init__(self, depth: int):
        self._data: List[Quote] = []
        self.depth = depth

    @staticmethod
    def parse(html):
        return bs(html, "html.parser")

    def find_elements(self, html, block, attr, multiple=False):
        """
        Универсальный метод для поиска одного или нескольких элементов
        :param html: HTML-строка или объект bs4
        :param block: Имя HTML блока
        :param attr: Словарь атрибутов для поиска
        :param multiple: Если True вернет все элементы, иначе первый элемент
        :return: Один элемент или список элементов
        """

        if isinstance(html, str):
            html = self.parse(html)

        if multiple is True:
            return html.find_all(block, attrs=attr)
        else:
            return html.find(block, attrs=attr)

    @staticmethod
    def request(url) -> str:
        """
        Выполняет запрос с обработкой исключений, для определения пропусков
        :param url: Ссылка на ресурс
        :return: Вернет содержание страницы
        """
        try:
            return requests.get(url, headers=headers).text
        except Exception as ex:
            logger.critical(ex)
            raise ex

    def get_more_info_author(self, href: str, name: str) -> Author:
        """
        Получение всей информации об авторе
        :param href: href на автора
        :param name: Имя автора
        :return Author: Вернет объект Author
        """
        logger.debug(f"Author {name} data collection process")

        html = self.request(base_url + href)
        author = Author(
            author_href=href,
            author_name=name
        )
        author.author_date = self.find_elements(html, "span", {"class": "author-born-date"}).text.strip()
        author.author_location = self.find_elements(html, "span", {"class": "author-born-location"}).text.strip()
        author.author_description = self.find_elements(html, "div", {"class": "author-description"}).text.strip()
        return author

    def process_quote(self, quote: bs) -> Quote:
        """
        Процесс сбора информации
        :param quote: Объект bs4
        :return Quote: Вернет всю информацию по цитате
        """
        logger.debug("Quote data collection process")

        quote_text = self.find_elements(quote, "span", {"class": "text"}).text.strip()
        author_name = self.find_elements(quote, "small", {"class": "author"}).text.strip()
        author_href = self.find_elements(quote, "a", {"href": True}).get("href")
        tags = [
            {"href": tag.get("href"), "name": tag.text}
            for tag in self.find_elements(quote, "a", {"class": "tag"}, multiple=True)
        ]

        _author = self.get_more_info_author(author_href, author_name)
        quote_data = Quote(
            text=quote_text,
            tags=[Tag(**tag) for tag in tags],
            author=_author
        )
        return quote_data

    def run(self):
        """
        Многопоточная сборка данных о цитатах и авторах
        :return:
        """
        logger.debug("Run scrap quotes")

        resources = [page_url_template.format(page=index) for index in range(1, self.depth + 1)]
        with ThreadPoolExecutor() as executor:

            futures = [executor.submit(self.request, url) for url in resources]
            for future in as_completed(futures):
                html = future.result()
                quotes = self.find_elements(html, "div", {"class": "quote"}, multiple=True)

                quote_futures = [executor.submit(self.process_quote, quote) for quote in quotes]
                for quote_future in as_completed(quote_futures):
                    try:
                        quote_data = quote_future.result()
                        self._data.append(quote_data)
                    except Exception as ex:
                        logger.error(f"Failed to process quote: {ex}")

    def save(self, path_to_save: str):
        """
        Сохранение результатов сбора
        :param path_to_save: Путь до файла в который сохранить результаты
        :return:
        """
        logger.debug(f"Saving results to {path_to_save}")
        with open(path_to_save, "w", encoding="utf-8") as fl:
            json.dump(
                [asdict(item) for item in self._data],
                fl,
                ensure_ascii=False,
                indent=4
            )
        logger.debug("Saved results")


if __name__ == "__main__":
    impl = Scrap(10)
    impl.run()
    impl.save("results.json")
    logger.debug("Finished app")
