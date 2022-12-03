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

X_train_tensor = torch.tensor(X_train, dtype=torch.float)
Y_train_tensor = torch.tensor(y_train, dtype=torch.float)

X_test_tensor = torch.tensor(X_test, dtype=torch.float)
Y_test_tensor = torch.tensor(y_test, dtype=torch.float)

def calculate_accuracy(model):
    # Forward and backward passes
    with torch.no_grad():
        output = model.forward(X_test_tensor)
    
    # print("output:", output[0:3])
    output_floored = output // 1000 * 1000
    y_test_floored = Y_test_tensor // 1000 * 1000
    # print("output_floored", output_floored[0:3])
    # print("y_test_floored", y_test_floored[0:3])
    accuracy = sum(y_test_floored == output_floored)/len(Y_test_tensor)
    accuracy = accuracy.item()
    return accuracy

input_size, output_size = X_train_tensor.shape[1], Y_train_tensor.shape[1]

model = Net(input_size, H1, H2, H3, output_size)
criterion = nn.MSELoss(reduction='sum')
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4 * 2)

losses = []
accuracies = []
iterations = 10000
iterations_to_accuracy = 50
iterations_to_save = iterations_to_accuracy

for t in range(iterations):
    y_pred = model(X_train_tensor)
    
    loss = criterion(y_pred, Y_train_tensor)
    print(t, loss.item())
    losses.append(loss.item())

    if t!=0 and t % iterations_to_accuracy == 0:
        accuracy = calculate_accuracy(model)
        print("accuracy", accuracy)
        accuracies.append(accuracy)

    if t!=0 and t % iterations_to_save == 0:    
        torch.save(model, f"models/model {t} accuracy {accuracy}.pt")
    
    if torch.isnan(loss):
        break
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

plt.plot(range(len(losses)), losses)
plt.savefig("loss.png")

torch.save(model, "final_model.pt")