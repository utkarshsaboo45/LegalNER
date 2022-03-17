import numpy as np
import pandas as pd
import os
import nltk
import json
import random

from collections import defaultdict

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

import spacy
import uvicorn


nltk.download("brown")
nltk.download("universal_tagset")

from nltk.corpus import brown


app = FastAPI()
DOC_TEXT_CHARACTER_THRESHOLD = 100


def read_corpus(path):
    """Given a path, open a json file and return a list of dictionaries."""
    f = open(path, encoding="utf-8")
    corpus = json.load(f)
    f.close()
    return corpus


# Load corpora
path = "./final_annotations.json"
corpus = read_corpus(path)


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
    
    ## Why are we doing this?
    """
    if entity == "PERS_JUDGE":
        return HTMLResponse(
            put_in_table(find_matching_documents(keyword, entity))
        )
    if entity == "PERS_APPELLANT":
        return HTMLResponse(put_in_table(find_matching_documents(keyword, entity)))
    if entity == "PERS_RESPONDENT":
        return HTMLResponse(put_in_table(find_matching_documents(keyword, entity)))
    if entity == "PERS_COUNS_APPEL":
        return HTMLResponse(put_in_table(find_matching_documents(keyword, entity)))
    if entity == "PERS_COUNS_RESP":
        return HTMLResponse(put_in_table(find_matching_documents(keyword, entity)))
    if entity == "CITATION":
        return HTMLResponse(put_in_table(find_matching_documents(keyword, entity)))
    if entity == "DATE_JUDGEMENT":
        return HTMLResponse(put_in_table(find_matching_documents(keyword, entity)))
    if entity == "DATE_HEARING":
        return HTMLResponse(put_in_table(find_matching_documents(keyword, entity)))
    if entity == 'COURT_NAME':
        return HTMLResponse(put_in_table(find_matching_documents(keyword, entity)))
    """
    ## I think we can directly do this (?):
    return HTMLResponse(put_in_table(find_matching_documents(keyword, entity)))


# Finding Matching Documents on the givem Keyword and Entity/Tag
def find_matching_documents(keyword, entity_name):
    """Display the dataframe where the keyword appears on the frontend html page.
    keyword: a keyword to search documents. It can be a
    entity: a mode of search. Depending on the mode, this function calls different functions.

    """
    matching_documents = defaultdict(dict)

    # Extract paragraph from a matching document
    count = 0

    for i, doc in enumerate(corpus):
        for entity in doc["entities"]:
            if entity["label"] == entity_name:
                if keyword.lower() in entity["text"].lower():
                    start, end = entity["span"]
                    if start <= DOC_TEXT_CHARACTER_THRESHOLD:
                        matching_documents[count]["doc_match"] = doc["text"][
                            : end + DOC_TEXT_CHARACTER_THRESHOLD
                        ]
                    else:
                        matching_documents[count]["doc_match"] = (
                            f"""
                                ...{doc['text'][start - DOC_TEXT_CHARACTER_THRESHOLD: start]}
                                <mark style="color: black; background-color:pink">{doc['text'][start: end]}</mark>
                                {doc['text'][end: end + DOC_TEXT_CHARACTER_THRESHOLD]}...
                            """
                        )
                    try:
                        matching_documents[count]["doc_link"] = doc["url"]
                    except KeyError:
                        matching_documents[count]["doc_link"] = "None"

                    break
        count += 1
    return matching_documents


def create_row(dictionary):
    i = 0
    output_html = ""

    for columns in dictionary.values():
        i += 1
        output_html += "<tr>"
        output_html += f"<th scope='row'>{str(i)}</th>"
        for key, value in columns.items():
            if key == "doc_link":
                output_html += f"<td><a href={value}>View Document</a></td>"
            else:
                output_html += f"<td>{value}</td>"
        output_html += "</tr>"
    return output_html


def put_in_table(doc_dict):
    return (
        f"""
            <table class="table table-hover table-striped">
                <thead>
                    <tr>
                        <th scope="col">Doc #</th>
                        <th scope="col">Matched Documents</th>
                        <th scope="col">Link to the Document</th>
                    </tr>
                </thead>
                <tbody>
                    {create_row(doc_dict)}
                </tbody>
            </table>
        """
    )



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9999, debug=True)
