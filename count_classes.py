from queries import counts_connections, counts_communications, counts_controls, counts_multimedia, counts_drives

# create sqlalachemy session 
from sqlalchemy import create_engine
# import sessionmaker
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://backend:backend123@zpi.zgrate.ovh:5035/recommendation-system'
engine = create_engine(DATABASE_URL)
engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

counts = counts_connections(session).all()


# print results of counts_connections, counts_communications, counts_controls, counts_multimedia, counts_drives as tables in descending order
for func in [counts_connections, counts_communications, counts_controls, counts_multimedia, counts_drives]:
    counts = func(session).all()
    counts.sort(key=lambda x: x[0], reverse=True)
    print(func.__name__)
    # print counts with tabs in descending order
    for count in sorted(counts, key=lambda x: x[0], reverse=True):
        print('\t', count[0], '\t', count[1])
    print()


session.close()
