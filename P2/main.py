from bs4 import BeautifulSoup
import requests
import re
import csv
main_url = 'https://books.toscrape.com/'
url_book = input("url de la page du livre ")


def scrap_url_book(url_request):
    response = requests.get(url_request)
    if (response.ok):
        soup = BeautifulSoup(response.content, 'html.parser')

    return soup


def scrap_book(url_book):
    soup = scrap_url_book(url_book) #titre
    product_category = get_category(soup)#titre de la categorie
    img_url = soup.select('img')[0] #img
    book_img_link = main_url + img_url.get('src').strip('../../') #url de l image (pour la recuperer sur le site
    book_review_rate = scrub_review(soup)
    book_title = soup.find('h1').text
    book_product_description = soup.select('article > p ')[0].text

    product_info = soup.select('table.table')  #recup de la table pour en prendre tout les elements
    for info in product_info:
        book_universal_product_code = info.select('tr > td')[0].text
        book_price = clean_price(info.select('tr > td')[2].text)
        book_price_tax = clean_price(info.select('tr > td')[3].text)
        book_availability = clean_count(info.select('tr > td')[5].text)

        # for the other infos create a function to clean unused data ( like the symbols in price etc)

    book_infos = {
        "product_page_url": url_book,
        "universal_product_code": book_universal_product_code,
        "title": book_title,
        "price_including_tax": book_price_tax,
        "price_excluding_tax": book_price,
        "number_available": book_availability,
        "product_description": book_product_description,
        "category": product_category,
        "review_rating": book_review_rate,
        "image_url": book_img_link

        # product_page_url
        # ● universal_ product_code (upc)
        # ● title
        # ● price_including_tax
        # ● price_excluding_tax
        # ● number_available
        # ● product_description
        # ● category
        # ● review_rating
        # ● image_url

    }
    print(book_infos)
    return book_infos


def get_category(soup):
    category_book = soup.select('ul.breadcrumb')
    for element in category_book:
        book_category = element.select('li')[2].text
        return book_category


def clean_price(price):
    # clean the useless data
    price = re.sub('£', '', price)
    return price


def clean_count(nb_available):
    # cleana the useless data
    res = int(re.search(r'\d+', nb_available)[0])
    return res


def scrub_review(soup):
    ''' Conversion du rating en lettre par un chiffre '''

    review_rating_book = soup.find('p', class_='star-rating').get('class')[1]
    switcher = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5,
    }

    return switcher.get(review_rating_book, "None")


scrap_book(url_book)
