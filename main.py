import random
from pprint import pprint

from bs4 import BeautifulSoup
import requests
import time
import multiprocessing
import os
import json
import datetime

bad_names = ["sample", "test"]
DELAY = 3


def pattern_generation_engine(url_, start_, limit_):
    print(f'Hi, {url_}')  # Press Ctrl+F8 to toggle the breakpoint.


def log_in(url_, payload, session_):
    cookies = {
        "firsthelp": "true",
        "PHPSESSID": "8ddvjh4t419uhf7idjr1v6fdm1",
        "cookie_consent_user_accepted": "true",
        "firstvisithelp": "true",
        "hcmnotes": "true",
        "tos_accepted": "2017-07-29 09:00:00",
        "treechoice": "view1",
        "disablehealth": "yes",
        "_pk_ref.1.0eb5": "%5B%22%22%2C%22%22%2C1699624013%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D",
        "_pk_ses.1.0eb5": "1",
        "cookie_consent_level": "%7B%22strictly-necessary%22%3Atrue%2C%22functionality%22%3Atrue%2C%22tracking%22%3Atrue%2C%22targeting%22%3Atrue%7D",
        "_pk_id.1.0eb5": "d02e0bfada32158f.1697198598.5.1699627005.1699624013."
    }
    p = session_.post(url_, data=payload, headers={"User-Agent": "Mozilla/5.0"})
    # print(f"Log in: \n"
    #      f"{p.text}")


def search_engine(url_, start_, limit_):
    # Use for entering of pages, and starting crawling on open page
    misses_list = []
    with requests.Session() as s:
        payload = {
            "txtemail": "info@plemennakniha.sk",
            "txtupass": "&vBT3vmpc",
            "btn-login": ""
        }
        url__ = url_ + "login.php"
        log_in(url__, payload, s)
        cats = list()
        cons_misses = 0
        cons_missess = 0
        for patt in range(900, 1000):
            prev_len = len(cats)
            add_str = str(patt)
            if (patt < 100):
                while len(add_str) < 3:
                    add_str = "0" + add_str

            full_url = url_ + f"search.php?regnr={add_str}&catname=&catfullname=#"
            crawler_engine(s, full_url, cats)
            time.sleep(random.randint(0, DELAY))

            now_len = len(cats)
            print(f"From {full_url} we got: {now_len - prev_len}")
            if (now_len - prev_len == 0):
                cons_misses += 1
                misses_list.append(patt)
            else:
                cons_misses = 0
            if (cons_misses > 100):
                print(f"We got 100 misses, so we are done for today, we stopeed at {patt}.")
                break
        # transformer_engine(cats)
        save_cat(cats)
        print(misses_list)


def transformer_engine(proto_cat_json):
    # Use for first tranformation of taken data, such as trimm too much spaces, etc.
    print(f'Hi')  # Press Ctrl+F8 to toggle the breakpoint


def crawler_engine(session_, url_, allCats):
    # Use a for saving htm of opened page, and scraping target data
    try:
        akt_req = session_.get(url_, headers={"User-Agent": "Mozilla/5.0"})

        soup = BeautifulSoup(akt_req.text, 'html.parser')

        first_table = soup.find('div', class_="container-fluid")
        if first_table is None:
            print(f"Table is empty in : {url_}")
            return

        for all_finds in first_table.findAll('div', class_="col-md-12 col-sm-12 col-xs-12"):
            # print(f"\n\n\n4")
            cat = dict()
            table = all_finds.find('table', attrs={"border": "1"})
            if table is None:
                break
            for i in table.findAll('table', class_="sub"):
                i.replaceWith('')
            table.find('button', class_="btn btn-primary btn-sm pull-right addmate").replaceWith()

            for row in table.findAll('tr'):
                # print(f"5, {row}")
                key = row.th.text.strip().lower()
                if (key == "coi:"):
                    break
                cat[key] = row.td.get_text().strip()
                # print(f"Cat: {key}, {cat[key]}")

            allCats.append(cat)

    except Exception as e:
        print(f"Failed to fetch {url_}: {str(e)}")


def save_cat(cats_list):
    print("Total cats: " + str(len(cats_list)))

    currentDateTime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    fileName = f"cats_{currentDateTime}.json"

    with open(fileName, 'w', encoding='utf-8') as outfile:
        json.dump(cats_list, outfile, indent=4, ensure_ascii=False)
    print(f"Saved to {fileName}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url = "https://www.bengal-data.com/"
    search_engine(url, 60000, 10000)
