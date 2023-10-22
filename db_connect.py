from contextlib import contextmanager
from sqlalchemy import *
from sqlalchemy.orm import *


host= '192.168.1.11'
databasename= 'u0_a208'
username= 'u0_a208'
password= 'password'
port=5432



con = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{str(port)}/{databasename}',pool_size=5,max_overflow=5)
Session = sessionmaker(con)
    

@contextmanager
def conn():
    session = Session()
    try:
        yield session
        session.commit()
        print('session commited')
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        print('sessin closed')
        session.close()
