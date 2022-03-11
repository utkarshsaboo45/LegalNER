## 1. Motivation

A significant obstacle to the broad utilization of corpora is the difficulty in gaining access to specific subsets of data and annotations relevant to particular types of search.
With that in mind, we are planning to develop a web-based interface that facilitates browsing the corpora, viewing annotations, searching for documents and annotations of interest.

## 2. Available Data

The interface will allow access to the collection of the Court of Appeal and Supreme Court judgments that consist of 102 documents with tagged named entities stored as a .json file. Annotation conventions are documented in 
[annotation_guidelines.md](https://github.ubc.ca/us45/COLX_523_group3/blob/master/milestone_2/annotation_guidelines.md). Linguistic annotations include the start and endpoints of each span, identified by a unique Named Entity label.

## 3. Functionalities of the interface

### 3.1 About project Tab

In this tab, you will obtain the overall description of our project, explaining the project motivation, data sources, annotation tools, and the process of the NE annotation.

### 3.2 Search functionality

#### Document Search 

A user can search for a specific document by typing a keyword in the text field with the document search. It will include restricting text searches to the whole word or searching for text strings. There will be a dropdown list where the user can select a field of interest: `Citation`/`Judge name`/`Respondent`/`Appellant`/`Appellant Counsel`/`Respondent Counsel`/`Date of Judgement`. A list of documents will pop up under the chosen field of interest by clicking the Submit button.
If no search criteria were provided, a list of documents sorted by the latest `Date of Judgement` would pop up.

#### Named Entities Search

After clicking on a specific document from the list of documents from the document search results, it would bring up the whole text of the document. There will be a dropdown list where the user can select a named entity from all possible entities (see [annotation_guidelines.md](https://github.ubc.ca/us45/COLX_523_group3/blob/master/milestone_2/annotation_guidelines.md)) throughout the whole document.

## 4. Plans for future improvements

As this is a preliminary plan, we can face some deviations in the process of development and enhance our interface with the following:
 - Functionalities to enable additional types of searches;
 - Display various kinds of statistical information (making it possible to search for named entities with a minimum number of occurrences in a document, etc.);
 - Data Visualization:  A graph showing the annotation statistics (e. g., number of named entities of a specific type).
