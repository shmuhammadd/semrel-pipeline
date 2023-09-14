------------------------------------------------------------------------

## Semantic Relatedness Annotation Pipeline

### Overview

When creating a semantic relatedness dataset, randomly picking sentences from a corpus to form pairs will likely create mostly unrelated sentence pairs. Also, we want the dataset to include a wide variety of related sentences (in terms of domain, structure, relatedness score, etc). Thus, when creating sentence pairs that people will annotate for relatedness, we need to sample sentences in some clever way.
 
This repository provides a pipeline to find pairs of sentences that are likely to be semantically related in a given text, generate tuples for best-worst-scaling annotation (see https://www.saifmohammad.com/WebPages/BestWorst.html for more details), format the tuples for Label Studio annotation, process the annotations, and finally create sentence pairs with assigned scores. Please follow these guidelines to create such a file.

### Sequence of Tasks

1.  **Find a Wide Variety of Semantically Related Pairs**:
    -   The first step is to find sentences that are semantically related in a given corpus. There are many ways to achieve this, one way is lexical overlap, and here we have scripts for lexical overlap as a measure of semantic relatedness.
    -   Script: [`semantic_relatedness.py`](https://github.com/shmuhammadd/semantic_relatedness/blob/main/scripts/semantic_relatedness.py)
    -   Read the paper [What Makes Sentences Semantically Related? A Textual Relatedness Dataset and Empirical Study](https://arxiv.org/pdf/2110.04845.pdf) which motivates this shared task.
      
2.  **Generate Best-Worst-Scaling Tuples**:
    -   Once you have the semantically related sentence pairs, the next step is to generate tuples for best-worst-scaling annotation.
    -   Decide on on the N instances (sentence pairs) right at the beginning and generate 2N 4-tuples using the Best-Worst-Scaling script. Determine your N instances in one go and not add new instances later after annotation has begun.
    -   Script: [`generate-BWS-tuples.pl`](https://github.com/shmuhammadd/labelstudio-semrel-pipeline/blob/main/Best-Worst-Scaling-Scripts/generate-BWS-tuples.pl)
    -   Visit Saif Mohammad's website for more details [here](https://www.saifmohammad.com/WebPages/BestWorst.html)
    -   \[optional\] Read the paper to understand more about Best--Worst Scaling [Best--Worst Scaling More Reliable than Rating Scales: A Case Study on Sentiment Intensity Annotation](https://www.saifmohammad.com/WebDocs/BWS-reliable-ACL2017.pdf)
3.  **Format Tuples for Annotation**:
    -   With the generated tuples, you can now format them in a way that they can be uploaded for annotation.
    -   For Potato, use the Script:  [`potato_annotation_format.py`](https://github.com/shmuhammadd/semrel-pipeline/blob/main/scripts/potato_annotation_format.py)
    -   For Label Studio use the Script: [`label_studio_annotation_format.py`](https://github.com/shmuhammadd/labelstudio-semrel-pipeline/blob/main/scripts/label_studio_annotation_format.py)
    -   Use the Annotation guide [here](https://docs.google.com/document/d/1qwS9P-eRhgQw-JYMpWyOoTusBtuuxWCXEWnZZ-7LpBg/edit?usp=sharing)
    -   How much data to annotate? A few thousand instances per language are good (e.g., 3000).
    -   How many annotators? You can use multiple 2: 2 or 4 annotators
4.  **Process Annotations**:
    -   After completing the annotation in Label Studio, export the annotation in `tsv` format
    -   For Potato, after the annotation, run the following script on the server to export the formatted annotations: [`export_potato_annotations.py`](https://github.com/shmuhammadd/semrel-pipeline/blob/main/export_potato_annotations.py)
  
      
5.  **Calculate the Semantic Relatedness Pairs and Score, and the SHR score**
    -   Run the following bash script: [`process_annotations.sh`](https://github.com/shmuhammadd/semrel-pipeline/blob/main/process_annotations.sh)
    -   After running the above bash, it will generate multiple files below:
        1. Mapping between Pair and ID: `id_to_item.csv`
        2. Annotations by ID: `annotation_to_eval.csv`
        3. Semantic Relatedness PairID and Score: `pair_id-scores.csv`
        4. Semantic Relatedness Pairs and Score: `scored_annotations.tsv`
    - The Split Half Reliability Score (SHR score) will be printed on the screen.
    - Finally, the `scored_annotations.tsv` will be use for the shared task.
     
    
### Usage

#### 1. Find Semantically Related Sentences

``` bash
python semantic_relatedness.py [OPTIONS]
```

**OUTPUT**

`'data/semantic_related_pairs.tsv'` -- tsv file containing semantically related pairs.

| sentence1          | sentence2          |
|--------------------|--------------------|
| this is sentence1. | this is sentence2. |
| this is sentence3. | this is sentence4. |
| this is sentence5. | this is sentence6. |

#### 2. Generate Best-Worst-Scaling Tuples

``` bash
perl generate-BWS-tuples.pl [OPTIONS]
```

**OUTPUT**

`'data/semantic_related_pairs.tsv'` -- tsv file containing semantically related pairs. E.g.

| pair1                    | pair2                    | pair3                    | pair4                    |
|--------------------------|--------------------------|--------------------------|--------------------------|
| sentence1. \t sentence2. | sentence1. \t sentence3. | sentence1. \t sentence4. | sentence2. \t sentence3. |
| sentence3. \t sentence4. | sentence2. \t sentence4. | sentence1. \t sentence4. | sentence1. \t sentence2. |

#### 3. Format Tuples for Annotation

For label Studio:

``` bash
python label_studio_annotation_format.py -i [INPUT_TUPLES] -o [OUTPUT_PATH]
```

For Potate:

``` bash
python potato_annotation_format.py -i [INPUT_TUPLES] -o [OUTPUT_PATH]
```

Where - `INPUT_TUPLES`: Path to the tsv file containing the tuples. - `OUTPUT_PATH`: Output path for the annotation samples.

Example

``` bash
python label_studio_annotation_format.py -i data/tuples.tsv -o data/
```

**OUTPUT**

Below is an example of LabelStudio Output. 

-   `'data/label_studio_annotation_samples.tsv'` -- tsv file containing semantically related pairs ready for Label Studio upload. E.g.

| pair1a     | pair1b     | pair2a     | pair2b     | pair3a     | pair3b     | pair4a     | pair4b     |
|------------|------------|------------|------------|------------|------------|------------|------------|
| sentence1. | sentence2. | sentence1. | sentence3. | sentence1. | sentence4. | sentence2. | sentence3. |
| sentence3. | sentence4. | sentence2. | sentence4. | sentence1. | sentence4. | sentence1. | sentence2. |

Below is an example of Potato Output.

`
"<div class=""tuple""><b>PAIR A</b><br/>1. sentence1.<br/>2. sentence2 </div><br/><div class=""tuple""><b>PAIR B</b><br/>1. sentence1.  <br/>2. sentence3.</div><br/><div class=""tuple""><b>PAIR C</b><br/>1. sentence1 <br/>2.sentence4.</div><br/><div class=""tuple""><b>PAIR D</b><br/>1. sentence2.<br/>2. sentence3.</div>",tuple_1`

#### 4. Process Annotations

After annotation and you are using LabelStudio, export the annotation file files as `'.tsv'`.

After annotation, and you are using Potato, export the annotation.

Run the following script and it will generate x and y:

``` bash
python process_annotations.py -i data/exported_annotations.tsv -o data/
```

**OUTPUT**

-   `'data/id_to_item.tsv'` -- containing the sentence pairs and their IDs. E.g.

| item                                      | id  |
|-------------------------------------------|-----|
| this is sentence1. \\n this is sentence2. | 1   |
| this is sentence3. \\n this is sentence4. | 2   |
| this is sentence5. \\n this is sentence6. | 3   |

-   `'data/annotation_to_eval.tsv'` -- containing the sentence pairs (listed by IDs) and their best-pair and worst-pair annotations. E.g.

| Item1 | Item2 | Item3 | Item4 | BestItem | WorstItem |
|-------|-------|-------|-------|----------|-----------|
| 1     | 2     | 3     | 4     | 1        | 2         |
| 1     | 5     | 6     | 7     | 6        | 5         |

#### 5. Calculate Semantic Relatedness Score

``` bash
perl get-scores-from-BWS-annotations-counting.pl data/annotation_to_eval.tsv data/pairs-scores.tsv
```

**OUTPUT**

-   `'data/pairs-scores.tsv'` -- file containing the sentence pairs (listed by IDs) and their semantic relatedness scores. E.g.

| id  | score |
|-----|-------|
| 1   | 1.0   |
| 2   | 0.75  |
| 3   | 0.5   |

#### 6. Create Pairs and Scores

``` bash
python create_pair_and_scores.py -i data/id_to_item.tsv -s data/pairs-scores.tsv -o data
```

**OUTPUT**

-   `'data/scored_annotations.tsv'` -- file containing the sentence pairs (listed by IDs) and their semantic relatedness scores. E.g.

| item                                      | score |
|-------------------------------------------|-------|
| this is sentence1. \\n this is sentence2. | 1.0   |
| this is sentence3. \\n this is sentence4. | 0.75  |
| this is sentence5. \\n this is sentence6. | 0.5   |

### Note

Ensure you provide the correct paths to the scripts and data files. If you encounter any issues or have suggestions, please raise an issue or submit a pull request.

------------------------------------------------------------------------
