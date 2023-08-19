import os
import re
# Source path
PATHORIG ="./data/amh/"
# Path to save cleaned file
PATHCLEAN ="./data/amhclean/"
for file in os.listdir(PATHORIG):
  with open(PATHCLEAN+file,"w") as amhw:
    with open (PATHORIG+file) as amhr:
        for line in amhr:
            val = re.search('[a-zA-Z]+',line.strip())
            if val:
                continue
            else:
               amhw.write(line.strip() +"\n")
