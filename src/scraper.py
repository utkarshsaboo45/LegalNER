import os
import re
import time
import json
import glob
import shutil
import random
import zipfile
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

DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath("__file__")), "data")
JUDGEMENTS_FOLDER = os.path.join(DATA_FOLDER, "judgements")

# path the the json file where the urls of all cases are saved
URL_DICT_PATH = os.path.join(DATA_FOLDER, "url_dict.json")

MAX_FILES = 400
JUDGEMENT_CHARACTER_LOWER_LIMIT = 5000
JUDGEMENT_CHARACTER_UPPER_LIMIT = 20000


def log(message, echo=True):
    """
    Logs the outputs to logs.txt
    Parameters
    ----------
    message : str
        message to be logged.
    echo : boolean, optional
        prints the message to output console too if True. The default is True.
    """
    if echo:
        print(message)
    with open("logs.txt", "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")


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
    log("---Creating url dict---")
    url_dict = dict()
    for year in year_search_params:
        log(f"Fetching urls for year {year}...")
        for court in court_search_params:
            url = (
                URL_BASE
                + f"/search_judgments.aspx?obd={year}&court={court}#SearchTitle'"
            )
            page_soup = BeautifulSoup(urlopen(url), "html.parser")
            try:
                results = get_search_results_urls(page_soup)
                url_dict.update(results)
                time.sleep(1)
            except:
                log(f"Failed fetching urls from year: {year}, court: {court_search_params}.")

    log(f"Fetched {len(url_dict)} urls.")
    
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    
    with open(URL_DICT_PATH, "w", encoding="utf-8") as f:
        json.dump(url_dict, f)
    
    log("Urls saved in data/url_dict.json.")


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
            

def shuffle(src_path, subfolders=["Badr", "Oksana", "Sneha", "Utkarsh"]):
    """
    Shuffles the documents at the specified and moves them to
    specified subfolders

    Parameters
    ----------
    src_path : str
        path to the folder where documents are to be shuffled
    subfolders : list, optional
        list of subfolders among which the documents are to be randomly
        distributed. The default is ["Badr", "Oksana", "Sneha", "Utkarsh"]
    """
    filenames = glob.glob(src_path + "/*")
    random.shuffle(filenames)
    
    for i, subfolder in enumerate(subfolders):
        target_path = os.path.join(src_path, subfolder)
        
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        
        n_docs_p_person = len(filenames) // len(subfolders)
        
        for src_file in filenames[i * n_docs_p_person: (i + 1) * n_docs_p_person]:
            shutil.move(src_file, src_file.replace(src_path, target_path))
    
    log(f"Documents shuffled among {subfolders}")


# Referred stackoverflow
def zipdir(path, filename):
    """
    Creates a zip file of the specified folder

    Parameters
    ----------
    path : str
        path of the folder to be zipped.
    filename : str
        path to zip file to which the folder content is zipped.
    """
    ziph = zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)
    
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), 
                        os.path.relpath(os.path.join(root, file), 
                                        os.path.join(path, '..')))

    ziph.close()
    log("Judgements zipped.")


def merge(path_rasa, path_ls):
    """
    A helper method to merge output dictionaries from RASA and Label-Studio

    Parameters
    ----------
    path_rasa : str
        path to the RASA JSON outut file.
    path_ls : str
        path to the Label-Studio output file.

    Returns
    -------
    export_dict_list : list
        A merged list of dictionaries with all document texts and entities from
        the RASA and Label-studio JSON files.

    """
    with open(path_rasa, encoding="utf-8-sig") as f:
        dict_rasa = json.load(f)
    with open(path_ls, encoding="utf-8") as f:
        dict_ls = json.load(f)

    export_dict_list = list()

    for doc in dict_rasa["rasa_nlu_data"]["common_examples"]:
        entities = list()
        for entity in doc["entities"]:
            entities.append({
                "start": entity["start"],
                "end": entity["end"],
                "value": entity["value"],
                "entity": entity["entity"],
            })

        export_dict_list.append({
            "text": doc["text"].encode('unicode-escape').replace(b'\\\\', b'\\').decode('unicode-escape'),
            "entities": entities
        })

    for doc in dict_ls:
        entities = list()
        for entity in doc["label"]:
            entities.append({
                "start": entity["start"],
                "end": entity["end"],
                "value": entity["text"],
                "entity": entity["labels"][0],
            })

        export_dict_list.append({
            "text": doc["text"].encode('unicode-escape').decode('unicode-escape'),
            "entities": entities
        })

    return export_dict_list    
    

if __name__ == "__main__":
    if not os.path.exists(URL_DICT_PATH):
        create_url_dict(
            #year_search_params=list(range(1990, 2023))
        )

    with open(URL_DICT_PATH) as f:
        url_dict = json.load(f)
    
    file_count = 0
    
    if not os.path.exists(JUDGEMENTS_FOLDER):
        os.makedirs(JUDGEMENTS_FOLDER)
    
    for i, (case_name, case_url) in enumerate(url_dict.items()):
        if file_count == MAX_FILES:
            log(f"\nMaximum limit of {MAX_FILES} documents reached. Stopping...")
            break
        
        log(f"Fetching file {i + 1} out of {len(url_dict.items())}...")
        page_soup = BeautifulSoup(urlopen(case_url), "html.parser")
        try:
            text = re.sub("[^\S\r\n]+", " ", get_text(page_soup))
        
            if len(text) > JUDGEMENT_CHARACTER_LOWER_LIMIT and len(text) < JUDGEMENT_CHARACTER_UPPER_LIMIT:
                file_name = slugify(case_name) + ".txt"
                
                with open(os.path.join(JUDGEMENTS_FOLDER, file_name), "w", encoding="utf-8") as f:
                    f.write(text)
                
                file_count += 1
                
                log("-" * 20)
                log(f"Saved file no. {file_count} with size {len(text)}.")
                log("-" * 20)
                
                time.sleep(1)
            else:
                log(f"Skipping document with size {len(text)}...")
        except:
            log(f"Failed extracting text from document {i + 1}")
    
    shuffle(JUDGEMENTS_FOLDER)
    
    zipdir(JUDGEMENTS_FOLDER, os.path.join(DATA_FOLDER, "judgements.zip"))

    # Merge RASA and Label-Studio output jsons
    path_rasa, path_ls, merged_output_path = "f2.json", "f1.json", "merged.json"

    merged_dict_list = merge(path_rasa, path_ls)
    with open(merged_output_path, "w", encoding="utf-8-sig") as f:
        json.dump(merged_dict_list, f, indent=4)