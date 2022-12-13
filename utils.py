from sklearn.model_selection import train_test_split

def training_split(X, Y):
   X_train, X_verify, y_train, y_verify = train_test_split(X, Y, test_size=0.1, random_state=0)
   X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.4, random_state=0)

   return X_train, X_test, y_train, y_test

def verify_split(X, Y):
   X_train, X_verify, y_train, y_verify = train_test_split(X, Y, test_size=0.1, random_state=0)
   X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.4, random_state=0)

   return X_verify, y_verify

import pickle

def save(obj, path):
    with open(path, "wb") as f:
        pickle.dump(obj, f)

def load(path):
    with open(path, "rb") as f:
        return pickle.load(f)
