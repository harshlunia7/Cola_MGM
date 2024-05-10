from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import json

def evaluate_predictions(pred_actions, true_actions):
    accuracy = accuracy_score(true_actions, pred_actions)
    precision = precision_score(true_actions, pred_actions, average='weighted')
    recall = recall_score(true_actions, pred_actions, average='weighted')
    f1 = f1_score(true_actions, pred_actions, average='weighted')
    
    return accuracy, precision, recall, f1

predicted_actions = []
true_actions = []

with open('./predictions/sphar_custom_final/epoch_29/val-da.json', 'r') as f:
    data = json.load(f)

for video_path, pred in data.items():
    true_actions.append(video_path.split('/')[1])
    predicted_actions.append(pred)
    print(true_actions[-1], predicted_actions[-1])

accuracy, precision, recall, f1 = evaluate_predictions(predicted_actions, true_actions)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)
