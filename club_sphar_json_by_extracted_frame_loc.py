import json

def group_entries_by_location(json_file):
    try:
        # Open the JSON file
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Create a dictionary to store entries grouped by extracted_frame_location
        grouped_entries = {}

        # Iterate over each entry in the JSON data
        for entry in data:
            location = entry.get("extracted_frame_location")
            question_id = entry.get("question_id")
            image_id = entry.get("image_id")
            category = entry.get("direct_answers")[0]
            split = entry.get("split")
            # Check if the location already exists in the dictionary
            if location in grouped_entries:
                # Append the question_id to the list of question_ids for this location
                grouped_entries[location]["question_id"].append(question_id)
                grouped_entries[location]["image_id"].append(image_id)
                assert grouped_entries[location]["category"] == category
                assert grouped_entries[location]["split"] == split
            else:
                # Create a new entry in the dictionary with the question_id as a list
                grouped_entries[location] = {}
                grouped_entries[location]["question_id"] = [question_id]
                grouped_entries[location]["image_id"] = [image_id]
                grouped_entries[location]["category"] = category
                grouped_entries[location]["split"] = split


        
        return grouped_entries
    
    except Exception as e:
        print("Error:", e)
        return None

# Replace 'input.json' with the path to your JSON file
json_file = 'sphar_val.json'
output_json_file = 'sphar_val_grouped_by_question_id.json'
grouped_entries = group_entries_by_location(json_file)

if grouped_entries is not None:
    print("Entries grouped by extracted_frame_location:")
    with open(output_json_file, 'w') as f:
        json.dump(grouped_entries, f, indent=4)
else:
    print("Failed to group entries.")
