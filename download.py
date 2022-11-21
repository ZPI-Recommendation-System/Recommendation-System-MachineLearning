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

NUMBER = {"ModelEntity" : ["ramAmount", "driveStorage", "weight", "ramNumberOfFreeSlots",
"ramMaxAmount", "hddSpeed"], ("ProcessorEntity", "benchmark_entity"):["benchmark"], 
("ProcessorEntity", "benchmark_entity"):["benchmark"], 
("GraphicsEntity", "benchmark_entity"):["benchmark"], 
"ProcessorEntity": ["cores", "frequency"],
"ScreenEntity":["refreshRate", "diagonalScreenInches"]}
CATEGORICAL = {"ModelEntity" : ["color", "ramType", "driveType"],
"ScreenEntity":["screenFinish"], "ScreenEntity":["touchScreen"],
"GraphicsEntity":["graphicsCardVRam"]
}

def get_data():
    engine = create_engine(DATABASE_URL)
    engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    fields_classes = defaultdict(list)

    X_pre = []
    Y = []
    
    for row in (session.query(OfferEntity, ModelEntity, ProcessorEntity, GraphicsEntity,ScreenEntity)
    .filter(OfferEntity.modelId==ModelEntity.id)
    .filter(ModelEntity.processorId==ProcessorEntity.id)
    .filter(ModelEntity.graphicsId==GraphicsEntity.id)
    .filter(ModelEntity.screenId==ScreenEntity.id)
    ).limit(1000).all():
        Y.append(row.OfferEntity.offerPrice // 1000 * 1000)
        new_row = {}
        for table, fields in NUMBER.items():
            for field in fields:
                if type(table)==tuple:
                    target = getattr(getattr(row, table[0]), table[1])
                else:
                    target = getattr(row, table)
                # GPU is integrated and None
                if target:
                    value = getattr(target, field)
                else:
                    value = None
                new_row[field] = value or 0
        for table, fields in CATEGORICAL.items():
            for field in fields:
                new_row[field] = key_to_classes(field, getattr(row, table), fields_classes)
        X_pre.append(new_row)

    X = []
    for row in X_pre:
        new_row = []
        for table, fields in NUMBER.items():
            for field in fields:
                new_row.append(row[field])
        
        for table, fields in CATEGORICAL.items():
            for field in fields:
                new_row.extend([1 if row[field]==_class else 0 
                for _class in range(len(fields_classes[field]))])
        X.append(new_row)

    # cleanup some memory
    del X_pre, fields_classes

    session.close()

    return (X, Y)

if __name__ == "__main__":
    print(get_data())