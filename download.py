import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.entities import *
import pandas as pd
from collections import defaultdict

DATABASE_URL = 'postgresql://backend:backend123@zpi.zgrate.ovh:5035/recommendation-system'

def key_to_classes(key, row, fields_classes: defaultdict[list]):
    classes = fields_classes[key]
    value = getattr(row, key)

    if value in classes:
        return classes.index(value)
    else:
        classes.append(value)
        return len(classes)-1

if __name__ == "__main__":
    engine = create_engine(DATABASE_URL)
    engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    fields_classes = defaultdict(list)
    
    for offer, model in session.query(OfferEntity, ModelEntity).limit(10).all():
        print(offer.offerPrice, model.ramAmount, model.color, key_to_classes('color', model, fields_classes))

    session.close()
