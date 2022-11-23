from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from math import ceil
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.under_sampling import RandomUnderSampler, ClusterCentroids, NearMiss

import pandas as pd
import pickle

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

print("RandomForestClassifier")

classifier = RandomForestClassifier(random_state=0)
# classifier =  Pipeline([('Normalizing',MinMaxScaler()),('RandomForestClassifier',RandomForestClassifier(random_state=0))])
classifier.fit(new_X, new_Y)
score = classifier.score(X_test, y_test)

print("Accuracy:", score)

with open("model.bin", "wb") as f:
   pickle.dump(classifier, f)

with open("classes.bin", "wb") as f:
   pickle.dump(fields_classes, f)
