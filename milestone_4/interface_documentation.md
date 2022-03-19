# Technical Interface Documentation

This file provides brief technical documentation of the project's backend and frontend.

## Requirements

To successfully run the project, one would need to have the following dependencies installed :

- Python 3.8 (or above)
- uvicorn
- fastapi
- numpy
- pandas


## 1. Backend

We have used FastAPI and Uvicorn with Python to implement the interface's backend.

### 1.1 backend.py

- This file implements the interface's functionality, using FastAPI that responds to HTTP "GET" requests from a browser. The code is broken down into functions with proper documentation

- Here are few of the main functions that we have worked on :

    -  `read_corpus()` - Given a path, open a json file and return a list of dictionaries
    -  `normalize_entity_text()` - Normalizes a piece of text by removing everything apart from alphanumeric
    and lowercases it
    -  `get_document_text()` - Fetches some text of the matched document with words around the start and end of the span
    -  `find_matching_documents()` - Display a table of documents in which a particular keyword, matching a particular entity type occurs
    
 
## 2. Frontend


### 2.1 frontend.html

- The `frontend.html` contains three forms: form, about-form, and usage-form. 

- `<form action="/about/" id="about-form">`  with  `onclick="update_about_form()"`  and  `<form action="/usage/" id="usage-form">`  with `onclick="update_usage_form()"`  invoke appropriate javascript functions. 

- When the user submits the form, `class="submit-button"` calls `update_page()`.

### 2.2 frontend.js
    
The `frontend.js` is a javascript file that communicates between the `frontend.html` and the `backend.py`. It contains the following functions:

- `insert_result()` - inserts results to the `<maintext>` section of frontend.html 
- `insert_result_container()` - inserts results to the `<container>` section of frontend.html 
- `update_page()`  - updates the Main page of the frontend interface
- `update_about_form()` - updates the About page of the frontend interface
- `update_usage_form()` - updates the Usage page of the frontend interface

### 2.3 frontend.css

The `frontend.css` takes care of the stylistic elements for all components present on the frontend.

### 2.4 about.html 

The `about.html` contains an explanation of how to use the interface.

### 2.5 usage.html

The `usage.html` introduces the project, contributors, and the mentor.
