import operator
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.entities import OfferEntity
import numpy as np

from queries import all_laptops
from to_x import to_x
import pandas as pd
from collections import defaultdict
from fields import NUMBER, CATEGORICAL

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt

from collections import Counter

DATABASE_URL = 'postgresql://backend:backend123@zpi.zgrate.ovh:5035/recommendation-system'

import pickle

with open("classes.bin", "rb") as f:
   fields_classes = pickle.load(f)


with open("model.bin", "rb") as f:
   model = pickle.load(f)


with open("index_to_field.bin", "rb") as f:
   index_to_field = pickle.load(f)


with open("data.bin", "rb") as f:
    data = pickle.load(f)

X, Y, fields_classes = data

def process():
      X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

      pred = model.predict(X_test)
      diff = np.absolute(pred - y_test)

      L = sorted(zip(y_test, diff), key=operator.itemgetter(0))   
      y_test, diff = zip(*L)

      c = Counter(zip(y_test, diff))
      s = [c[(xx,yy)] for xx,yy in zip(y_test,diff)]

      
      plt.scatter(y_test, diff, s=s)
      plt.xlabel("Price")
      plt.ylabel("Error")
      plt.show()

if __name__ == "__main__":
   process()
