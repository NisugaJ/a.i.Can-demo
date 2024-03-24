from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///sqlite.db', echo=True)
Session = sessionmaker(bind=engine)

def get_session():
    session = Session()
    return session
