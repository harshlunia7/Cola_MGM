<!-- # 🥤 Cola: Language Models are Visual Reasoning Coordinators -->

<div align="center">

<h2>MGM 2024 Spring: Project</br> Large Language Models are Visual Reasoning Coordinators </br> </br> Can VLMs be used on videos for action recognition?</h2>

<div align="center">
    <a href='https://www.linkedin.com/in/harsh-lunia-b913587b' target='_blank'>Harsh Lunia</a>&emsp;
   
</div>

<div align="center">
    IIIT Hyderabad
    
</div>

---

<img src="https://i.postimg.cc/ZqXSn8rN/sm-teaser.png">

<h3>TL;DR</h3>
The **COLA** (COordinative LAnguage model or visual reasoning) framework leverages a Large Language Model (LLM) to consolidate the outputs of multiple vision-language models (VLMs).

COLA demonstrates its highest efficacy when the LLM is fine-tuned, referred to as Cola-FT. In addition to performance enhancement, COLA exhibits greater resilience to errors inherent in VLMs.

To evaluate the paper's contribution, the project assesses the model's approach of aggregating VLM outputs through a LLM on the A-OKVQA dataset, albeit utilizing scaled-down versions of LLM. The results confirm the paper's assertions that an LLM serves as a superior coordinator among diverse VLMs, resulting in more accurate responses to visual questions compared to an ensemble approach.

Building upon this work, the same methodology is applied to surveillance videos for action recognition. VLMs are queried on extracted keyframes, and their outputs are subsequently processed by LLMs for final output generation. Despite the absence or minimal presence of temporal information, LLMs demonstrate reasonably effective performance, achieving an accuracy of just under 60%.

---

<p align="center">
  <a href="https://arxiv.org/abs/2310.15166" target='_blank'>[COLA Paper]</a> •
  <a href="https://cohere.com/events/c4ai-Liangyu-Chen-2023" target='_blank'>[Talk on COLA]</a> •
 

</div>

## 🍱 Environment Setup
I highly recommend you to update NVIDIA drivers and CUDA to the latest version in case of weird bugs. See `requirements.txt` for the environment where the code is tested with.

```shell
conda env create -f cola.yml
```
We use bf16 for inference and finetuning, which supports newer GPUs.

## 🥙 Prepare Datasets and Models
```shell
mkdir datasets
mkdir predictions
mkdir pretrained_models
```

Below are the datasets we tested, you don't have to download all. I suggest starting with A-OKVQA.

* A-OKVQA: download from [official page](https://allenai.org/project/a-okvqa/home)
* SPHAR: download from [Github page](https://github.com/AlexanderMelde/SPHAR-Dataset)


 All the datasets are converted to the format of A-OKVQA dataset. See `./data_utils` for conversion scripts.

```shell
datasets
├── aokvqa
├── sphar
├── coco
│   ├── train2017
│   ├── val2017
│   └── test2017
└── clevr
```

Download OFA model from Huggingface. 
```shell
cd ..
git lfs clone https://huggingface.co/OFA-Sys/ofa-large
```

## 🚀 Inference

```shell
# 1. Get the plausible answers for the validation set

python query/query_blip.py --data-dir ./datasets/ --dataset-name aokvqa --split val --vlm-task vqa --bs 8 --prediction-out ./predictions/aokvqa_blip_vqa_val-da.json --num_workers 8;

python query/query_ofa.py --vlm-model-path ../ofa-large --data-dir ./datasets/ --dataset-name aokvqa --split val --vlm-task vqa --bs 4 --prediction-out ./predictions/aokvqa_ofa_vqa_val-da.json --num_workers 4;

# 2. Get the captions for the validation set

python query/query_blip.py --data-dir ./datasets/ --dataset-name aokvqa --split val --vlm-task caption --bs 8 --prediction-out ./predictions/aokvqa_blip_caption_val-da.json --num_workers 8;

python query/query_ofa.py --vlm-model-path ../OFA-large --data-dir ./datasets/ --dataset-name aokvqa --split val --vlm-task caption --bs 4 --prediction-out ./predictions/aokvqa_ofa_caption_val-da.json --num_workers 4;


# 3. Query the language model, 

python query/query_flan.py --data-dir ./datasets/ --dataset-name aokvqa --split val --vlm-task vqa --bs 4 --prediction-out ./predictions/aokvqa_cola2-da.json --max-new-tokens 250 --llm google/flan-t5-small --vlm1 ofa --vlm2 blip --include-profile --include-caption --include-choices --incontext --num-examples 2



# 4. Evaluate the predictions
export PYTHONPATH=.
export DATA_DIR=./datasets/
export DATASET=aokvqa
export SPLIT=val
export LOG_DIR=./logs/
export PREDS_DIR=./predictions
export PT_MODEL_DIR=./pretrained_models/
export PREFIX=aokvqa_cola0

python evaluation/prepare_predictions.py \
--data-dir ${DATA_DIR} --dataset ${DATASET} \
--split ${SPLIT} \
--da ${PREDS_DIR}/${PREFIX}-da.json \
--mc ${PREDS_DIR}/${PREFIX}-mc.json \
--out ${PREDS_DIR}/${PREFIX}.json

python evaluation/eval_predictions.py \
--data-dir ${DATA_DIR} --dataset ${DATASET} \
--split ${SPLIT} \
--preds ${PREDS_DIR}/${PREFIX}.json
```

## 🎛️ Finetuning

```shell
# Get the plausible answers and captions for both training and validation sets (see Step 1 and 2 of Inference)

# 1. Finetune the language model on A-OKVQA, Cola-FT. 
WANDB_RUN_ID=aok_blip_ofa_ft python query/finetune_flan.py \
--data-dir ./datasets/ --dataset-name aokvqa --split train --val-split val \
--bs 4 --llm google/flan-t5-base --vlm1 blip --vlm2 ofa \
--prediction-out placeholder --include-profile --include-caption 

# 1. Finetune the language model on SPHAR Dataset, Cola-FT. 
WANDB_RUN_ID=aok_blip_ofa_ft python query/finetune_flan.py \
--data-dir ./datasets/ --dataset-name aokvqa --split train --val-split val \
--bs 4 --llm google/flan-t5-base --vlm1 blip --vlm2 ofa \
--prediction-out placeholder --include-profile --include-caption 

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

## Modified/New Files

```shell
├── create_confusion_matrix.py
├── evaluate.sh
├── sphar_dataset_processing/
├── action_performance_eval.py
├── query
│   ├── data.py
│   ├── finetune_flan_for_sphar.py
│   ├── query_flan.py
│   ├── query_blip_for_sphar.py
│   ├── utils.py
│   └── finetune_flan.py
└── infer_vlms.sh
```
