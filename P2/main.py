from bs4 import BeautifulSoup
import requests
import csv
url_book = input("url de la page du livre ")
def scrap_url_book(url_request):

    response = requests.get(url_request)
    if (response.ok):
        soup = BeautifulSoup(response.content, 'html.parser')

    return soup
def scrap_Book(url_book):
        #to get the info of one book (place in another file affter and call it in the main)
        soup = scrap_url_book(url_book) 
        product_category = get_category(soup)
        product_info = soup.select('table.table') #to get all the info in the table                                 
        book_title = soup.find('h1').text
        book_product_description = soup.select('article > p ')[0].text
        for info in product_info :
            book_universal_product_code = info.select('tr > td')[0].text
            book_price = info.select('tr > td')[2].text
            book_price_tax = info.select('tr > td')[3].text
            book_availability = info.select('tr > td')[5].text
            #for the other infos create a function to clean unused data ( like the symbols in price etc)
           
        
        book_infos ={
                "product_page_url":url_book,
                "title":book_title,
                "universal_product_code": book_universal_product_code ,
                "price_including_tax": book_price_tax,
                "price_excluding_tax": book_price ,
                "number_available": book_availability,
                "product_description": book_product_description,
                "category" : product_category
                
                
                #product_page_url
                #● universal_ product_code (upc)
                #● title
                #● price_including_tax
                #● price_excluding_tax
                #● number_available
                #● product_description
                #● category
                #● review_rating
                #● image_url


                    }
        print(book_infos)
        return book_infos
        
def get_category(soup):
    category_book = soup.select('ul.breadcrumb')
    for element in category_book:
        book_category = element.select('li')[2].text
        
    

scrap_Book(url_book)