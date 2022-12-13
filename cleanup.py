import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.entities import OfferEntity

DATABASE_URL = f"'postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DB')}"

engine = create_engine(DATABASE_URL)
engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

session.query(OfferEntity).filter_by(offerURL="ML").delete()

session.commit()
session.close()
