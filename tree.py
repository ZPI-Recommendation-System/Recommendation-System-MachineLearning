from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.pipeline import make_pipeline

from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.under_sampling import RandomUnderSampler, ClusterCentroids, NearMiss
import numpy as np

import utils

DATA_FROM_DB = False
MODEL = "forest"

def make_model(model_type):
   if model_type == "forest":
      return make_pipeline(MinMaxScaler(), RandomForestClassifier(random_state=0))
   # https://blog.bigml.com/2016/09/26/predicting-airbnb-prices-with-logistic-regression/
   elif model_type == "logistic":
      return make_pipeline(StandardScaler(), LogisticRegression(multi_class='multinomial', solver='sag', max_iter=100_000))
   elif model_type == "bayes_multinomial":
      return make_pipeline(MinMaxScaler(), MultinomialNB())
   elif model_type == "bayes_complement":
      return make_pipeline(MinMaxScaler(), ComplementNB())
      

def process():
   if DATA_FROM_DB:
      from download import get_data

      data = get_data()
   else:
      data = utils.load("data.bin")
      print("Data loaded from file")

   X, Y, fields_classes = data
   
   # remove one laptop with price of 10_000

   def count_iterable(iterable):
      return sum(1 for _ in iterable)
   
   def filter_same(iterable, value):
      return filter(lambda x: x==value, iterable)

   X_train, X_test, y_train, y_test = utils.training_split(X, Y)
   
   counts = dict(
               (y, count_iterable(filter_same(y_train, y)))
               for y in y_train)
   
   adasyn_min_samples = 3
   for_adasyn = [(x, y) for x, y in zip(X, y_train) if counts[y]>adasyn_min_samples]
   # classes with less than 3 samples would be rejected by adasyn
   adasyn_rejected = [(x, y) for x, y in zip(X, y_train) if counts[y]<=adasyn_min_samples]
   X_train, y_train = list(zip(*for_adasyn))

   new_X, new_Y = ADASYN(sampling_strategy='minority').fit_resample(X_train, y_train)

   # add rejected samples back to the training dataset
   X_no_adasyn, y_no_adasyn = list(zip(*adasyn_rejected))
   new_X = np.append(new_X, X_no_adasyn, axis=0)
   new_Y = np.append(new_Y, y_no_adasyn, axis=0)

   classifier = make_model(MODEL)
   classifier.fit(new_X, new_Y)
   score = classifier.score(X_test, y_test)

   print("Accuracy:", score)

   utils.save(classifier, "model.bin")
   utils.save(fields_classes, "classes.bin")

if __name__ == "__main__":
   process()