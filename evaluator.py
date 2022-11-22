import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.entities import OfferEntity

from queries import all_laptops
from to_x import to_x
import pandas as pd
from collections import defaultdict
from fields import NUMBER, CATEGORICAL

DATABASE_URL = 'postgresql://backend:backend123@zpi.zgrate.ovh:5035/recommendation-system'

import pickle

with open("classes.bin", "rb") as f:
   fields_classes = pickle.load(f)


with open("model.bin", "rb") as f:
   model = pickle.load(f)


with open("index_to_field.bin", "rb") as f:
   index_to_field = pickle.load(f)

print(fields_classes)

def process():
    engine = create_engine(DATABASE_URL)
    engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    
    print("Starting the query")

    for row in all_laptops(session).limit(10).all():

      # TOOD: refactor
      new_row = {}
      for table, fields in NUMBER.items():
         for field in fields:
            if type(table) == tuple:
               target = getattr(getattr(row, table[0]), table[1])
            else:
               target = getattr(row, table)
            if target:
               value = getattr(target, field)
            else:
               value = None
            new_row[field] = value
      for table, fields in CATEGORICAL.items():
         for field in fields:
            target = getattr(row, table)
            new_row[field] = value

      X = to_x([new_row], index_to_field, fields_classes)

      predictedPrice = model.predict(X)[0]
      print(predictedPrice)

      print("Posting offer")
      newOffer = OfferEntity(offerName="ML", offerURL="ML", offerPrice=predictedPrice, modelId=row.ModelEntity.id)
      session.add(newOffer)   

    session.commit()
    session.close()


if __name__ == "__main__":
   process()
