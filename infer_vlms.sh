python query/query_blip.py \
--data-dir /ssd_scratch/cvit/rafaelgetto/datasets \
--dataset-name aokvqa \
--split train \
--vlm-task caption \
--bs 8 \
--prediction-out ./predictions/aokvqa_blip_caption_train-da.json \
--num_workers 8;

python query/query_ofa.py \
--vlm-model-path ../ofa-large \
--data-dir /ssd_scratch/cvit/rafaelgetto/datasets \
--dataset-name aokvqa \
--split train \
--vlm-task vqa \
--bs 4 \
--prediction-out ./predictions/aokvqa_ofa_vqa_train-da.json \
--num_workers 4;

python query/query_ofa.py \
--vlm-model-path ../ofa-large \
--data-dir /ssd_scratch/cvit/rafaelgetto/datasets \
--dataset-name aokvqa \
--split train \
--vlm-task caption \
--bs 4 \
--prediction-out ./predictions/aokvqa_ofa_caption_train-da.json \
--num_workers 4;


