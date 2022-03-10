# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 14:16:24 2022

@author: UTKARSH
"""

import json
import codecs
import uuid


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
    

def rasa_to_ls(path_rasa, path_ls, username):
    """
    A helper method to convert RASA output format to Label-Studio
    compatible format and export it as a JSON file

    Parameters
    ----------
    path_rasa : str
        path to the RASA JSON input file.
    path_ls : str
        path to the Label-Studio compatible output file.

    """
    with open(path_rasa, encoding="utf-8-sig") as f:
        dict_rasa = json.load(f)

    ls_list = list()

    for doc_id, doc in enumerate(dict_rasa["rasa_nlu_data"]["common_examples"]):
        ls_dict = dict()
        ls_dict["id"] = doc_id                      # Randomly generated
        ls_dict["data"] = {"text": doc["text"]}

        results = list()

        for entity in doc["entities"]:
            value = {
                "start": entity["start"],
                "end": entity["end"],
                "text": entity["value"],
                "labels": [
                    entity["entity"]
                ]
            }

            results.append({
                "value": value,
                "id": str(uuid.uuid1())[:10],   # Randomly generated
                "from_name": "label",           # Fixed
                "to_name": "text",              # Fixed
                "type": "labels",               # Fixed
                "origin": "manual"              # Fixed
            })
        
        ls_dict["annotations"] = [{
            "id": doc_id,                                   # Randomly generated
            "created_username": username,
            "created_ago": "1 hour, 34 minutes",            # Random fixed value
            "result": results,
            "was_cancelled": False,                         # Random fixed value
            "ground_truth": False,                          # Random fixed value
            "created_at": "2022-03-02T20:40:19.456372Z",    # Random fixed value 
            "updated_at": "2022-03-02T20:40:19.456372Z",    # Random fixed value
            "lead_time": 1228.582,                          # Random fixed value
            "task": doc_id,                                 # Randomly generated
            "completed_by": 1,                              # Random fixed value
            "parent_prediction": None,                      # Random fixed value
            "parent_annotation": None                       # Random fixed value
        }]
    
        ls_dict["predictions"] = list()                     # Empty list

        ls_list.append(ls_dict)

    with codecs.open(path_ls, "w", encoding="utf-8") as f:
        json.dump(ls_list, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    # Convert RASA output to Label-Studio compatible json
    path_rasa, path_ls = "rasa.json", "label-studio.json"
    username = "Utkarsh Saboo utkarshsaboo45@gmail.com, 1"  # Random fixed value
    rasa_to_ls(path_rasa, path_ls, username)



    # # Merge RASA and Label-Studio output jsons
    # path_rasa, path_ls = "f1.json", "f2.json"
    # merged_output_path = "merged.json"

    # merged_dict_list = merge(path_rasa, path_ls)
    # with codecs.open(merged_output_path, "w", encoding="utf-8") as f:
    #     json.dump(merged_dict_list, f, indent=4, ensure_ascii=False)
    