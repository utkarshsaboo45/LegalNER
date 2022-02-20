# Project Proposal

## 1. Motivation 

Most legal firms these days have lawyers and paralegals going through hundreds of court judgments day to day manually to fetch a few details of past cases. Many data scientists working in legal firms also require huge amounts of annotated data to be able to predict court judgments based on past court cases. Our annotated corpus of court judgment documents is a contribution to access to justice research in BC and Canada. 

## 2. Source and structure of the data

In the present work, we consider the Court of Appeal and Supreme Court Judgments. 
The collection of data will be limited to only those judgments related to tenancy/rental matters which are submitted between Jan 1, 2019 and Feb 16, 2022.

The data will be collected from the British columbia Courts website - https://www.bccourts.ca/search_judgments.aspx with the following search criteria:

**Search criteria:**

Keywords: tenant

Judgment Date: 2019/01/01 - 2022/02/16

Court Level: Court of Appeal and Supreme Court

**Structure of the data**

The court judgment documents will be scraped and stored as .txt files. There are roughly 400 text files in our dataset. On average, the mean length of each text file in our dataset is 6000 tokens.

**Terminology:**

The **Court of Appeal** is the highest court in the province. It hears appeals from the Supreme Court, from the Provincial Court on some criminal matters, and reviews and appeals from some administrative boards and tribunals.

The **Supreme Court of British Columbia** is the province's superior trial court. The Supreme Court is a court of general and inherent jurisdiction which means that it can hear any type of case, civil or criminal. It hears most appeals from the Provincial Court in civil and criminal cases and appeals from arbitration. A party may appeal a decision of the Supreme Court to the Court of Appeal.

The **Provincial Court of British Columbia** is a trial level court in British Columbia that hears cases in criminal, civil and family matters. The Provincial Court is a creation of statute, and as such its jurisdiction is limited to only those matters over which is permitted by statute

## 3. A preliminary annotation 

### 3.1 Named Entity Recognition

For Named Entity Tags, we are looking to tag the following entities:

`COURT_NAME` - type of a court (the Court of Appeal, the Supreme Court, the Provincial Court)

`PERS_APPELLANT`  - name of an appellant (Faye-Ann Muriel Thompson)

`PERS_RESPONDENT` - name of a respondent (Regina)

`PERS_JUDGE` - name of a judge (Madam Justice D. Smith)

`PERS_COUNS_APPEL` - name of an appellant counsel (M.F. Welsh, Q.C.)

`PERS_COUNS_RESP` - name of a respondent counsel (J.R. Neal)

`DATE_HEARING` - date of hearing (November 26, 2018)

`DATE_JUDGEMENT` - date of judgement (January 2, 2019)

`CITATION` - citation (R. v. Thompson, 2019 BCCA 1)

`SECTION` - section (s. 348(1)(b) of the Criminal Code, R.S.C. 1985, c. C-46)

As an annotation tool, we will be using RASA (https://rasahq.github.io/rasa-nlu-trainer/) to aid us with the entity tagging process of the documents.

### 3.2 Coreference Resolution

Coreference resolution is the task of finding all expressions that refer to the same entity in a text. Since legal documents use a lot of pronouns while discussing case proceedings referring to either the appellant , respondent or other. We would be resolving these pronouns and tagging them with their respective named entity tags.


## 4. POC: A plan on building corpus of Legal documents

We have written a python script to scrape the website mentioned above and have successfully accomplished collecting the entire corpus of 400 court judgment documents. Please refer `POC.md` for more details.