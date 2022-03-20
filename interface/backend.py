import re
import json
from dateutil import parser
from collections import defaultdict

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

import uvicorn

app = FastAPI()

# No. of characters to be displayed before and after the tagged entity
DOC_TEXT_CHARACTER_THRESHOLD = 100

# Colors to highlight entities on the frontend
MARK_COLOR = "black"
entity_color_dict = {
    "COURT_NAME": "#FFA39E",
    "PERS_APPELLANT": "#D4380D",
    "PERS_RESPONDENT": "#FFC069",
    "PERS_JUDGE": "#AD8B00",
    "PERS_COUNS_APPEL": "#D3F261",
    "PERS_COUNS_RESP": "#389E0D",
    "DATE_HEARING": "#5CDBD3",
    "DATE_JUDGEMENT": "#096DD9",
    "CITATION": "#ADC6FF",
    "SECTION": "#9254DE"
}



def read_corpus(path):
    """Given a path, open a json file and return a list of dictionaries."""
    f = open(path, encoding="utf-8")
    corpus = json.load(f)
    f.close()
    return corpus


# Load corpora and reverse index
annotations_path = "annotations_cleaned.json"
reverse_index_path = "reverse_index.json"

corpus = read_corpus(annotations_path)
reverse_index = read_corpus(reverse_index_path)


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
    keywords = keyword.split(",")
    entities = entity.split(",")
    return HTMLResponse(put_in_table(find_matching_documents(keywords, entities)))


def normalize_entity_text(entity_text, entity):
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
    if entity in ["DATE_HEARING", "DATE_JUDGEMENT"]:
        try:
            date = str(parser.parse(entity_text))[:10]
            return date
        except:
            entity_text
    else:
        return re.sub(r"[^a-zA-Z0-9]+", "", entity_text).lower()


def get_color_for_entity(entity):
    """
    Get highlight color for the entity to be displayed on frontend.

    Parameters
    ----------
    entity : str
        The entity for which the color is to be chosen.

    Returns
    -------
    str
        The highlight color for the specified entity.

    """
    try:
        return entity_color_dict[entity]
    except:
        return "#DDDDDD"


def get_document_text(text, entity_name, start, end, doc_text_char_threshold):
    """
    Fetches some text of the matched document with words around the start and end of the span of matched keyword

    Parameters
    ----------
    text : str
         Text of the matched document.
        
    entity_name : str
        Entity to be highlighed.
    
    start : int
        Start index of the entity.
        
    end : int
        End index of the entity.
        
    doc_text_char_threshold : int
        Number of characters to be displayed before and after the tagged entity.
    

    Returns
    -------
    dictionary
            matched documents

    """
    
    before_start = start - doc_text_char_threshold
    before_end = start
    after_start = end
    after_end = end + doc_text_char_threshold
    dots_before = "..."
    dots_after = "..."

    if start <= doc_text_char_threshold:
        before_start = 0
        dots_before = ""
    if end >= len(text) - doc_text_char_threshold:
        after_end = len(text)
        dots_after = ""

    return f"""
        {dots_before}{text[before_start: before_end]}
        <mark style="color: {MARK_COLOR}; background-color:{get_color_for_entity(entity_name)}">{text[start: end]}</mark>
        {text[after_start: after_end]}{dots_after}
    """


def set_defaultdict():
    """A helper function which returns a defaultdict of sets"""
    return defaultdict(set)


# Finding matching documents on the given keyword and entity/tag using reverse index
def find_matching_documents(keywords, entities):
    """
    Display a table of documents in which a particular keyword, matching a
    particular entity type occurs.

    Parameters
    ----------
    keyword : str
        A keyword to search relevant documents.
    entity_name : str
        The entity for which user requested the keyword to match with.

    Returns
    -------
    matching_documents : dict
        A defaultdict with keys as count and values as dictionaries with
        document details.

    """
    matching_documents = defaultdict(dict)
    docs_to_display_list = []

    for keyword, entity_name in zip(keywords, entities):
        keyword = normalize_entity_text(keyword, entity_name)
        docs_to_display = set()
        for entity_value in reverse_index[entity_name].keys():
            if keyword in entity_value or keyword == "":
                for rel_doc_id in reverse_index[entity_name][entity_value]:
                    if rel_doc_id in docs_to_display:
                        continue
                    else:
                        docs_to_display.add(rel_doc_id)

        docs_to_display_list.append(docs_to_display)

    merged_docs_to_display = set.intersection(*docs_to_display_list)
    count = 0

    # Extract paragraph from a matching document
    for rel_doc_id in merged_docs_to_display:
        displayed_entities = defaultdict(set_defaultdict)
        doc = corpus[rel_doc_id]
        text_match = ""
        hr = ""
        for keyword, entity_name in zip(keywords, entities):
            keyword = normalize_entity_text(keyword, entity_name)
            for entity in doc["entities"]:
                if (
                    entity["label"] == entity_name
                    and (keyword in normalize_entity_text(entity["text"], entity_name) or keyword == "")
                    and tuple(entity["span"]) not in displayed_entities[rel_doc_id]["spans"]
                    and normalize_entity_text(entity["text"], entity_name)
                    not in displayed_entities[rel_doc_id]["entities"]
                ):
                    displayed_entities[rel_doc_id]["spans"].add(tuple(entity["span"]))
                    displayed_entities[rel_doc_id]["entities"].add(
                        normalize_entity_text(entity["text"], entity_name)
                    )
                    start, end = entity["span"]
                    text_match += f"""
                        {hr}{get_document_text(
                            doc["text"], entity_name, start, end, DOC_TEXT_CHARACTER_THRESHOLD
                        )}<br>
                    """
                    hr = """<hr class="dashed">"""
        matching_documents[count]["doc_match"] = text_match
        try:
            matching_documents[count]["doc_link"] = doc["url"]
        except KeyError:
            matching_documents[count]["doc_link"] = "None"

        count += 1

    return matching_documents


def create_rows(dictionary):
    """
    Create rows from matching documents to populate data in the table

    Parameters
    ----------
    dictionary : dict
        A dictionary of all the documents that need to be displayed, where keys
        are document index and values are dictionaries with individual columns
        of the table.

    Returns
    -------
    output_html : str
        A string with formatted HTML text to insert rows in the table.

    """
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
    """
    Convert a dictionary to HTML formatted string to be used on the frontend.

    Parameters
    ----------
    doc_dict : dict
        A dictionary of all the documents that need to be displayed, where keys
        are document index and values are dictionaries with individual columns
        of the table.

    Returns
    -------
    str
        HTML formatted string to be used on the frontend.

    """
    return f"""
            <br>
            <table class="table table-hover table-striped">
                <thead>
                    <tr>
                        <th scope="col" data-field="id">#</th>
                        <th scope="col" data-field="text">Matched Documents</th>
                        <th scope="col" data-field="url">Judgement Link</th>
                    </tr>
                </thead>
                <tbody>
                    {create_rows(doc_dict)}
                </tbody>
            </table><br><br><br><br>
        """


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9999, debug=True)
