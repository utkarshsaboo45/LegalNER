# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 01:15:01 2022

@author: UTKARSH
"""

import re
import json
from dateutil import parser
from collections import defaultdict


ANNOTATIONS_PATH = "data/annotations_cleaned.json"
REVERSE_INDEX_PATH = "data/reverse_index.json"


def set_defaultdict():
    """A helper function which returns a defaultdict of sets"""
    return defaultdict(set)


def normalize_entity_text(entity_text):
    """
    Normalizes a piece of text by removing everything apart from alphanumeric
    and lowercases it.

    Parameters
    ----------
    entity_text : str
        Text to be normalized.

    Returns
    -------
    str
        Normalized text.

    """
    return re.sub(r"[^a-zA-Z0-9]+", "", entity_text).lower()


def build_reverse_index(documents):
    """
    Build reverse index for all the entities in all documents

    Parameters
    ----------
    documents : list
        A list of all the documents where each document is a dictionary
        containing all the tagged entities.

    Returns
    -------
    entity_docid_dict : dict
        A dictionary with keys as tags and values as dictionaries with keys as
        different "values" of those tags and values as a set of document ids in
        which those "values" are present.

    """
    entity_docid_dict = defaultdict(set_defaultdict)

    for doc in documents:
        for entity in doc["entities"]:
            if entity["label"] in ["DATE_HEARING", "DATE_JUDGEMENT"]:
                try:
                    date = str(parser.parse(entity["text"]))[:10]
                    entity_docid_dict[entity["label"]][date].add(doc["doc_id"])
                except:
                    entity_docid_dict[entity["label"]][entity["text"]].add(doc["doc_id"])
            else:
                entity_docid_dict[entity["label"]][normalize_entity_text(entity["text"])].add(doc["doc_id"])

    # Converting sets to lists to make it serializable
    for _, entity_dict in entity_docid_dict.items():
        for entity in entity_dict:
            entity_dict[entity] = list(entity_dict[entity])

    return entity_docid_dict


if __name__ == "__main__":
    with open(ANNOTATIONS_PATH, "r", encoding="utf-8") as f:
        documents = json.load(f)

    entity_docid_dict = build_reverse_index(documents)

    with open(REVERSE_INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(entity_docid_dict, f, indent=4)