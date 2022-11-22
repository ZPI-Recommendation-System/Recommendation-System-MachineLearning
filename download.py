import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.entities import *
import pandas as pd
from collections import defaultdict
from fields import NUMBER, CATEGORICAL
import pickle

DATABASE_URL = 'postgresql://backend:backend123@zpi.zgrate.ovh:5035/recommendation-system'

def force_float(value):
    try:
        return float(value)
    except:
        return -1

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
    index_to_field = {}

    X_pre = []
    Y = []
    
    print("Starting the query")

    for row in (session.query(OfferEntity, ModelEntity, ProcessorEntity, GraphicsEntity, ScreenEntity)
                .filter(OfferEntity.modelId == ModelEntity.id)
                .filter(ModelEntity.processorId == ProcessorEntity.id)
                .filter(ModelEntity.graphicsId == GraphicsEntity.id)
                .filter(ModelEntity.screenId == ScreenEntity.id)
                ).all():
        Y.append(row.OfferEntity.offerPrice // 1000 * 1000)
        new_row = {}
        for table, fields in NUMBER.items():
            for field in fields:
                if type(table) == tuple:
                    target = getattr(getattr(row, table[0]), table[1])
                else:
                    target = getattr(row, table)
                # GPU is integrated and None
                if target:
                    value = getattr(target, field)
                else:
                    value = None
                new_row[field] = force_float(value)
        for table, fields in CATEGORICAL.items():
            for field in fields:
                # collect classe
                target = getattr(row, table)
                new_row[field] = getattr(target, field)
                key_to_classes(field, target, fields_classes)
        X_pre.append(new_row)

    X = []
    for row in X_pre:
        new_row = []
        for table, fields in NUMBER.items():
            for field in fields:
                index_to_field[len(new_row)] = field
                new_row.append(row[field])

        for table, fields in CATEGORICAL.items():
            for field in fields:
                for i in range(len(fields_classes[field])):
                    index_to_field[len(new_row)+i] = field
                new_row.extend([1 if row[field] == _class else 0
                                for _class in fields_classes[field]])
        X.append(new_row)

    # cleanup some memory
    del X_pre

    session.close()

    
    with open("index_to_field.bin", "wb") as f:
      pickle.dump(index_to_field, f)

    print("Returning data")

    return (X, Y, fields_classes)


if __name__ == "__main__":
    print(get_data()[2])
