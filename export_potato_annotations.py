import pandas as pd
import jsonlines
import re
import os

import argparse

def clean_text(text):
  text = re.sub(r'<.*?>', '', text)
  text = re.sub(r'\d+\.\s*', '', text)
  return text.strip()

def get_annotations(ann_path):
  annotations = []
  with jsonlines.open(ann_path) as reader:
    for line in reader:
      annotations.append(line)

  #print(ann_path, len(annotations))

  data = []

  for annotation in annotations:
    id = annotation["id"]
    paira = annotation["displayed_text"].split("<div class=\"tuple\"><b>PAIR A</b><br/>")[1].split("<br/>")
    pairb = annotation["displayed_text"].split("<div class=\"tuple\"><b>PAIR B</b><br/>")[1].split("<br/>")
    pairc = annotation["displayed_text"].split("<div class=\"tuple\"><b>PAIR C</b><br/>")[1].split("<br/>")
    paird = annotation["displayed_text"].split("<div class=\"tuple\"><b>PAIR D</b><br/>")[1].split("<br/>")
    try:
      best = list(annotation["label_annotations"]["best"].keys())[0]
    except:
      best = '-'
    try:
      worst = list(annotation["label_annotations"]["worst"].keys())[0]
    except:
      worst = '-'

    data.append(
      {
        "id": id,
        "A": f"{clean_text(paira[0])}\\n{clean_text(paira[1])}",
        "B": f"{clean_text(pairb[0])}\\n{clean_text(pairb[1])}",
        "C": f"{clean_text(pairc[0])}\\n{clean_text(pairb[1])}",
        "D": f"{clean_text(paird[0])}\\n{clean_text(paird[1])}",
        "best-pair": best,
        "worst-pair": worst
      }
    )

  return pd.DataFrame(data)

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--annotation_dir', type=str, required=True, help='path to the directory containing the annotation_output folders')
parser.add_argument('-o', '--output_file', type=str, required=True, help='path to the output file')
args = parser.parse_args()

data_dir = args.annotation_dir
anns = os.listdir(data_dir)
anns = [a for a in anns if '@' in a]
df = pd.DataFrame()

for ann in anns:
  df = pd.concat([df, get_annotations(os.path.join(data_dir, ann, 'annotated_instances.jsonl'))])

print('number of annotations', len(df))

df = df.dropna()
df = df[~df.apply(lambda row: row.str.contains('-')).any(axis=1)]
print('number of annotations after removing empty', len(df))

id_counts = df['id'].value_counts()
df = df[df['id'].map(id_counts).mod(2) == 0]
print('number of annotations after removing odds', len(df))

df.to_csv(os.path.join(args.output_file, 'processed_annotations.tsv'), sep='\t', index=False)
print('saved', len(df), 'annotations')