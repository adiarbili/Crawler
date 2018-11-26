from bs4 import BeautifulSoup
import requests
import csv
import sys


def request_source_code(url):
    # create a response object via get method which consists source code of the website.
    res_obj = requests.get(url)

    # extract the source code of the website.
    source_code = res_obj.text

    # convert the source code of the website to an soup object which can find all html elements.
    return BeautifulSoup(source_code, 'html.parser')


def crawler(url, max_page):
    page = 0

    # file's name.
    csv_file_name = 'firstQuery.csv'

    # open file with write permission.
    csv_file = open(csv_file_name, 'w')

    # set fields list as input for csv.Dictwriter().
    field_names = ['href', 'text', 'rating']

    # create writer object,
    writer = csv.DictWriter(csv_file, delimiter=',', quotechar='\\', quoting=csv.QUOTE_MINIMAL, doublequote=False,
                            fieldnames=field_names)

    # write columns' titles as dictionary.
    writer.writerow({"href": "href", "text": "description", "rating": "positive rating"})

    # iterate pages until max_page.
    while page < max_page:
        try:
            ebay_search_results = request_source_code(url)

            # find all the links that the search has returned.
            for link in ebay_search_results.find_all('a', {'class': "s-item__link"}):
                # get the actual link to the page.
                href = link.get('href')

                # get the description of link.
                text = link.text

                # get seller rating
                seller_page = request_source_code(href)
                inner_text_div = seller_page.find('div', {'id': "si-fb"}).text
                rating = inner_text_div.split()[0]

                # create a data dictionary as an input to writer.writerow().
                data = dict(

                    # remove leading and trailing spaces, and convert to utf-8 format.
                    # after encoding with utf-8 we get a string of byte object, the 'b' prefix indicates it
                    # there for we decode bytes to a string again.
                    href=href.encode("utf-8").decode("utf-8").strip(),
                    text=text.encode("utf-8").decode("utf-8").strip(),
                    rating=rating.encode("utf-8").decode("utf-8").strip())

                # write the data to csv file and print it.
                writer.writerow(data)
                print(data)

            page += 1

            # get forward and backward buttons,
            foraward_backward_btns = ebay_search_results.find_all('a', {'class': 'x-pagination__control'})

            # request for the next page
            url = foraward_backward_btns[1].get('href')
        except requests.exceptions.RequestException as e:
            print("Cause of failure: {}".format(e))
            sys.exit(1)


# define a query for ebay website.
query = "https://www.ebay.com/sch/i.html?_fsrp=1&_nkw=vehicle+camera+dash+board&_sacat=0" \
        "&_from=R40&rt=nc&LH_TitleDesc=0&LH_ItemCondition=3"

crawler(query, 1)
