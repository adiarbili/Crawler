from bs4 import BeautifulSoup
import requests
import csv
import sys


def request_source_code(url):
    """
    Input: url - query/link to a website.

    Description: Performs a get request with the specified url.

    Output: Source code of url as BeautifulSoup object
    """

    # create a response object via get method which consists source code of the website.
    res_obj = requests.get(url)

    # extract the source code of the website.
    source_code = res_obj.text

    # convert the source code of the website to an soup object which can find all html elements.
    return BeautifulSoup(source_code, 'html.parser')


def extract_num(exp):
    num = ""

    for dig in exp:
        if dig.isdigit():
            num += dig

    return num


def crawler(url, max_page):
    page = 0

    # file's name.
    csv_file_name = 'secondQuery.csv'

    # open file with write permission.
    csv_file = open(csv_file_name, 'w', encoding="utf-8")

    # set fields list as input for csv.Dictwriter().
    field_names = ['href', 'text', 'feedbacks_amount']

    # create writer object,
    writer = csv.DictWriter(csv_file, delimiter=',', escapechar="\\", quotechar='"', quoting=csv.QUOTE_MINIMAL,
                            doublequote=False, fieldnames=field_names)

    # write columns' titles as dictionary.
    writer.writerow({"href": "href", "text": "description", "feedbacks_amount": "feedbacks amount"})

    # create empty list in order to sort it by seller's feedback.
    sorted_list = []
    i = 1
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

                # get seller feedbacks
                item_page = request_source_code(href)
                seller_profile_href = item_page.find('a', {'id': "mbgLink"}).get('href')
                seller_profile_src_code = request_source_code(seller_profile_href)

                feedback_table = seller_profile_src_code.find('div', {'id': 'feedback_ratings'}).find_all('a')

                positive = extract_num(feedback_table[0].text)

                negative = extract_num(feedback_table[2].text)

                feedbacks_amount = int(positive) + int(negative)

                # create a data dictionary as an input to writer.writerow().
                data = dict(

                    # remove leading and trailing spaces, and convert to utf-8 format.
                    # after encoding with utf-8 we get a string of byte object, the 'b' prefix indicates it
                    # there for we decode bytes to a string again.
                    href=href.encode("utf-8").decode("utf-8").strip(),
                    text=text.encode("utf-8").decode("utf-8").strip(),
                    feedbacks_amount=feedbacks_amount)

                # append the data dictionary to sorted_list.
                sorted_list.append(data)

                print("{}. {}".format(i, data))
                i += 1
                '''
                
                if i >= 2:
                    break
                '''
            page += 1

            # get forward and backward buttons,
            foraward_backward_btns = ebay_search_results.find_all('a', {'class': 'x-pagination__control'})

            # request for the next page
            url = foraward_backward_btns[1].get('href')
        except requests.exceptions.RequestException as e:
            print("Cause of failure: {}".format(e))
            sys.exit(1)

    # create ordered list by rating descending
    sorted_list = sorted(sorted_list, key=lambda k: k['feedbacks_amount'], reverse=True)

    # write the data to csv file
    for line in sorted_list:
        writer.writerow(line)


# define a query for ebay website.
query = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw=dash+board+camera&_sacat=0"

crawler(query, 2)
