import re
import json
from dateutil import parser
from collections import defaultdict

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

import uvicorn

app = FastAPI()
DOC_TEXT_CHARACTER_THRESHOLD = 100
MARK_COLOR = "red"
MARK_BACKGROUND_COLOR = "pink"


def read_corpus(path):
    """Given a path, open a json file and return a list of dictionaries."""
    f = open(path, encoding="utf-8")
    corpus = json.load(f)
    f.close()
    return corpus


# Load corpora
annotations_path = "../../src/data/annotations_cleaned.json"
reverse_index_path = "../../src/data/reverse_index.json"

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


def get_document_text(text, start, end, doc_text_char_threshold):
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
        <mark style="color: {MARK_COLOR}; background-color:{MARK_BACKGROUND_COLOR}">{text[start: end]}</mark>
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
    displayed_docs_list = []

    for keyword, entity_name in zip(keywords, entities):
        keyword = normalize_entity_text(keyword, entity_name)
        displayed_docs = set()
        for entity_value in reverse_index[entity_name].keys():
            if keyword in entity_value:
                for rel_doc_id in reverse_index[entity_name][entity_value]:
                    if rel_doc_id in displayed_docs:
                        continue
                    else:
                        displayed_docs.add(rel_doc_id)

        displayed_docs_list.append(displayed_docs)

    merged_displayed_docs = set.intersection(*displayed_docs_list)
    count = 0

    # Extract paragraph from a matching document
    for keyword, entity_name in zip(keywords, entities):
        keyword = normalize_entity_text(keyword, entity_name)
        for rel_doc_id in merged_displayed_docs:
            displayed_entities = defaultdict(set_defaultdict)
            doc = corpus[rel_doc_id]
            text_match = ""
            hr = ""
            for entity in doc["entities"]:
                if (
                    entity["label"] == entity_name
                    and keyword in normalize_entity_text(entity["text"], entity_name)
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
                            doc["text"], start, end, DOC_TEXT_CHARACTER_THRESHOLD
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
    return f"""
            <table class="table table-hover table-striped">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Matched Documents</th>
                        <th scope="col">Judgement Link</th>
                    </tr>
                </thead>
                <tbody>
                    {create_rows(doc_dict)}
                </tbody>
            </table>
        """


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9999, debug=True)
