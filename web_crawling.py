import os
import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

file_handler = logging.FileHandler('crawler.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:%(message)s'))
logging.getLogger().addHandler(file_handler)

class Crawler:

    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls
        self.indexed_pages = {}

    def download_url(self, url):
        return requests.get(url).text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def save_page_to_file(self, url, html):
        # Gera um nome de arquivo baseado no URL
        filename = f'{url.replace("://", "_").replace("/", "_")}.html'
        filepath = os.path.join('indexed_pages', filename)

        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(html)

    def crawl(self, url):
        html = self.download_url(url)
        self.indexed_pages[url] = html
        self.save_page_to_file(url, html)  # Salva o conteúdo HTML da página indexada em um arquivo
        for linked_url in self.get_linked_urls(url, html):
            self.add_url_to_visit(linked_url)

    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)

if __name__ == '__main__':
    # Cria o diretório para armazenar as páginas indexadas
    os.makedirs('indexed_pages', exist_ok=True)

    crawler = Crawler(urls=['https://quotes.toscrape.com/'])
    crawler.run()

    # Agora você pode acessar o conteúdo HTML indexado das páginas usando crawler.indexed_pages
    # Exemplo: print(crawler.indexed_pages['https://quotes.toscrape.com/'])
