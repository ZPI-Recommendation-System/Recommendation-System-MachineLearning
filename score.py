import operator
import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np

from queries import all_laptops
from to_x import to_x
import pandas as pd
from collections import defaultdict
from fields import NUMBER, CATEGORICAL

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import random
import numpy as np
import utils

from collections import Counter

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DB')}"

USE_VERIF = False

fields_classes = utils.load("classes.bin")
model = utils.load("model.bin")
index_to_field = utils.load("index_to_field.bin")
data = utils.load("data.bin")

X, Y, fields_classes = data

def random_reading():
   return random.randint(1, 10) * 1000

def process():
      if USE_VERIF:
         X_verify, y_verify = utils.verify_split(X, Y)
      else:
         X_verify = X
         y_verify = Y
      
      pred = model.predict(X_verify)
      # random prediction
      # pred = np.array([random_reading() for i in range(len(y_verify))])
      diff = np.absolute(pred - y_verify)
      # count the number of zeroes in diff
      hits = len(diff) - np.count_nonzero(diff)
      score = hits / len(diff)
      print("Score: ", score)

      L = sorted(zip(y_verify, diff), key=operator.itemgetter(0))   
      y_verify, diff = zip(*L)

      c = Counter(zip(y_verify, diff))
      s = [c[(xx,yy)] for xx,yy in zip(y_verify,diff)]

      
      plt.scatter(y_verify, diff, s=s)
      plt.xlabel("Price")
      plt.ylabel("Error")
      plt.show()

if __name__ == "__main__":
   process()
