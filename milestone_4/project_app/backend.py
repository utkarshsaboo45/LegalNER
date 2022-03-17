import json
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
    return HTMLResponse(put_in_table(find_matching_documents(keyword, entity)))


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
                    matching_documents[count]["doc_match"] = get_document_text(
                        doc["text"], start, end, DOC_TEXT_CHARACTER_THRESHOLD
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
                        <th scope="col">#</th>
                        <th scope="col">Matched Documents</th>
                        <th scope="col">Judgement Link</th>
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
