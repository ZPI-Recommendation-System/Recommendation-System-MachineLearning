from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

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

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

# https://blog.bigml.com/2016/09/26/predicting-airbnb-prices-with-logistic-regression/
classifier = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=100_000)
classifier.fit(X_train, y_train)
score = classifier.score(X_test, y_test)

print("Accuracy:", score)

with open("model.bin", "wb") as f:
   pickle.dump(classifier, f)

with open("classes.bin", "wb") as f:
   pickle.dump(fields_classes, f)
