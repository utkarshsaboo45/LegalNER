# Interannotator Agreement Study

## Agreement score

We calculated several agreement scores for our annotation. Here is a brief on what agreement scores we obtained:

```
S score : 0.9470038574679591
pi score : 0.9366619900370948
K score : 0.9371439741077994
Alpha score : 0.9360954383660536
```

As a bonus, we also calculated precision, recall and f1 measure for our annotations, the details of which can be found [here](https://github.ubc.ca/us45/COLX_523_group3/blob/utkarsh/milestone_3/Interannotator-agreement.pdf). We obtained the following results:

```
Total number of annotated entities: 5890
Total number of correctly annotated entities: 5829
Total number of missed entities: 346
Our final agreement precision: 0.99
Our final agreement recall: 0.944
Our final agreement f1-score: 0.966
```

The reason for that is that we consider that all our tags are equal, but at the same time, the tags are not equally distributed, but we assume that since we have a big sample size of randomly sampled similar documents shared between annotators, the distribution of the tags will be similar for each annotator.

### Results

We got a pi score of: `0.94`, which is pretty high!
The tags follows patterns which are unambiguous most of the time and when they aren't, we discuss them.
Sometimes, there are some ambiguities and those deffinitely are a reason for a lowered score. 
They other reason is human error, we had lots of documents to tag and some of us deffinitively didn't make the perfect choice each time.
