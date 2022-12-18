import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from queries import all_laptops
from to_x import to_x
from collections import defaultdict
from fields import NUMBER, CATEGORICAL, CATEGORICAL_MULTI
import utils

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DB')}"

def force_float(value):
    try:
        return float(value)
    except:
        return -1

def key_to_classes(key, row, fields_classes: defaultdict[list], value: any = None):
    classes = fields_classes[key]
    if value is None:
        value = getattr(row, key)

    if value in classes:
        return classes.index(value)
    else:
        classes.append(value)
        return len(classes)-1

def get_data(floor_price=True):
    engine = create_engine(DATABASE_URL)
    engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    fields_classes = defaultdict(list)
    index_to_field = {}

    X_pre = []
    Y = []
    
    print("Starting the query")

    for row in all_laptops(session).all():
        if row.ModelEntity.priceSource != 'allegro':
            # skip laptops without scraped price
            continue
        
        price = row.ModelEntity.price
        if floor_price:
            # round instead of floor should yield better results
            price = round(price / 1000) * 1000
        
        Y.append(price)
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
                # collect classes
                target = getattr(row, table)
                new_row[field] = getattr(target, field)
                key_to_classes(field, target, fields_classes)
        # this data took long to collect and didn't improve the results
        # for table, fields in CATEGORICAL_MULTI.items():
        #     for field, classes in fields.items():
        #         target = getattr(row, table)
        #         value = [str(element) for element in getattr(target, field)]
        #         new_row[field] = value
        #         for element in value:
        #             if type(classes) != list or element in classes:
        #                 key_to_classes(field, row, fields_classes, element)
        X_pre.append(new_row)

    print("Converting to X")
    X = to_x(X_pre, index_to_field, fields_classes)

    # cleanup some memory
    del X_pre

    session.close()
    
    print("Saving index_to_field")    

    utils.save(index_to_field, "index_to_field.bin")

    data = (X, Y, fields_classes)

    print("Saving data")

    utils.save(data, "data.bin")

    print("Returning data")

    return data


if __name__ == "__main__":
    print("Field classes: ")
    print(get_data()[2])
