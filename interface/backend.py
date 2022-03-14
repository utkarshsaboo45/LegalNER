from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from collections import defaultdict
import uvicorn
import numpy as np
import random
import json
import pandas as pd
import os

app = FastAPI()


@app.get("/")
def start():
    return FileResponse("frontend.html")

@app.get("/{filename}")
def get_file(filename):
    return FileResponse(filename)

@app.get("/about/")
def display_about():
    """
    Display 'about' contents on the HTML page.
    """
    return FileResponse("about.html")

@app.get("/usage/")
def display_usage():
    """
    Display 'usage' contents on the HTML page.
    """
    return FileResponse("usage.html")

@app.get("/corpus/")
def display_corpus(keyword, entity):
    """
    Display the dataframe where the keyword appears on the frontend html page.
    keyword: a keyword to search documents.
    entity: a named entity where to search for a keyword.
    """
    print(keyword)
    if entity == "judge":
        return HTMLResponse(create_table(get_documents_with_keyword(entity, keyword)))
    if entity == "appellant":
        return HTMLResponse("Find docs with appellant name!") # replace with: HTMLResponse(create_table(get_documents_with_keyword(entity)))
    if entity == "respondent":
        return HTMLResponse("Find docs with respondent name!")
    if entity == "couns_appel":
        return HTMLResponse("Find docs with counsel appellant name!")
    if entity == "couns_resp":
        return HTMLResponse("Find docs with counsel respondent name!")
    if entity == "citation":
        return HTMLResponse("Find docs with citation!")
    if entity == "date_judgement":
        return HTMLResponse("Find docs with date of judgement!")
    if entity == "date_hearing":
        return HTMLResponse("Find docs with date of hearing!")

def get_documents_with_keyword(entity: str, keyword: str):
    """
    Function to search for all documents that have the given keyword among provided named entity.
    keyword: a keyword to search documents.
    entity: a named entity where to search for a keyword.
    Returns
    documents: dictionary with entity type as a key, and texts of documents that have the provided entity.
    """
    documents = {}
    documents[entity] = "First document's text with NERs!"
    documents[entity[:2]] = "Second document's text with NERs!"
    return documents

def create_rows(documents: dict):
    """
    Function to create rows in the table.
    
    Returns:
    output_str: str
    """
    S = []
    i = 0
    output_str = ""
    S.append("<tr>")
    for key, value in documents.items():
        S = []
        i += 1
        S.append('<th scope="row">' + str(i) + "</td>")
        S.append('<td>' + key + '</td>')
        S.append('<td>' + value + '</td>')
        S.append("</tr>")
        output_str += "".join(S)
    return output_str

def create_table(dictionary):
    return '<table class="table table-hover table-dark"><thead><tr><th scope="col">#</th><th scope="col">Search Entity</th><th scope="col">Document</th></tr></thead>' + create_rows(dictionary) + '</table>'

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9999, debug=True)