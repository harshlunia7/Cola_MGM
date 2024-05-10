import pandas as pd
import json
import os
import hashlib
import time
import uuid 
import random
def generate_unique_sequence(index):
    input_data = str(random.randint(1, 100000) + index + random.randint(1, 100000))
    hash_object = hashlib.sha256(input_data.encode())
    return hash_object.hexdigest()

def create_json(csv_file, json_file):
    json_data = []
    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_file, sep='\t', header=None, names=["video_input_path", "video_duration", "extracted_frames", "extracted_frames_location", "category"])

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        frame_names = os.listdir(row["extracted_frames_location"])
        for frame_number, frame_filename in enumerate(frame_names):
            entry = {
                "split": csv_file.split('/')[-1].split('.')[0],
                "image_id": frame_filename.split('.')[0],
                "extracted_frame_location": row["extracted_frames_location"],
                "question_id": str(uuid.uuid4()),
                "question": "What action is happening in the frame?",
                "direct_answers": [row["category"]],
                "difficult_direct_answer": False
            }
            json_data.append(entry)
    
    # Write JSON data to file
    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=4)

# Replace 'input.csv' with the path to your CSV file and 'output.json' with the desired path for your JSON file
create_json('./extracted_frames/val.txt', 'sphar_val.json')
create_json('./extracted_frames/train.txt', 'sphar_train.json')

