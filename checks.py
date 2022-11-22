import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.entities import OfferEntity

from queries import all_laptops
from to_x import to_x
import pandas as pd
from collections import defaultdict
from fields import NUMBER, CATEGORICAL
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

DATABASE_URL = 'postgresql://backend:backend123@zpi.zgrate.ovh:5035/recommendation-system'

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
        # skip macbooks for now
        name = row.ModelEntity.name.lower()
        if "macbook" in name or "apple" in name:
            continue

        price.append(row.OfferEntity.offerPrice)
        processor.append((row.ProcessorEntity.benchmark_entity and row.ProcessorEntity.benchmark_entity.benchmark) or 0)
        graphics.append((row.GraphicsEntity and row.GraphicsEntity.benchmark_entity and row.GraphicsEntity.benchmark_entity.benchmark) or 0)

    plt.scatter(processor, price, c=graphics, cmap='viridis')
    plt.colorbar()
    plt.show()
        
if __name__ == '__main__':
    process()