import os
import time
import json
from slugify import slugify
from bs4 import BeautifulSoup
from urllib.request import urlopen

"""
This file generates the data corresponding to the search
criterion from the bccourts website.
If the search criterion is changed, the url_dict.json file 
must be deleted.
"""

URL_BASE = "https://www.bccourts.ca"
COURT_OF_APPEALS_ID = 1
SUPREME_COURT_ID = 2

DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# path the the json file where the urls of all cases are saved
URL_DICT_PATH = os.path.join(DATA_FOLDER, "url_dict.json")


def get_search_results_urls(results, base_url=URL_BASE):
    """
    Looks for all the hyperlinks pointing to
    case file pages and links them to their case
    names.

    Parameters
    ----------
    results : bs4 object
        search results bs4 object.
    base_url : str, optional
        bccourts website, by default URL_BASE

    Returns
    -------
    dict
        case names and their urls.
    """
    url_dict = dict()

    for result_tr in results.find_all("tr")[1:-2]:
        url = base_url + result_tr.find("a")["href"]
        name = result_tr.find("a").find("span").contents[0]
        url_dict[name] = url

    return url_dict


def create_url_dict(
    year_search_params=[2019, 2020, 2021, 2022],
    court_search_params=[COURT_OF_APPEALS_ID, SUPREME_COURT_ID],
):
    """
    For each parameter in the search paramters,
    looks for cases and their urls and saves them as
    a json file in the data folder.

    Parameters
    ----------
    year_search_params : list, optional
        years where the cases happened, by default [2019, 2020, 2021, 2022]
    court_search_params : list, optional
        courts where the cases happened, by default [COURT_OF_APPEALS_ID, SUPREME_COURT_ID]
    """
    url_dict = dict()
    for court in court_search_params:
        for year in year_search_params:
            url = (
                URL_BASE
                + f"/search_judgments.aspx?obd={year}&court={court}#SearchTitle'"
            )
            page_soup = BeautifulSoup(urlopen(url), "html.parser")
            results = get_search_results_urls(page_soup)
            url_dict = url_dict | results
            time.sleep(1)

    with open(URL_DICT_PATH, "w") as f:
        json.dump(url_dict, f)


def get_paragraph_text(paragraph):
    """
    Looks for all free text
    inside a paragraph.

    Parameters
    ----------
    paragraph : bs4 object
        paragraph bs4 object

    Returns
    -------
    list
        all text found in the paragraph.
    """
    text = []
    for item in paragraph.contents:
        if isinstance(item, str):
            text.append(item)
        elif hasattr(list, "__iter__"):
            text.extend(get_paragraph_text(item))
        else:
            text.extend(get_paragraph_text(item.contents))
    return text


def get_text(page_soup):
    """
    Converts a bs4 html object into
    free text by looking for all the free text
    in the page.

    Parameters
    ----------
    page_soup : bs4 object
        the webpage

    Returns
    -------
    str
        full string of the webpage.
    """
    text = []
    body = page_soup.find("body")
    for paragraph in body.find_all("p"):
        text.extend(get_paragraph_text(paragraph))
    return "\n".join(text)


if __name__ == "__main__":
    if not os.path.exists(URL_DICT_PATH):
        print("creating url dict")
        create_url_dict()

    with open(URL_DICT_PATH) as f:
        url_dict = json.load(f)

    for i, (case_name, case_url) in enumerate(url_dict.items()):
        print(f"writting file {i+1} out of {len(url_dict.items())} ...")
        page_soup = BeautifulSoup(urlopen(case_url), "html.parser")
        text = get_text(page_soup)
        file_name = slugify(case_name) + ".txt"

        with open(os.path.join(DATA_FOLDER, file_name), "w") as f:
            f.write(text)

        time.sleep(1)
