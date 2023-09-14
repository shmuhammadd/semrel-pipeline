while getopts a:t:o: flag
do
    case "${flag}" in
        a) annotations=${OPTARG};;
        t) tool=${OPTARG};;
        o) output=${OPTARG};;
    esac
done

export DATA_FILE=$annotations
export ANNOTATION_TOOL=$tool
export OUTPUT_DIR=$output

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