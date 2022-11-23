from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline

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

new_X = []
new_Y = []
count = 200

# similar counts for classes 
for price in set(Y):
   counter = 0
   for x, y in zip(X, Y):
      if y == price and price != 10000.0:
         new_X.append(x)
         new_Y.append(y)
         counter += 1
         if counter >= count:
            break
   if counter < count:
      print("not enough data for price", price, counter)

X_train, X_test, y_train, y_test = train_test_split(new_X, new_Y, test_size=0.4, random_state=0)

print("Logistic regression")

# https://blog.bigml.com/2016/09/26/predicting-airbnb-prices-with-logistic-regression/
classifier = Pipeline([('Normalizing',MinMaxScaler()),('NaiveBayes',MultinomialNB())]) # ComplementNB
classifier.fit(X_train, y_train)
score = classifier.score(X_test, y_test)

print("Accuracy:", score)

with open("model.bin", "wb") as f:
   pickle.dump(classifier, f)

with open("classes.bin", "wb") as f:
   pickle.dump(fields_classes, f)
