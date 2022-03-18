# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 15:16:29 2022

@author: UTKARSH
"""

import re
import json
import uuid
import zipfile
from slugify import slugify
from interannotator_agreement import extract_relevant_fields


def get_doc_content_to_name_dict(filename):
    """
    Returns a dictionary with the first few characters of a document
    text as key and the document's name as it's value

    Parameters
    ----------
    filename : str
        Path to the zip file containing judgement documents.

    Returns
    -------
    dict_doc_content_to_name : dict
        a dictionary with keys as the first few characters of documents'
        texts and values as the documents' name.

    """
    dict_doc_content_to_name = dict()

    archive = zipfile.ZipFile(filename, 'r')

    for judgement_doc in archive.namelist():
        doc_name = judgement_doc.split("/")[-1].replace(".txt", "")
        text = archive.read(judgement_doc).decode('utf-8')
        if not "/Badr/" in judgement_doc:
            dict_doc_content_to_name[re.sub("[^\S]+", "", text)[:100].lower()] = doc_name

    return dict_doc_content_to_name


def get_un_slugify_urls_dict(filenames):
    """
    Returns a dictionary with keys as slugified filenames and values as their 
    corresponding original filenames

    Parameters
    ----------
    filenames : dict/list
        Can be a list of filenames or a dict with keys as filenames.

    Returns
    -------
    dict
        A dictionary with keys as slugified filenames and values as the 
        corresponding original filenames.

    """
    return {slugify(filename): filename for filename in urls}


def link_url_to_doc(docs, urls, dict_un_slugify_urls, dict_doc_content_to_name):
    """
    Cleans document entities and links document with their corresponding urls

    Parameters
    ----------
    docs : list
        A list of original documents where each document is a dictionary of 
        document text and its entities.
    urls : dict
        A dictionary with keys as document names and values as their
        corresponding urls.
    dict_un_slugify_urls : dict
        A dictionary with keys as slugified filenames and values as the 
        corresponding original filenames.
    dict_doc_content_to_name : TYPE
        a dictionary with keys as the first few characters of documents'
        texts and values as the documents' name.

    Returns
    -------
    cleaned_docs_with_url : dict
        A dictionary of cleaned documents where keys are unique document ids
        and values are documents which is a dictionary of document text,
        entities and link to its corresponding url.

    """
    cleaned_docs_with_url = dict()
    for doc_i, doc in enumerate(docs):
        doc = extract_relevant_fields(doc)
        doc_few_chars = re.sub("[^\S]+", "", doc["text"])[:100].lower()
        try:
            doc_name = dict_doc_content_to_name[doc_few_chars]
            doc_url = urls[dict_un_slugify_urls[doc_name]]
            doc["url"] = doc_url
        except:
            print("Failed to extract from", doc_few_chars[:30])
        cleaned_docs_with_url[str(uuid.uuid1())] = doc
    return cleaned_docs_with_url
    

if __name__ == "__main__":
    with open("data/annotations.json", "r", encoding="utf-8") as f:
        docs = json.load(f)
    with open("data/url_dict.json", "r", encoding="utf-8") as f:
        urls = json.load(f)

    dict_doc_content_to_name = get_doc_content_to_name_dict("data/judgements.zip")
    dict_un_slugify_urls = get_un_slugify_urls_dict(urls)
    docs_with_urls = link_url_to_doc(
        docs,
        urls,
        dict_un_slugify_urls,
        dict_doc_content_to_name
    )

    with open("data/annotations_cleaned.json", "w", encoding="utf-8") as f:
        json.dump(docs_with_urls, f, indent=4)
    print("Saved cleaned annotations!")
    
    
    
    
    
    
    
    