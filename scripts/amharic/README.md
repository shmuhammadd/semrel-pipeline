The relatedness tuples for ***Amahric semantic relatedness** task are generated from 9 million sentences which are collected from different news portals.

We have used the **sklearn** library, mainly from the **sklearn.metrics.pairwise** module, the `cosine_similarity` function to compute similarity. We have discarded sentences below a similarity score of less than 0.4

In this folder, we have multiple scripts. the `remove_non_amahric_sent` script is used to remove sentences that contain non-Amahric script such as numbers.


Since the similarity function took a longer time, we have split the file into manageable chunks, such as 100k sentences.

The `generate_run_sh.py` file produces lines that can be run in parallel such as the following
```
python similarity.py -i ./data/amhclean/amh_part_aa& 
python similarity.py -i ./data/amhclean/amh_part_aq&
python similarity.py -i ./data/amhclean/amh_part_bg& 

```

The `similarity.py` file performs the cosine similarity and keeps sentences if they are similar above the given threshold.
