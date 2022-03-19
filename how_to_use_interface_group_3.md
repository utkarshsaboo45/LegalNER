# HOW TO USE OUR INTERFACE (GROUP 3)

- This text explains how to use the interface. It is also included in the application.

### 1. Interface

#### 1.1 How to use the search functionality?

- It is a multi-search functionality. There are multiple entities tagged in our court judgment documents like - 'Judge,' 'Appellant,' 'Respondent,' 'Counsel of the Appellant,' 'Counsel of the Respondent,' 'Court Name,' 'Citation,' 'Section,' 'Date of Judgement' and 'Date of hearing.'

- The search bar has two parts: The first part is a drop-down that lets you select the entity type and the second part is a search bar that accepts any keyword to search in that particular entity type.

- For instance, if you type 'Fisher' under the entity name 'Judge' and type 'Supreme Court' under the entity name 'Court name,' on submitting the query, our page will return all documents mentioning Judge Fisher and Supreme Court.

#### 1.2. How to interpret the results returned?

- Once you submit a successful query, you will notice a table with a few documents returned.

- The column `Matched Document` returns unique instances of the occurrence of a particular keyword for a given entity for every document.

- The column `Judgement link` takes you to the actual Court Judgement document of the match on the BC Law webpage (https://www.bclaws.gov.bc.ca) in case the user wants to know more about the case.

#### 1.3. To know more about the project

- Please refer to the 'About' section on the page for details on the project.

- Please refer to the 'Usage' section for more details on the interface usage.

### 2. Docker

1. Download `group_3_img.tar` .
2. Load the docker image using this command: `docker load < group_3_img.tar`
3. Run command `docker run -p 9999:9999 group_3_img`
4. Go to `localhost:9999` using your browser (Chrome recommended). 

**NOTE** If you are using Windows, please use `cmd.exe` or `powershell.exe` to load the docker image file. Docker does not support any other third-party terminal such as git bash. (source: [link](https://github.com/rprichard/winpty/issues/166)) 