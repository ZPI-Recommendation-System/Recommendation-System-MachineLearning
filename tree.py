from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.pipeline import make_pipeline

from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.under_sampling import RandomUnderSampler, ClusterCentroids, NearMiss

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
   l = [(x, y) for x, y in zip(X, Y) if y!=10000.0]
   X, Y = list(zip(*l))

   X_train, X_test, y_train, y_test = utils.training_split(X, Y)

   new_X, new_Y = ADASYN(sampling_strategy='minority').fit_resample(X_train, y_train)

   classifier = make_model(MODEL)
   classifier.fit(new_X, new_Y)
   score = classifier.score(X_test, y_test)

   print("Accuracy:", score)

   utils.save(classifier, "model.bin")
   utils.save(fields_classes, "classes.bin")

if __name__ == "__main__":
   process()