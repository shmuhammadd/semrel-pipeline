import os
import sys
import pandas as pd
import argparse

def get_or_assign_id(item):
  global current_id
  if item not in item_to_id:
    item_to_id[item] = current_id
    current_id += 1
  return item_to_id[item]

parser = argparse.ArgumentParser(description='Process semantic relatedness annotations from Label Studio.')
parser.add_argument('-i', '--input', required=True, type=str, help='csv or tsv file containing the annotations.')
parser.add_argument('-o', '--output', required=True, type=str, help='output directory for the processed annotations.')

args = parser.parse_args()
annotations = args.input
output_dir = args.output

# create the output directory if it does not exist
if not os.path.exists(output_dir):
  os.mkdir(output_dir)

# ensure that the input file exists and is a csv or tsv file
assert os.path.exists(annotations), 'Input file does not exist.'
assert annotations.endswith('.csv') or annotations.endswith('.tsv'), 'Input file must be a csv or tsv file.'

# read the annotations
try:
  df = pd.read_csv(annotations)
except:
  try:
    df = pd.read_csv(annotations, sep='\t')
  except:
    sys.exit('Could not read the input file. Please check the file format.')

# select the required columns
try:
  df = df[['pair1a', 'pair1b', 'pair2a', 'pair2b', 'pair3a', 'pair3b', 'pair4a', 'pair4b', 'best-pair', 'worst-pair']]
except:
  sys.exit('Could not find the required columns in the input file. Please check the file format.')

# merge the columns to form item pairs
new_data = {
    'A': df['pair1a'] + '\\n' + df['pair1b'],
    'B': df['pair2a'] + '\\n' + df['pair2b'],
    'C': df['pair3a'] + '\\n' + df['pair3b'],
    'D': df['pair4a'] + '\\n' + df['pair4b'],
    'best-pair': df['best-pair'],
    'worst-pair': df['worst-pair']
}

# create a new dataframe with the merged columns
df = pd.DataFrame(new_data)

# replace the best-pair and worst-pair labels with the actual item pairs
df['best-pair'] = df.apply(lambda row: row[row['best-pair']], axis=1)
df['worst-pair'] = df.apply(lambda row: row[row['worst-pair']], axis=1)

# rename the columns to Item1, Item2, Item3, Item4, BestItem, WorstItem
new_names = {'A': 'Item1',
             'B': 'Item2',
             'C': 'Item3',
             'D': 'Item4',
             'best-pair': 'BestItem',
             'worst-pair': 'WorstItem'}
df = df.rename(columns=new_names)

# create a dictionary to map each item to an ID
item_to_id = {}
current_id = 1

# replace each item with its ID
for col in df.columns:
  df[col] = df[col].apply(get_or_assign_id)

# save index to item mapping
id_df = pd.DataFrame(item_to_id.items(), columns=['item', 'id'])

# save the processed annotations and the index to item mapping
df.to_csv(os.path.join(output_dir, 'annotation_to_eval.csv'), index=False)
id_df.to_csv(os.path.join(output_dir, 'id_to_item.csv'), index=False)

print('saved processed files to:', os.path.join(output_dir, 'annotation_to_eval.csv'), 'and', os.path.join(output_dir, 'id_to_item.csv'))