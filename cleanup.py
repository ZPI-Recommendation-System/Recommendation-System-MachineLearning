import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.entities import OfferEntity

DATABASE_URL = 'postgresql://backend:backend123@zpi.zgrate.ovh:5035/recommendation-system'

engine = create_engine(DATABASE_URL)
engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

session.query(OfferEntity).filter_by(offerURL="ML").delete()

session.commit()
session.close()
