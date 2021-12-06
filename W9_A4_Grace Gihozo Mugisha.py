import bs4
import requests
import sys
import time


# When a user inputs page numbers as an argument, the get data page() method lets us get the data page number for the webpage we're trying to visit.

def get_data_page(n):
    pages = 2
    if n == 0 or n > pages:
        print("Sorry, this web page only have 2 pages. You can only check books on page 1 and 2")
        sys.exit()


page = 2
get_data_page(page)

# The url variable contains the URL we're trying to collect data from.
url = f"https://www.amazon.com/gp/bestsellers/books/ref=bsm_nav_pill_print/ref=s9_acss_bw_cg_bsmpill_1c1_w?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-1&pf_rd_r=JSFR919BB1373W4FETRV&pf_rd_t=101&pf_rd_p=65e3ce24-654c-43fb-a17b-86a554348820&pf_rd_i=16857165011={page}"
# This is a sorting approach for informing everyone who is executing your program that data is on the way.
print("See top 10 book which are most expensive and popular in Amazon \n")
time.sleep(1)

try:

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 '
                      'Safari/537.36',
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate"
    }
    # Use request.get() to get web page url.
    request = requests.get(url, headers=headers, params={"wait": 1})

    #  soup object
    soup = bs4.BeautifulSoup(request.text, 'lxml')


    book_data = soup.select(".zg-item-immersion")
    # print(book_data)

    if not len(book_data):
        print("This site can’t be reached")

    # list to add all the popular books we have selected from webpage using BeautifulSoup
    popular_books = []
    # loop of popular books
    for book in book_data:
        # If we come across a book with five stars, we know it's popular
        if "a-star-5" in str(book):
            for book_names in book.select(".p13n-sc-truncate"):
                popular_books.append(book_names.getText().strip())

    # list to hold the values prices book has
    popular_books_prices = []
    for book in book_data:
        # If we come across a book with five stars, we know it's popular.
        if "a-star-5" in str(book):
            for prices in book.find(name="span", class_="p13n-sc-price"):
                popular_books_prices.append(float(prices.replace("$", "")))

    # list to hold the sorted prices book has
    sorted_top_ten_prices = []
    #Get the top 10 book prices by looping through the initial price list in popular book.
    for price in popular_books_prices:
        sorted_top_ten_prices.append(price)
    # Get the top 10 prices of books

    max_range = 10
    sorted_top_ten_prices.sort()
    sorted_top_ten_prices = sorted_top_ten_prices[-max_range:]

    # list to hold the value
    ten_most_expensive = []
    unsorted_prices = []
    # Loop of top 10 book are expensive
    for book in book_data:
        # If we come across a book with five stars, we know it's popular.
        if "a-star-5" in str(book):
            # as well as loop through the sorted top ten pricing list
            for boo in sorted_top_ten_prices:
                # if the pricing list's boo is in the string book data
                if f"${boo}" in str(book):
                    # add all of the books from the list of the ten most expensive books
                    ten_most_expensive.append((book.find(name="div", class_="p13n-sc-truncate").text.strip()))

                    for prices in book.find(name="span", class_="p13n-sc-price"):
                        unsorted_prices.append(prices)

    # USING dictionary

    finalresult = [{ten_most_expensive[j]: unsorted_prices[j] for j in range(len(ten_most_expensive))}]
    print(finalresult)

except requests.exceptions.RequestException as e:
    print("Something went wrong. Please check the URL\n", e)
