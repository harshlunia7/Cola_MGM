import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import json

predicted_actions = []
true_actions = []
actions = set()
with open('./predictions/sphar_custom_final/epoch_29/val-da.json', 'r') as f:
    data = json.load(f)

for video_path, pred in data.items():
    true_actions.append(video_path.split('/')[1])
    actions.add(true_actions[-1])
    predicted_actions.append(pred)
    print(true_actions[-1], predicted_actions[-1])
print(actions)
# cm = confusion_matrix(true_actions, predicted_actions)

# Plot confusion matrix
# plt.figure(figsize=(10, 10))
# sns.heatmap(cm, annot=True, cmap='Blues', fmt='g', xticklabels=actions,
#             yticklabels=actions)
# plt.xlabel('Predicted')
# plt.ylabel('True')
# plt.title('Confusion Matrix')
# plt.savefig('confusion_matrix.png')  
# plt.show()
