# Annotation Plan


## 1. Type of Annotation

We will be tagging **Named Entities** as part of annotating our corpus of legal court judgement documents. We will be tagging various entities relevant to the domain like Court Name, Appellant Name, Respondent Name, Date of hearing etc. 

## 2. Details of our Annotation Process

Input : Each court judgment document is cleaned and stored as a **.html** file *(.html is compatible with label studio)*

Output : All annotated documents will be stored as a single **.json** file with details of all tagged named entities. *(A single .json file would make it easier to handle the annotations)*

Named Entity Tags : Below are the tag names that we would be using as part of our Annotation Process. 

1) `COURT_NAME` - type of a court (the Court of Appeal, the Supreme Court, the Provincial Court)

2) `PERS_APPELLANT`  - name of an appellant (Faye-Ann Muriel Thompson)

3) `PERS_RESPONDENT` - name of a respondent (Regina)

4) `PERS_JUDGE` - name of a judge (Madam Justice D. Smith)

5) `PERS_COUNS_APPEL` - name of an appellant counsel (M.F. Welsh, Q.C.)

6) `PERS_COUNS_RESP` - name of a respondent counsel (J.R. Neal)

4) `DATE_HEARING` - date of hearing (November 26, 2018)

5) `DATE_JUDGEMENT` - date of judgement (January 2, 2019)

6) `CITATION` - citation (R. v. Thompson, 2019 BCCA 1)

7) `SECTION` - section (s. 348(1)(b) of the Criminal Code, R.S.C. 1985, c. C-46)


### 2.1 Tool to be used for Annotation

We will be using a tool called **label-studio** (https://labelstud.io) for tagging named entities in our corpus. It is an open source data-labeling tool.

### 2.2 Details of the Annotators

The team members (Badr Jaidi, Oksana Kurylo, Sneha Jhaveri, Utkarsh Saboo) will be the annotators for this project. We will be diving the corpus equally among ourselves and would be annotating the tools using the tool mentioned above. Since, the legal documents are in English, all the team members would be able to do the annotation without any issues.

### 2.3 Estimation of the Annotation Process Timeline

We aim to annotate around 100 legal documents before the next milestone. The estimated time for annotating each document is 30 minutes and since each of us will also be reviewing the annotations done by one other team member, we are also taking that time into account. 

### 2.4 Evaluation of Annotation Quality

Here are a few things we are planning to do in order to evaluate our annotation quality :

1) Each member of the group will work on annotating their assigned documents and also do a quality check of the documents annotated by every other team member in the group. This way we can ensure a thorough quality check for our annotations. Basically, every team member will annotate 25 documents and will review 75 documents.

2) In case of any conflicts during the annotation review process, we will consider the opinion of majority of the team members and go ahead with that.

3) We are also planning to overlap a few documents that we would be annotating in order to calculate the inter annotator agreement score which can help us evaluate the quality of our annotation in other documents and also understand how many entities are tagged correctly.

## 3. Pilot Study

We did a pilot study over the break where each of us annotated 2 documents and shared the resultant json files with the team. This process was really useful as there were a few of ambiguous cases where it was difficult to tag the entities and this process also helped us clear out any confusion regarding the entity tags before we annotate the remaining corpus. 
