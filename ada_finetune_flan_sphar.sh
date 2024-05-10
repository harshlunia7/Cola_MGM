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


mkdir /ssd_scratch/cvit/rafaelgetto;
mkdir /ssd_scratch/cvit/rafaelgetto/pretrained_models;


echo "Starting Training";
WANDB_RUN_ID=sphar_custom_final python query/finetune_flan_for_sphar.py \
--data-dir ./datasets \
--dataset-name sphar_custom \
--split train \
--val-split val \
--bs 4 \
--llm google/flan-t5-base \
--vlm1 blip \
--vlm2 ofa \
--prediction-out ./predictions/sphar_custom_ft_predictions_out.json \
--include-caption \
--prediction-output-dir ./predictions \
--model-output-dir /ssd_scratch/cvit/rafaelgetto/pretrained_models \
--num_workers 4;

echo "deactivate environment";
conda deactivate; 
