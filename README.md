---

## Semantic Relatedness Annotation Pipeline

### Overview
This repository provides a pipeline to find semantically related sentences in a given text, generate tuples for best-worst-scaling annotation, format the tuples for Label Studio annotation, process the annotations, and finally create pairs with scores. This README will guide you through the sequence of tasks to achieve this.

### Sequence of Tasks:

1. **Find Semantically Related Sentences**: 
   - The first step is to find sentences that are semantically related in a given text. This is achieved using lexical overlap as a measure of semantic relatedness.
   - Script: [`semantic_relatedness.py`](https://github.com/shmuhammadd/semantic_relatedness/blob/main/scripts/semantic_relatedness.py)
   - Read the paper [What Makes Sentences Semantically Related? A Textual Relatedness Dataset and Empirical Study](https://arxiv.org/pdf/2110.04845.pdf) which motivates this shared task.

2. **Generate Best-Worst-Scaling Tuples**: 
   - Once you have the semantically related sentences, the next step is to generate tuples for best-worst-scaling annotation.
   - Script: [`generate-BWS-tuples.pl`](https://github.com/shmuhammadd/labelstudio-semrel-pipeline/blob/main/Best-Worst-Scaling-Scripts/generate-BWS-tuples.pl)
   - Visit Saif Mohammad's website for more details [here](https://www.saifmohammad.com/WebPages/BestWorst.html)

3. **Format Tuples for Label Studio Annotation**: 
   - With the generated tuples, you can now format them in a way that they can be uploaded to Label Studio for annotation.
   - Script: [`label_studio_annotation_format.py`](https://github.com/shmuhammadd/labelstudio-semrel-pipeline/blob/main/scripts/label_studio_annotation_format.py)
   - Ask Nedjma to add you in LabelStudio, and Shamsuddeen and Idris are happy to help configure your setup. 

4. **Process Annotations**: 
   - After completing the annotation in Label Studio, you can process the annotations using the following script.
   - Script: [`process_annotations.py`](https://github.com/shmuhammadd/labelstudio-semrel-pipeline/blob/main/scripts/process_annotations.py)

5. **Create Pairs and Scores**: 
   - The final step is to create pairs and their corresponding scores based on the processed annotations.
   - Script: [`create_pair_and_scores.py`](https://github.com/shmuhammadd/labelstudio-semrel-pipeline/blob/main/scripts/create_pair_and%20scores.py)

### Usage:

#### 1. Find Semantically Related Sentences:
```bash
python semantic_relatedness.py [OPTIONS]
```

#### 2. Generate Best-Worst-Scaling Tuples:
```bash
perl generate-BWS-tuples.pl [OPTIONS]
```

#### 3. Format Tuples for Label Studio Annotation:
```bash
python label_studio_annotation_format.py -i [INPUT_TUPLES] -o [OUTPUT_PATH]
```
Where:
- `INPUT_TUPLES`: Path to the tsv file containing the tuples.
- `OUTPUT_PATH`: Output path for the annotation samples.

Example:
```bash
python label_studio_annotation_format.py -i ./data/tuples.tsv -o ./output/
```

#### 4. Process Annotations:
```bash
python process_annotations.py [OPTIONS]
```

#### 5. Create Pairs and Scores:
```bash
python create_pair_and_scores.py [OPTIONS]
```

### Note:
Ensure you have all the required dependencies installed and always provide the correct paths to the scripts and data files.


If you encounter any issues or have suggestions, please raise an issue or submit a pull request.

---
