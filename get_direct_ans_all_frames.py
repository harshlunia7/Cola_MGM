import json

def infuse_answers(json_file, answer_json, vlm_model):
    try:
        # Open the JSON file
        with open(answer_json, 'r') as f:
            data = json.load(f)
        
        # Create a dictionary to store entries grouped by extracted_frame_location
        with open(json_file, 'r') as f:
            grouped_entries = json.load(f)

        # Iterate over each entry in the JSON data
        for question_id, vlm_answer in data.items():
            for entry in grouped_entries.values():
                if question_id in entry["question_id"]:
                    if f"{vlm_model}_answer" not in entry:
                        entry[f"{vlm_model}_answer"] = [""] * len(entry["question_id"])
                        entry[f"{vlm_model}_answer"][entry["question_id"].index(question_id)] = vlm_answer
                    else:
                        entry[f"{vlm_model}_answer"][entry["question_id"].index(question_id)] = vlm_answer
        return grouped_entries
    
    except Exception as e:
        print("Error:", e)
        return None

input_json_file = 'sphar_blip_ofa_vqa_train_answers.json'
output_json_file = f"sphar_blip_ofa_vqa_train_answers.json"

answer_json = 'sphar_ofa_vqa_train-da.json'
vlm_model = answer_json.split("_")[1]

grouped_entries = infuse_answers(input_json_file, answer_json, vlm_model)

if grouped_entries is not None:
    print("Entries grouped by extracted_frame_location:")
    with open(output_json_file, 'w') as f:
        json.dump(grouped_entries, f, indent=4)
else:
    print("Failed to group entries.")
