from sklearn.model_selection import train_test_split
from math import ceil
from imblearn.over_sampling import SMOTE, ADASYN
import pickle

import torch
import torch.nn as nn

import matplotlib.pyplot as plt


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

new_X, new_Y = ADASYN(sampling_strategy='minority').fit_resample(X_train, y_train)


class Net(nn.Module):
    def __init__(self, D_in, H1, H2, H3, D_out):
        super(Net, self).__init__()
        
        self.linear1 = nn.Linear(D_in, H1)
        self.linear2 = nn.Linear(H1, H2)
        self.linear3 = nn.Linear(H2, H3)
        self.linear4 = nn.Linear(H3, D_out)
        
    def forward(self, x):
        y_pred = self.linear1(x).clamp(min=0)
        y_pred = self.linear2(y_pred).clamp(min=0)
        y_pred = self.linear3(y_pred).clamp(min=0)
        y_pred = self.linear4(y_pred)
        return y_pred


H1, H2, H3 = 500, 1000, 200

numeric_x = torch.tensor(new_X, dtype=torch.float)
numeric_y = torch.tensor([[y] for y in new_Y], dtype=torch.float)

D_in, D_out = numeric_x.shape[1], numeric_y.shape[1]

model1 = Net(D_in, H1, H2, H3, D_out)
criterion = nn.MSELoss(reduction='sum')
optimizer = torch.optim.Adam(model1.parameters(), lr=1e-4 * 2)

losses1 = []

for t in range(10):
    y_pred = model1(numeric_x)
    
    loss = criterion(y_pred, numeric_y)
    print(t, loss.item())
    losses1.append(loss.item())
    
    if torch.isnan(loss):
        break
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

plt.plot(range(len(losses1)), losses1)
plt.savefig("loss.png")