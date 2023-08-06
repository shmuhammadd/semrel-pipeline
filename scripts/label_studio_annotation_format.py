import os
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Create annotation samples for Label Studio.')
parser.add_argument('-i', '--tuples', required=True, type=str, help='tsv file containing the tuples.')
parser.add_argument('-o', '--output', default='', type=str, help='output path for the annotation samples.')

args = parser.parse_args()
tuples = args.tuples
output_path = args.output
col_names = ['pair1a', 'pair1b', 'pair2a', 'pair2b', 'pair3a', 'pair3b', 'pair4a', 'pair4b']

# create the output directory if it does not exist
if not os.path.exists(output_path):
  os.mkdir(output_path)

# ensure that the input file exists and is a tsv file
assert os.path.exists(tuples), 'Input file does not exist.'

# read the tuples
df = pd.read_csv(tuples, sep='\t', header=None, names=col_names)

df.to_csv(os.path.join(output_path, 'label_studio_annotation_samples.tsv'), sep='\t', index=False)

print('samples saved to:', os.path.join(output_path, 'label_studio_annotation_samples.tsv'))