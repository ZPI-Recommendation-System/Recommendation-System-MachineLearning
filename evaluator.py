import pickle

with open("classes.bin", "rb") as f:
   fields_classes = pickle.load(f)

print(fields_classes)