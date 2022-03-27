# LegalNER

## Objectives

As a part of our course - Advanced Corpus Linguistics, we worked on this project with the following objectives: 
 - Collect raw data from the web
 - Carry out reliable annotations on the data to convert it to a practically useful corpus
 - Make the corpus searchable through an HTML/JavaScript frontend and Python backend, distributable using Docker

This project involved writing a scraper, manual annotation, text pre-processing, creating reverse index for entities, creating html frontend and python backend and finally hosting it on Docker

We scraped Legal Judgement documents from the BC Courts website, annotated these documents with named entities found in the data such as Court Name, Citations, Sections, etc. using [LabelStudio](https://labelstud.io/), performed inter-annotator agreement to ensure quality of annotations, and finally built a front-end with which users can interact and fetch relevant documents by searching for specific entities or raw text from the documents. By the end of this project, we had a complete pipeline ready, where we created a corpus from scratch and presented it ready-to-use to the users for applications such as Text Summarization, Question Answering, Information Extraction, etc.

## Results

Here are the results of annotations we performed: 

```
Total number of annotated entities: 5890
Total number of correctly annotated entities: 5829
Total number of missed entities: 346
Our final agreement precision: 0.99
Our final agreement recall: 0.944
Our final agreement f1-score: 0.966
```

## Usage

This section explains how to use the interface. It is also included in the web-interface.

### 1. Docker

Follow these steps in order to interact with our interface:

1. Download [`group_3_img.tar`](https://drive.google.com/file/d/1JoY8RJ8AgjT9OK9K0U6h3VdoGFgswat2/view?usp=sharing).
2. Make sure docker is running. Move to the same directory as the image file and load it by netering this in the terminal: `docker load < group_3_img.tar`
3. Start the server using this command: `docker run -d --name group_3_img -p 9999:9999 group_3_img`
4. Go to [`localhost:9999`](http://localhost:9999/) using your browser to directly access the app.

__Debugging:__

1. Although the interface generally works well with other browsers too, we recomend using Google Chrome to access it.
2. Make sure you your `9999` port isn't being blocked by any other service.
3. If the interface doesn't work, please try deleting the container and restarting docker/system.

### 2. Interface

#### 2.1 How to use the search functionality?

- It is a multi-search functionality. There are multiple entities tagged in our court judgment documents like - 'Judge,' 'Appellant,' 'Respondent,' 'Counsel of the Appellant,' 'Counsel of the Respondent,' 'Court Name,' 'Citation,' 'Section,' 'Date of Judgement' and 'Date of hearing.'
- The search bar has two parts: The first part is a drop-down that lets you select the entity type and the second part is a search bar that accepts any keyword to search in that particular entity type.
- For instance, if you type 'Fisher' under the entity name 'Judge' and type 'Supreme Court' under the entity name 'Court name,' on submitting the query, our page will return all documents mentioning Judge Fisher and Supreme Court.

#### 2.2. How to interpret the results returned?

- Once you submit a successful query, you will notice a table with a few documents returned.
- The column `Matched Document` returns unique instances of the occurrence of a particular keyword for a given entity for every document.
- The column `Judgement link` takes you to the actual Court Judgement document of the match on the [BC Law webpage](https://www.bclaws.gov.bc.ca) in case the user wants to know more about the case.

#### 2.3. To know more about the project

- Please refer to the `About` section on the page for details on the project.
- Please refer to the `Usage` section for more details on the interface usage.

### A screenshot of our deliverable interface

![interface.png](https://github.com/utkarshsaboo45/LegalNER/blob/master/interface.png)
