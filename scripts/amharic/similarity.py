import pandas as pd
import numpy as np
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from  similaritywrite import Sim

import argparse
id = 1
parser = argparse.ArgumentParser(description='Compute most similar sentences pairs with cosine similarity.')
parser.add_argument('-i', '--input', type=str, help='file containing the cleaned sentences.')
args = parser.parse_args()
file = args.input
#for file in os.listdir(PATH):
fid = []
content =[]
with open (file) as amhf:
    for line in amhf:
      if len(line.split(" ")) < 5 or len(line.strip().split(" ")) > 15:
         continue
      fid.append(id)
      content.append(line.strip())
      id += 1
print("Reading file", file, "Done")
df = pd.DataFrame({'ID':fid,'DESCRIPTION':content})
corpus = list(df["DESCRIPTION"].values)
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(list(corpus))
print("Vectoring of file", file, "Done")

head, filenam = os.path.split(file)
with open("amhsim/"+filenam,"w",encoding="utf-8") as amh:
  #Sim.similarity_write(X, corpus)
    threshold = 0.4
    for x in range(0,X.shape[0]):
        if x%1000==0:
          print(x,"X documents processed")
        for y in range(x,X.shape[0]):   
          if(x!=y):
              if(cosine_similarity(X[x],X[y])>threshold):
                amh.write(corpus[x].replace("\t","") + \
                          "\t" + corpus[y].replace("\t","") + "\t" +\
                            str(cosine_similarity(X[x],X[y])) +"\n")
    print("File", file, "Done")
