from contextlib import contextmanager
from sqlalchemy import *
from sqlalchemy.orm import *


host= 'localhost'
databasename= 'postgres'
username= 'postgres'
password= 'Password'
port=5432

connection_str= f'postgresql+psycopg2://{username}:{password}@{host}:{str(port)}/{databasename}'
connection_str_cx= f'postgresql://{username}:{password}@{host}:{str(port)}/{databasename}'

con = create_engine(connection_str,pool_size=5,max_overflow=5)
Session = sessionmaker(con,autocommit=False)
    

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
