# COLX_523_group3 Milestone 2

_This is the readme file for Milestone 2 of COLX 523 Project. The files were created as per [these](https://github.ubc.ca/mds-cl-2021-22/COLX_523_adv-corp-ling_students/blob/master/milestones/milestone2.md) guidelines._

The following documents are attached as part of this milestone:

[__annotation_guidelines.md__](https://github.ubc.ca/us45/COLX_523_group3/blob/master/milestone_2/annotation_guidelines.md) - This file communicates what rules we would be following for the annotation of our corpus. It consists of the entities we identified in the documents and some general annotation rules for each of those entities.

[__annotation_plan.md__](https://github.ubc.ca/us45/COLX_523_group3/blob/master/milestone_2/annotation_plan.md) - This file includes our annotation plan with details about the annotation tool, timeline, evaluation and process.

[__corpus_analysis.md__](https://github.ubc.ca/us45/COLX_523_group3/blob/master/milestone_2/corpus_analysis.md) - This file consists of an analysis done on our corpus in comparison to other available NLTK corpus. It also includes some basic stats about our corpus files such as token count, most common words, average word count and type-to-token ratio.

[__corpus_analysis.ipynb__](https://github.ubc.ca/us45/COLX_523_group3/blob/master/milestone_2/corpus_analysis.ipynb) - This is the notebook file which was used to generate the analysis done in corpus_analysis.md.

[__scraper.py__](https://github.ubc.ca/us45/COLX_523_group3/blob/master/src/scraper.py) - This code (Python) file is a scraper to scrape judgement documents from the BC Court website. It saves urls for all the documents which match a search criteria (as defined by the user) and save them into a dictionary. It then uses that dictionary to fetch all the documents and save them as txt files, ready for annotating.

[__convert_format.py__](https://github.ubc.ca/us45/COLX_523_group3/blob/master/src/convert_format.py) - This is a helper file which we created to convert our older annotations done with RASA to the Label-Studio annotation tool format to make eveluation of annotations feasible.

## How to reproduce results for Milestone 2:

- Delete all the files/folders in the [src](https://github.ubc.ca/us45/COLX_523_group3/tree/master/src) folder excluding [scraper.py](https://github.ubc.ca/us45/COLX_523_group3/blob/master/src/scraper.py) and [url_dict.json](https://github.ubc.ca/us45/COLX_523_group3/blob/master/src/data/url_dict.json)
- Execute [scraper.py](https://github.ubc.ca/us45/COLX_523_group3/blob/master/src/scraper.py). It will fetch all the urls from the court website, save the judgements to txt files, shuffle and zip them to judgements.zip

Note: The [url_dict.json](https://github.ubc.ca/us45/COLX_523_group3/blob/master/src/data/url_dict.json) contains all the urls for documents which will be saved locally. It is recommended to fetch this again only when search parameters are updated, otherwise it can be re-used to save time and directly start with saving of the documents.

Note: The number of files to be downloaded, restrictions (required document length range) and search criterion can be changed within [scraper.py](https://github.ubc.ca/us45/COLX_523_group3/blob/master/src/scraper.py)
