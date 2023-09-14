import os
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Create annotation samples for Label Studio.')
parser.add_argument('-i', '--tuples', required=True, type=str, help='tsv file containing the tuples.')
parser.add_argument('-o', '--output', default='', type=str, help='output path for the annotation samples.')

args = parser.parse_args()
tuples = args.tuples
output_path = args.output

# create the output directory if it does not exist
if not os.path.exists(output_path):
  os.mkdir(output_path)

# ensure that the input file exists and is a tsv file
assert os.path.exists(tuples), 'Input file does not exist.'

# read the tuples
df = pd.read_csv(tuples, sep='\t', header=None)

formatted_output = []
for i in range(len(df)):
  formatted_output.append(f'<div class="tuple"><b>PAIR A</b><br/>1. {df.iloc[:, 0][i]}<br/>2. {df.iloc[:, 1][i]}</div><br/>'
                          f'<div class="tuple"><b>PAIR B</b><br/>1. {df.iloc[:, 2][i]}<br/>2. {df.iloc[:, 3][i]}</div><br/>'
                          f'<div class="tuple"><b>PAIR C</b><br/>1. {df.iloc[:, 4][i]}<br/>2. {df.iloc[:, 5][i]}</div><br/>'
                          f'<div class="tuple"><b>PAIR D</b><br/>1. {df.iloc[:, 6][i]}<br/>2. {df.iloc[:, 7][i]}</div>')

new_df = pd.DataFrame()
new_df['tuple'] = formatted_output
new_df['id'] = ['tuple_' + str(i+1) for i in range(len(new_df))]

new_df.to_csv(os.path.join(output_path, 'potato_annotation_samples.csv'), index=False)

print('samples saved to:', os.path.join(output_path, 'potato_annotation_samples.csv'))