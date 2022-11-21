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
   print("Data loaded from file")

X, Y, fields_classes = data

with open("index_to_field.bin", "rb") as f:
   index_to_field = pickle.load(f)

kmeans = KMeans(n_clusters=12, random_state=0).fit(X)

for center in kmeans.cluster_centers_:
   print("\nCluster center:")
   for i in range(len(center)):
      print(index_to_field[i], center[i])

# TOOD: visualise clusters
# requires saving index to field mapping