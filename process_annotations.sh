export DATA_FILE=darija/darija_annotations.tsv
export ANNOTATION_TOOL=potato
export OUTPUT_DIR=darija

python scripts/process_annotations.py \
  -i $DATA_FILE \
  -t $ANNOTATION_TOOL \
  -o $OUTPUT_DIR

perl scripts/BWS/get-scores-from-BWS-annotations-counting.pl \
  $OUTPUT_DIR/annotation_to_eval.csv \
  $OUTPUT_DIR/pair_id-scores.csv

python scripts/create_pair_and_scores.py \
  -i $OUTPUT_DIR/id_to_item.csv \
  -s $OUTPUT_DIR/pair_id-scores.csv \
  -o $OUTPUT_DIR

perl scripts/BWS/SHR-BWS.pl \
  $OUTPUT_DIR/annotation_to_eval.csv