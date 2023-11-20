import requests
from bs4 import BeautifulSoup
import csv
import json

def scrape_page(soup, quotes):
    # Recuperando todos os elementos HTML <div> de citação na página
    quote_elements = soup.find_all('div', class_='quote')

    # Iterando sobre a lista de elementos de citação
    # para extrair os dados de interesse e armazená-los
    # em quotes
    for quote_elements in quote_elements:
        # Extraindo o texto da citação
        texto = quote_elements.find('span', class_='text').text
        # Extraindo o autor da citação
        autor = quote_elements.find('small', class_='author').text

        # Extraindo os elementos HTML <a> relacionados às tags da citação
        elementos_tag = quote_elements.find('div', class_='tags').find_all('a', class_='tag')

        # Armazenando a lista de strings de tag em uma lista
        tags = [elemento_tag.text for elemento_tag in elementos_tag]

        # Adicionando um dicionário contendo os dados da citação
        # em um novo formato à lista de quotes
        quotes.append(
            {
                'text': texto,
                'author': autor,
                'tags': tags
            }
        )

# A URL da página inicial do site alvo
base_url = 'https://quotes.toscrape.com'

# Definindo o cabeçalho User-Agent para usar na solicitação GET abaixo
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

# Recuperando a página da web alvo
page = requests.get(base_url, headers=headers)

# Analisando a página da web alvo com o Beautiful Soup
soup = BeautifulSoup(page.text, 'html.parser')

# Inicializando a variável que conterá
# a lista de todos os dados de citação
quotes = []

# Raspe a página inicial
scrape_page(soup, quotes)

# Obtendo o elemento HTML "Next →"
next_li_element = soup.find('li', class_='next')

# Se houver uma próxima página
while next_li_element is not None:
    next_page_relative_url = next_li_element.find('a', href=True)['href']

    # Obtendo a nova página
    page = requests.get(base_url + next_page_relative_url, headers=headers)

    # Analisando a nova página
    soup = BeautifulSoup(page.text, 'html.parser')

    # Raspe a nova página
    scrape_page(soup, quotes)

    # Procurando o elemento HTML "Next →" na nova página
    next_li_element = soup.find('li', class_='next')

# Gravando as citações em um arquivo CSV
with open('quotes.csv', 'w', encoding='utf-8', newline='') as csv_file:
    # Inicializando o objeto de escrita para inserir dados
    # no arquivo CSV
    csv_writer = csv.writer(csv_file)

    # Escrevendo o cabeçalho do arquivo CSV
    csv_writer.writerow(['Texto', 'Autor', 'Tags'])

    # Escrevendo cada linha do CSV
    for quote in quotes:
        csv_writer.writerow(quote.values())

# Gravando as citações em um arquivo JSON
with open('quotes.json', 'w', encoding='utf-8') as json_file:
    json.dump(quotes, json_file, ensure_ascii=False, indent=2)
