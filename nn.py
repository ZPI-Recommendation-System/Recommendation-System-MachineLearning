from sklearn.model_selection import train_test_split
from math import ceil
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

   data = get_data(floor_price=False)
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
y_test = [[y] for y in y_test]
y_train = [[y] for y in y_train]

class Net(nn.Module):
    def __init__(self, input_size, H1, H2, H3, output_size):
        super(Net, self).__init__()
        
        # https://machinelearningmastery.com/dropout-for-regularizing-deep-neural-networks/
        input_dropout = 0.2
        dropout = 0.2

        self.dropout0 = nn.Dropout(input_dropout)
        self.linear1 = nn.Linear(input_size, H1)
        self.dropout1 = nn.Dropout(dropout)
        self.linear2 = nn.Linear(H1, H2)
        self.dropout2 = nn.Dropout(dropout)
        self.linear3 = nn.Linear(H2, H3)
        self.dropout3 = nn.Dropout(dropout)
        self.linear4 = nn.Linear(H3, output_size)
        
    def forward(self, x):
        y_pred = self.dropout0(x)
        y_pred = self.linear1(y_pred).clamp(min=0)
        y_pred = self.dropout1(y_pred)
        y_pred = self.linear2(y_pred).clamp(min=0)
        y_pred = self.dropout2(y_pred)
        y_pred = self.linear3(y_pred).clamp(min=0)
        y_pred = self.dropout3(y_pred)
        y_pred = self.linear4(y_pred)
        return y_pred


H1, H2, H3 = 500, 1000, 200

X_train_tensor = torch.tensor(X_train, dtype=torch.float)
Y_train_tensor = torch.tensor(y_train, dtype=torch.float)

X_test_tensor = torch.tensor(X_test, dtype=torch.float)
Y_test_tensor = torch.tensor(y_test, dtype=torch.float)

def calculate_accuracy(model):
    # Forward and backward passes
    with torch.no_grad():
        output = model.forward(X_test_tensor)
    
    # print("output:", output[0:3])
    output_floored = torch.round(output / 1000) * 1000
    y_test_floored = torch.round(Y_test_tensor / 1000) * 1000
    # print("output_floored", output_floored[0:3])
    # print("y_test_floored", y_test_floored[0:3])
    accuracy = sum(y_test_floored == output_floored)/len(Y_test_tensor)
    accuracy = accuracy.item()
    return accuracy

input_size, output_size = X_train_tensor.shape[1], Y_train_tensor.shape[1]

model = Net(input_size, H1, H2, H3, output_size)
criterion = nn.MSELoss(reduction='sum')
# lr: https://machinelearningmastery.com/dropout-regularization-deep-learning-models-keras/
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4 * 2 * 10)

losses = []
accuracies = []
iterations = 100_000
iterations_to_accuracy = 50
iterations_to_save = iterations_to_accuracy

try:
    for t in range(iterations):
        y_pred = model(X_train_tensor)
        
        loss = criterion(y_pred, Y_train_tensor)
        print(t, loss.item())
        losses.append(loss.item())

        if (t+1) % iterations_to_accuracy == 0:
            accuracy = calculate_accuracy(model)
            print("accuracy", accuracy)
            accuracies.append(accuracy)

        if (t+1) % iterations_to_save == 0:    
            torch.save(model, f"models/model {t} accuracy {accuracy}.pt")
        
        if torch.isnan(loss):
            break
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
except KeyboardInterrupt:
    print("KeyboardInterrupt")

# ignore values from before 1000 for better display
losses = losses[1000:]
accuracies = accuracies[1000:]

plt.plot(range(len(losses[1000:])), losses)
plt.savefig("loss.png")

# clear plot
plt.clf()
plt.cla()

plt.plot(range(len(accuracies)), accuracies)
plt.savefig("acc.png")

torch.save(model, "final_model.pt")