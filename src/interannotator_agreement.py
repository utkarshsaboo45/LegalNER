# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 03:42:00 2022

@author: UTKARSH
"""

import json
import uuid
from collections import defaultdict


TEXT_MATCH_THRESHOLD = 100
TAGGERS_THRESHOLD = 2
REVIEWERS_THRESHOLD = 1


def extract_relevant_fields(doc):
    entities = []
    for entity in doc["annotations"][0]["result"]:
        entities.append({
            "start": entity["value"]["start"],
            "end": entity["value"]["end"],
            "span": (entity["value"]["start"], entity["value"]["end"]),
            "text": entity["value"]["text"],
            "label": entity["value"]["labels"][0]
        })
    return {
        "entities": entities,
        "text": doc["data"]["text"]
    }

    

def match_by_doc_text(text, docs):#, aligned_docs=list()):
    for doc in docs:
        if doc["text"][:TEXT_MATCH_THRESHOLD] == text[:TEXT_MATCH_THRESHOLD]:
            return doc
            # aligned_docs.append(doc)
            # return aligned_docs
    assert 1 == 2


def get_aligned_docs_list(docs_dict, annotator):
    assert len(docs_dict) > 1

    for _, docs in docs_dict.items():
        for doc_i, doc in enumerate(docs):
            docs[doc_i] = extract_relevant_fields(doc)

    aligned_docs_list = list()

    for doc_ref in docs_dict[annotator]:
        reviewed_entities = dict()

        for reviewer, docs in docs_dict.items():
            if reviewer == annotator:
                continue
            matching_doc = match_by_doc_text(doc_ref["text"], docs)
            reviewed_entities[reviewer] = matching_doc["entities"]

        assert len(reviewed_entities) == len(docs_dict) - 1

        aligned_docs_list.append({
            "doc_id": str(uuid.uuid1()),
            "text": doc_ref["text"],
            "ref_entities": doc_ref["entities"],
            "reviewed_entities": reviewed_entities
        })

    return aligned_docs_list


def get_span_list(entities):
    return [entity["span"] for entity in entities]



def calculate_inter_annotator_score(aligned_docs_list, annotator):
    total_annotated = 0
    total_correctly_annotated = 0
    total_missed = 0
    
    for aligned_doc in aligned_docs_list:
        
        spans_dict = defaultdict(set)

        for span in get_span_list(aligned_doc["ref_entities"]):
            spans_dict[span].add(annotator)

        total_annotated += len(spans_dict)

        for reviewer, reviewed_entities in aligned_doc["reviewed_entities"].items():
            for span in get_span_list(reviewed_entities):
                spans_dict[span].add(reviewer)
        for reviewers in spans_dict.values():
            if annotator in reviewers and len(reviewers) >= TAGGERS_THRESHOLD:
                total_correctly_annotated += 1
            if annotator not in reviewers and len(reviewers) >= REVIEWERS_THRESHOLD:
                total_missed += 1

    precision = total_correctly_annotated / total_annotated
    recall = total_correctly_annotated / (total_correctly_annotated + total_missed)
    f1 = 2 * precision * recall / (precision + recall)
    print(precision, recall, f1)
        
                


# def calculate_inter_annotator_score(aligned_docs_list, annotator):
#     for aligned_doc in aligned_docs_list:
#         spans_dict = defaultdict(list)
        
#         for span in get_span_list(aligned_doc["ref_entities"]):
#             spans_dict[span].append(annotator)

#         for reviewer, reviewed_entities in aligned_doc["reviewed_entities"].items():
#             for span in get_span_list(reviewed_entities):
#                 spans_dict[span].append(reviewer)
#                 if len(spans_dict[span]) > 2:
#                     print(span)
#         for reviewers in spans_dict.values():
#             if len(reviewers) != 2:
#                 print(reviewers)



if __name__ == "__main__":

    with open("data/annotations/oksana/oksana.json", encoding="utf-8") as f:
        docs_oksana = json.load(f)
    with open("data/annotations/sneha/oksana_sneha.json", encoding="utf-8") as f:
        docs_sneha = json.load(f)


    docs_dict = {
        "oksana": docs_oksana,
        "sneha": docs_sneha
    }

    aligned_docs_list = get_aligned_docs_list(docs_dict, annotator="oksana")

    calculate_inter_annotator_score(aligned_docs_list, annotator="oksana")













