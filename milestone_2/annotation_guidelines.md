# Annotation Guidelines

Terminology:

Named Entity (NE) — is a name that indicates a unique entity. Entities include names of people, names of places, organizations, works, websites, etc.
An entity consists of one or more words. Any named entity must contain at least one capitalized word.

## General annotation rules

- one entity should be continuous: `Tejwant Danjou`, instead of separately `Tejwant` and `Danjou`.
- two adjacent entities must be separated. Example: "Jeana  Ventures Ltd. ("Jeana") ..." - here `Jeana` is a separate entity of the type `PERS_APPELLANT`, `Jeana  Ventures Ltd.` is a separate entity of the type `PERS_APPELLANT`.
- if the name is completely in quotation marks(e.g., "Jeana"), then highlight it without quotation marks (`Jeana` - words only). 
- if the name has a dot in it as in `Jeana  Ventures Ltd.`, then the dot **should be also included** into that entity (i.e. **not** `Jeana  Ventures Ltd` but `Jeana  Ventures Ltd.`). 
- if the name has an `'s` in it as in `Tejwant Danjou's house`, then highlight it without `'s`, i.e. `Tejwant Danjou`.
- if the name contains the word in quotation marks, then also allocate quotation marks (`Boarding school "Periwinkle"`).
- when summarizing it is very important to follow the same approaches to the selection and classification of such entities, to be attentive and meticulous.
 
## Types of Named Entities with examples and explanations

1. `COURT_NAME` - type of a court.
 
 **Examples:** `The Supreme Court of British Columbia`, `THE COUNTY COURT OF VANCOUVER`, `the Court of Appeal`, `the Supreme Court`.
 
 **Annotation remarks:** Select the court name along with the articles before its name.

2. `CITATION` - citation of the court judgment.

**Examples:** `R. v. Thompson, 2019 BCCA 1`, `Regina v. Smithers (1978) 1 S.C.R. 506`, `R. v. Lloyd, 2019 BCCA 25`, ` R. v. Lloyd , Vancouver  Registry 233735-2-C` 

**Annotation remarks:** Can occur in various patterns and all instances should be tagged. It's important to include the whole entity with an id `R. v. Lloyd, 2019 BCCA 25`, **not only** `R. v. Lloyd`

3. `DATE_HEARING` - date of hearing.

**Examples:** `November 26, 2018`.

**Annotation remarks:** Tag only once in the whole document. Date is accepted in any format.

4. `DATE_JUDGEMENT` - date of judgement. 

**Examples:** `January 2, 2019`.

**Annotation remarks:** Tag only once in the whole document. Date is accepted in any format.

5. `PERS_JUDGE` - name of a judge.

**Examples:**  `The Honourable Madam Justice D. Smith`, `SMITH J.A`, `The Honourable Mr. Justice Frank`.

**Annotation remarks:** Tag all instances of the judge name in the whole document even if a judge is not related to this court hearing and is only mentioned. Tag the judge’s full name as in `SMITH J.A`, but if there is `The Honourable Madam`, `The Honourable Mr.`, or `Justice` include them as well.

6. `PERS_APPELLANT`  - name of an appellant.

**Examples:** `A.S.`, `Director of Civil Forfeiture`, `Director`, `Faye-Ann Muriel Thompson`, `Joseph Ryan Lloyd`, `Mr. Lloyd`, `Trans Canada  Insurance Marketing Inc.`, `Fransen Insurance Services Ltd.`.

**Annotation remarks:** Tag all instances of the appellant name in the whole document. If it starts with `Ms.` or `Mr.`, they should be also included. Companies are also tagged as `PERS_APPELLANT`. If there is no surname but only `Director of Civil Forfeiture`, it should be tagged the way it is provided. And then, if it is refered in the document as `Director`, it also should be tagged. 

7. `PERS_RESPONDENT` - name of a respondent.

**Examples:** `InsureBC Underwriting Services Inc.`, `Trans Canada`, `A.S.`

**Annotation remarks:** Tag all instances of the respondent name in the whole document. The same remarks as for the tag `PERS_APPELLANT` are also applied to `PERS_RESPONDENT`.


8. `PERS_COUNS_APPEL` - name of an appellant counsel. 

**Examples:** `M.F. Welsh, Q.C.`, `L. F. de Lima`.

**Annotation remarks:** Tag only the counsel’s name and not the rest `Counsel for the Plaintiff`.

9. `PERS_COUNS_RESP` - name of a respondent counsel.

**Examples:**  `J.R. Neal`, 

**Annotation remarks:** Tag only the counsel’s name and not the rest `Counsel for the Defendant`,  `A. Huynh`.

10. `SECTION` - reference to a section of another legal document.

**Examples:** `Section 255(2) of the Criminal Code`, `Section 249(3) of the Code`, `Section 249(3) of the Code`, `Sec. 253 of CPC`, `Sec 253`, `S. 255`, `Section 253`, `s. 348(1)(b) of the Criminal Code, R.S.C. 1985, c. C-46`.

**Annotation remarks:** Select all instances of the section and tag them all.


## Data 

Each of the court judgment documents was scraped and stored as .txt file. It was cleaned from html tags and prepared for annotation during scraping, i.e. files only contain plain text.

The code that produces the data can be found in [data](https://github.ubc.ca/us45/COLX_523_group3/tree/master/src/data) 




