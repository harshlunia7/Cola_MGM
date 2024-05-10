#! /bin/bash
#SBATCH -A rafaelgetto
#SBATCH -n 20
#SBATCH --partition=long
#SBATCH --mem-per-cpu=2G
#SBATCH --gres=gpu:1
#SBATCH --time=46:00:00

# conda initialization 
source /home2/rafaelgetto/miniconda3/etc/profile.d/conda.sh; 

# activate conda environment 
conda activate cola;
echo "conda environment activated";

echo "Creating ssd_scratch/cvit/rafaelgetto directory";
mkdir /ssd_scratch/cvit/rafaelgetto;
mkdir /ssd_scratch/cvit/rafaelgetto/datasets;
mkdir /ssd_scratch/cvit/rafaelgetto/predictions;
mkdir /ssd_scratch/cvit/rafaelgetto/pretrained_models;


# copy dataset to ssd_scratch 
cp -R /home2/rafaelgetto/Cola_MGM/datasets/aokvqa /ssd_scratch/cvit/rafaelgetto/datasets;
cp -R /home2/rafaelgetto/Cola_MGM/predictions/* /ssd_scratch/cvit/rafaelgetto/predictions;
echo "Dataset Copied";

echo "Starting Training";
WANDB_RUN_ID=flan_base_aok_blip_ofa_1 python query/finetune_flan.py \
--data-dir /ssd_scratch/cvit/rafaelgetto/datasets \
--dataset-name aokvqa \
--split train \
--val-split val \
--bs 4 \
--llm google/flan-t5-base \
--vlm1 blip \
--vlm2 ofa \
--prediction-out /ssd_scratch/cvit/rafaelgetto/predictions/aokvqa_cola_ft_predictions_out.json \
--include-profile \
--include-caption \
--prediction-output-dir /ssd_scratch/cvit/rafaelgetto/predictions \
--model-output-dir /ssd_scratch/cvit/rafaelgetto/pretrained_models \
--num_workers 4;

rsync -azP predictions/flan_base_aok_blip_ofa_1/epoch_29 rafaelgetto@ada.iiit.ac.in:/share3/rafaelgetto/MGM_proj/outputs/Cola_FT/aokvqa/predictions/flan_base_aok_blip_ofa_1/;
rsync -azP pretrained_models/flan_base_aok_blip_ofa_1/google/flan-t5-base_language_profile_bs4_epoch29 rafaelgetto@ada.iiit.ac.in:/share3/rafaelgetto/MGM_proj/outputs/Cola_FT/aokvqa/pretrained_models/flan_base_aok_blip_ofa_1

echo "deactivate environment";
conda deactivate; 
