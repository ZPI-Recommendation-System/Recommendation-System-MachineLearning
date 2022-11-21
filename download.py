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

def get_data():
    engine = create_engine(DATABASE_URL)
    engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    fields_classes = defaultdict(list)

    X = []
    Y = []
    
    for offer, model in session.query(OfferEntity, ModelEntity).filter(OfferEntity.modelId==ModelEntity.id).limit(1000).all():
        Y.append(offer.offerPrice // 1000 * 1000)
        X.append([model.ramAmount, key_to_classes('color', model, fields_classes)])

    session.close()

    return (X, Y)

if __name__ == "__main__":
    print(get_data())