import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from queries import all_laptops
from to_x import to_x
import pandas as pd
from collections import defaultdict
from fields import NUMBER, CATEGORICAL
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DB')}"

def process():
    processor = []
    graphics = []
    price = []

    engine = create_engine(DATABASE_URL)
    engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    
    print("Starting the query")

    for row in all_laptops(session).all():

        price.append(row.ModelEntity.price)
        processor.append((row.ProcessorEntity.benchmark_entity and row.ProcessorEntity.benchmark_entity.benchmark) or 0)
        graphics.append((row.GraphicsEntity and row.GraphicsEntity.benchmark_entity and row.GraphicsEntity.benchmark_entity.benchmark) or 0)

    plt.scatter(processor, price, c=graphics, cmap='viridis')
    plt.colorbar(label="Graphics")
    plt.xlabel("Processor")
    plt.ylabel("Price")
    plt.show()
        
if __name__ == '__main__':
    process()