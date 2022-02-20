# POC: A plan on building corpus of Legal documents

We plan to build a corpus of legal documents with named entities tagged. Here is the brief of approach we follow:

1. We wrote a scraper that scrapes documents from the BC Courts website (https://www.bccourts.ca)
    - We fetched 400 judgement documents urls from the website and stored them as txt files.
    - Our script contains these important functions:
        - `get_search_results_urls()`: This method looks for all the hyperlinks pointing to case file pages and links them to their case names as a dictionary
        - `create_url_dict()`: This method looks for cases and their urls as per the year and court type parameters and saves them as a json file in the data folder
        - `get_paragraph_text()`: Extracts all the text in free paragraphs
        - `get_text()`: It takes in a bs4 object and converts it into text by looking for all the free text in the page
        - Other helper methods to shuffle documents for annotation among the group members, zip documents, logging, etc

2. We will use [RASA-NLU](https://rasahq.github.io/rasa-nlu-trainer) to annotate these documents with the named entities
    - Here is a list of entities we identified:
        - `COURT_NAME`
        - `PERS_APPELLANT`
        - `PERS_RESPONDENT`
        - `PERS_JUDGE`
        - `PERS_COUNS_APPEL`
        - `PERS_COUNS_RESP`
        - `DATE_HEARING`
        - `DATE_JUDGEMENT`
        - `CITATION`
        - `SECTION`

3. We also plan to annotate pronouns with the person name they refer to in the coming weeks.

4. As the last step, we will build a web interface which can be used by users to view these tagged entities discussed above.

## How to reproduce results for Milestone 1:

- Delete all the other files in the [src](https://github.ubc.ca/us45/COLX_523_group3/tree/master/src) folder excluding [scraper.py](https://github.ubc.ca/us45/COLX_523_group3/blob/master/src/scraper.py)
- Execute [scraper.py](https://github.ubc.ca/us45/COLX_523_group3/blob/master/src/scraper.py). It will fetch all the urls from the court website, save the judgements to txt files, shuffle and zip them to judgements.zip

Note: The number of files to be downloaded, restrictions (required document length range) and search criterion can be changed within [scraper.py](https://github.ubc.ca/us45/COLX_523_group3/blob/master/src/scraper.py)
