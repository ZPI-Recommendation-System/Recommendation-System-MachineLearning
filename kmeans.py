from sklearn.cluster import KMeans
import pickle
from fields import NUMBER, CATEGORICAL

DATA_FROM_DB = False

if DATA_FROM_DB:
   from download import get_data

   data = get_data()
   with open("data.bin", "wb") as f:
      pickle.dump(data, f)
else:
   with open("data.bin", "rb") as f:
      data = pickle.load(f)
   # print("Data loaded from file")

X, Y, fields_classes = data

with open("index_to_field.bin", "rb") as f:
   index_to_field:dict[int, str] = pickle.load(f)

kmeans = KMeans(n_clusters=12, random_state=0).fit(X)


with open("classes.bin", "rb") as f:
   fields_classes:dict[str, list] = pickle.load(f)

print("field,class,value")
for center in kmeans.cluster_centers_:
   print("\nCluster center:")
   values = {}
   for i in range(len(center)):
      field = index_to_field[i]
      if field in fields_classes:
         class_start = [key for key, value in index_to_field.items() if value == field][0]
         class_index = i - class_start
         clss = (fields_classes[field][class_index] or "-")
         if not field in values or values[field][1] < center[i]:
            values[field] = (clss, center[i])
      else:
         values[field] = ("{:.2f}".format(center[i]), 1)
   for key, value in values.items():
      print(f"{key}: {value[0]}")
