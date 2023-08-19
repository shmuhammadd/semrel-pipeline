The touples for ***Amahric semantic relatedness** task are generated from 9 million sentences which are collected from different news portals.

We have used the **sklearn** library, mainly from the **sklearn.metrics.pairwise** module, the `cosine_similarity` function to compute similarity. We have discarded sentences below a similarity score less than 0.4

In this folder, we hvae multiple script. the `remove_non_amahric_sent` script is used to remove sentences which contains non-Amahric script such as numbers.


Since the similarity function took longer time, we have splitted the file into manageable chunks, such as 100k sentences.

The `generate_run_sh.py` file produce lines that can be run in parallel such as the following
```
python similarity.py -i ./data/amhclean/amh_part_aa& 
python similarity.py -i.data/amhclean/amh_part_aq&
python similarity.py -i ./data/amhclean/amh_part_bg& 

```

