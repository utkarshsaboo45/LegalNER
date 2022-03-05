# Corpus Description

## General

All the data was collected from the `bc courts` [website](https://www.bccourts.ca/search_judgments.aspx).
The search engine available on the website was used to filter cases by year and court and then collect the links of each case to scrap.

The data is in the `/src/data` directory, with `url_dict.json` being the list of court case urls and `judgements.zip` being the corpus itself.

## Properties

- The corpus is stored in `.txt` files inside `jugement.zip`.
- There are 400 total files.
- There are 622,868 total words.
