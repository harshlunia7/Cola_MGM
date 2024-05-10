# Have the video folders come inside the json object as question_ids
# make the existing question_ids as frame_question_ids
# Having direct_answers field with one answer in a list; this will be same as category
import json

def change_json_entries(json_file, vlm_split):
    try:
        # Open the JSON file
        with open(json_file, 'r') as f:
            data = json.load(f)

        data_json = []
        blip_json = {}
        ofa_json = {}

        for key, value in data.items():
            data_json.append({
                "question_id": key,
                "frame_question_ids": value["question_id"],
                "frame_image_ids": value["image_id"],
                "category": value["category"],
                "direct_answers": [value["category"]],
                "split": value["split"],
                "blip_answer": value["blip_answer"],
                "ofa_answer": value["ofa_answer"]
            })
            blip_json[f"{key}"] = value["blip_answer"][:10]
            ofa_json[f"{key}"] = value["ofa_answer"][:10]

        with open(f"./finetune_flan_jsons/sphar_custom_blip_caption_{vlm_split}-da.json", "w") as f:
            json.dump(blip_json, f, indent=4)
        
        with open(f"./finetune_flan_jsons/sphar_custom_ofa_caption_{vlm_split}-da.json", "w") as f:
            json.dump(ofa_json, f, indent=4)
        
        with open(f"./finetune_flan_jsons/sphar_custom_{vlm_split}.json", "w") as f:
            json.dump(data_json, f, indent=4)

    except Exception as e:
        print("Error:", e)
        return False

# Replace 'input.json' with the path to your JSON file
json_file = 'sphar_blip_ofa_vqa_val-da.json'
change_json_entries(json_file, "val")

