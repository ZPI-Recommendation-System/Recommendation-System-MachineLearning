from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

import pandas as pd
import pickle
from download import get_data

X_train, X_test, y_train, y_test = train_test_split(*get_data(), test_size=0.2, random_state=0)

# https://blog.bigml.com/2016/09/26/predicting-airbnb-prices-with-logistic-regression/
classifier = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=200)
classifier.fit(X_train, y_train)
score = classifier.score(X_test, y_test)

print("Accuracy:", score)

filename = "model.lr"
print("Saving to", filename)
with open(filename, "wb") as f:
   pickle.dump(classifier, f)
