from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from collections import defaultdict
import spacy
import uvicorn
import numpy as np
import random
import json
import pandas as pd
import os
import nltk

nltk.download("brown")
nltk.download("universal_tagset")
from nltk.corpus import brown
from collections import defaultdict


app = FastAPI()


# define functions
def open_file_return_corpus(path):
    """Given a path, open a json file and return a list of dictionaries."""
    f = open(path, encoding="utf-8")
    corpus = json.load(f)
    f.close()
    return corpus


# load corpora
paths = [
    "./final_annotations.json",
]

corpus = open_file_return_corpus(paths[0])


@app.get("/")
def start():
    return FileResponse("frontend.html")


@app.get("/{filename}")
def get_file(filename):
    return FileResponse(filename)


@app.get("/about/")
def display_about():
    """Display 'about' contents on the HTML page."""
    return FileResponse("about.html")


@app.get("/usage/")
def display_usage():
    """Display 'usage' contents on the HTML page."""
    return FileResponse("usage.html")


@app.get("/corpus/")
def display_corpus(keyword, entity):
    if entity == "judge":
        entity_name = "PERS_JUDGE"
        return HTMLResponse(
            put_in_table(find_matching_documents(keyword, entity, entity_name))
        )
    if entity == "appellant":
        entity_name = "PERS_APPELLANT"
        return HTMLResponse(put_in_table(find_matching_documents(keyword, entity_name)))
    if entity == "respondent":
        entity_name = "PERS_RESPONDENT"
        return HTMLResponse(put_in_table(find_matching_documents(keyword, entity_name)))
    if entity == "couns_appel":
        entity_name = "PERS_COUNS_APPEL"
        return HTMLResponse(put_in_table(find_matching_documents(keyword, entity_name)))
    if entity == "couns_resp":
        entity_name = "PERS_COUNS_RESP"
        return HTMLResponse(put_in_table(find_matching_documents(keyword, entity_name)))
    if entity == "citation":
        entity_name = "CITATION"
        return HTMLResponse(put_in_table(find_matching_documents(keyword, entity_name)))
    if entity == "date_judgement":
        entity_name = "DATE_JUDGEMENT"
        return HTMLResponse(put_in_table(find_matching_documents(keyword, entity_name)))
    if entity == "date_hearing":
        entity_name = "DATE_HEARING"
        return HTMLResponse(put_in_table(find_matching_documents(keyword, entity_name)))


# Finding data match
def find_matching_documents(keyword, entity, entity_name):
    """Display the dataframe where the keyword appears on the frontend html page.
    keyword: a keyword to search documents. It can be a
    entity: a mode of search. Depending on the mode, this function calls different functions.

    """
    matching_documents = defaultdict(dict)
    # find a paragraph in a corpus
    count = 0
    for i, doc in enumerate(corpus):
        for entity in doc["entities"]:
            if entity["label"] == entity_name:
                if keyword.lower() in entity["text"].lower():
                    start, end = entity["span"]
                    if start <= 200:
                        matching_documents[count]["doc_match"] = doc["text"][
                            : end + 200
                        ]
                    else:
                        matching_documents[count]["doc_match"] = (
                            "..." + doc["text"][start - 200 : end + 200] + "..."
                        )
                    try:
                        matching_documents[count]["full_doc"] = doc['url']
                    except KeyError:
                        matching_documents[count]["full_doc"] = "None"

                    break
        count += 1
    return matching_documents


def create_row(dictionary):
    S = []
    i = 0
    output_str = ""
    for k in dictionary.keys():
        values = dictionary[k].values()
        S = []
        i += 1
        S.append("<tr>")
        S.append('<th scope="row">' + str(i) + "</th>")
        for value in values:
            S.append("<td>" + value + "</td>")
        S.append("</tr>")
        output_str += "".join(S)
    return output_str


def put_in_table(doc_dict):
    return (
        '<table class="table table-hover table-striped"><thead><tr><th scope="col">#</th><th scope="col">Matched Document</th><th scope="col">Link to the Document</th></tr></thead><tbody>'
        + create_row(doc_dict)
        + "</tbody></table>"
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9999, debug=True)
