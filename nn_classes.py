from sklearn.model_selection import train_test_split
from math import ceil
from imblearn.over_sampling import SMOTE, ADASYN
import pickle

import torch
import torch.nn as nn

import matplotlib.pyplot as plt
from pathlib import Path

# create directory models if it doesn't exist using Path module
Path("models").mkdir(parents=True, exist_ok=True)

DATA_FROM_DB = False

if DATA_FROM_DB:
   from download import get_data

   data = get_data()
   with open("data.bin", "wb") as f:
      pickle.dump(data, f)
else:
   with open("data.bin", "rb") as f:
      data = pickle.load(f)
   print("Data loaded from file")

X, Y, fields_classes = data

# remove one laptop with price of 10_000
l = [(x, y) for x, y in zip(X, Y) if y!=10000.0]
X, Y = list(zip(*l))

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.4, random_state=0)

X_train_balanced, Y_train_balanced = ADASYN(sampling_strategy='minority').fit_resample(X_train, y_train)

class Net(nn.Module):
    def __init__(self, input_size, H1, H2, H3, output_size):
        super(Net, self).__init__()
        
        self.linear1 = nn.Linear(input_size, H1)
        self.linear2 = nn.Linear(H1, H2)
        self.linear3 = nn.Linear(H2, H3)
        self.linear4 = nn.Linear(H3, output_size)
        
    def forward(self, x):
        y_pred = self.linear1(x).clamp(min=0)
        y_pred = self.linear2(y_pred).clamp(min=0)
        y_pred = self.linear3(y_pred).clamp(min=0)
        y_pred = self.linear4(y_pred)
        return y_pred


H1, H2, H3 = 500, 1000, 200

labels = list(range(1000, 11000, 1000))
print("labels", labels)

X_train_tensor = torch.tensor(X_train_balanced, dtype=torch.float)
Y_train_to_classes = [[1 if y == label else 0 for label in labels]
           for y in Y_train_balanced]
Y_train_tensor = torch.tensor(Y_train_to_classes, dtype=torch.float)

X_test_tensor = torch.tensor(X_test, dtype=torch.float)
Y_test_tensor = torch.tensor(y_test, dtype=torch.float)

def calculate_accuracy(model):
    # Forward and backward passes
    with torch.no_grad():
        output = model.forward(X_test_tensor)

    print("output:", output[0:3])
    predicted_labels = torch.argmax(output, dim=1).apply_(lambda x: labels[x])
    print("Y_test_tensor", Y_test_tensor[0:3])
    print("predicted_labels", predicted_labels[0:3])
    accuracy = sum(Y_test_tensor == predicted_labels)/len(Y_test_tensor)
    accuracy = accuracy.item()
    return accuracy

input_size, output_size = X_train_tensor.shape[1], Y_train_tensor.shape[1]

# model = Net(input_size, H1, H2, H3, output_size)
model = torch.load("models/model 9999 accuracy 0.5080482959747314.pt")
criterion = nn.MSELoss(reduction='sum')
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4 * 2)

losses = []
accuracies = []
iterations = 500_000
iterations_to_accuracy = 500
iterations_to_save = iterations_to_accuracy

for t in range(iterations):
    y_pred = model(X_train_tensor)
    
    loss = criterion(y_pred, Y_train_tensor)
    print(t, loss.item())
    losses.append(loss.item())

    if (t+1) % iterations_to_accuracy == 0:
        accuracy = calculate_accuracy(model)
        print("accuracy", accuracy)
        accuracies.append(accuracy)

    if(t+1) % iterations_to_save == 0:    
        torch.save(model, f"models/{t} acc {accuracy}.pt")
    
    if torch.isnan(loss):
        break
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# ignore values from before 1000 for better display
losses = losses[1000:]
plt.plot(range(len(losses)), losses)
plt.savefig("loss.png")

torch.save(model, "final_model.pt")