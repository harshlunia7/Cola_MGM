import json

def check_unique_question_ids(json_file):
    try:
        # Open the JSON file
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Create a set to store unique question_ids
        question_ids = set()

        # Iterate over each entry in the JSON data
        for entry in data:
            question_id = entry.get("question_id")
            
            # Check if the question_id is already in the set
            if question_id in question_ids:
                return False  # Not all question_ids are unique
            else:
                question_ids.add(question_id)
        
        return True  # All question_ids are unique
    
    except Exception as e:
        print("Error:", e)
        return False

# Replace 'input.json' with the path to your JSON file
json_file = 'sphar_val.json'
result = check_unique_question_ids(json_file)

if result:
    print("All question_ids are unique.")
else:
    print("Not all question_ids are unique.")
