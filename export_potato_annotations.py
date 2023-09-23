import pandas as pd
import jsonlines
import re
import os

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
        "C": f"{clean_text(pairc[0])}\\n{clean_text(pairc[1])}",
        "D": f"{clean_text(paird[0])}\\n{clean_text(paird[1])}",
        "best-pair": best,
        "worst-pair": worst
      }
    )

  return pd.DataFrame(data)

data_dir = 'kinyarwanda/sem-rel/annotation_output'
anns = os.listdir(data_dir)
anns = [a for a in anns if '@' in a]
df = pd.DataFrame()

for ann in anns:
  ann_file = os.path.join(data_dir, ann, 'annotated_instances.jsonl')
  if os.path.isfile(ann_file):
    df = pd.concat([df, get_annotations(ann_file)])

print(len(df), 'annotations')

df = df.dropna()
df = df[(df['best-pair'] != '-') & (df['worst-pair'] != '-')]
print(len(df), 'after removing empty annotations')

df = df[df['best-pair'] != df['worst-pair']]
print(len(df), 'after removing annotations with the same worst and best pair')

id_counts = df['id'].value_counts()
df = df[df['id'].map(id_counts).mod(2) == 0]
print(id_counts.max(), 'maximum annotations')
print(len(df), 'number of annotations after removing odds')

df.to_csv(os.path.join(data_dir, 'kinyarwanda_annotations.tsv'), sep='\t', index=False)
print('saved', len(df), 'annotations')
