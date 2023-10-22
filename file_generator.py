# import pandas as pd
# import random

# ll = []
# for i in range(1,1000000):
#     dd = {}
#     dd['1']=random.randint(500,1000)
#     dd['2']=random.randint(0,1000)
#     dd['3']=random.randint(0,1000)
#     dd['4']=random.randint(0,1000)
#     dd['5']=random.randint(0,1000)
#     dd['6']=random.randint(0,1000)
#     dd['7']=random.randint(1000,10000)
#     dd['8']=random.randint(0,1000)
#     ll.append(dd)

# pd.DataFrame(ll).to_csv('test.csv')

import pandas as pd
import yaml
import time
# import connectorx as cc
from sqlalchemy import *
from sqlalchemy.orm import *


# host= 'sdq-prod-1.cbvts3gwaard.us-east-1.rds.amazonaws.com'
# databasename= 'sdq-prod-a7-db'
# username= 'readonly'
# password= 'Pr0DR3!D%40One#'
# port=5432

host= '192.168.1.11'
databasename= 'u0_a208'
username= 'u0_a208'
password= 'password'
port=5432



con = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{str(port)}/{databasename}',pool_size=5,max_overflow=5)
Session = sessionmaker(con) 

session = Session()
# session.execute(text('''alter table users 
#                      add column userid serial primary key,
#                      add column user_name varchar not null,
#                      add column user_email varchar not null,
#                      add column is_authenticated boolean;'''))

# session.execute(text("insert into users (user_name,user_email,is_authenticated) values('yuvan','yuvan@gmail.com',false)"))

try:
    session.commit()
except Exception as e:
    print(e)
    session.rollback()
finally:
    session.close()

# def call():
#     session = Session()
#     print(session)
#     print(session.execute(text('select * from users')))

# for i in range(0,6):
#     call()

# config = yaml.safe_load(open('config.yaml','r'))
# host = config['data_base_creds']['host']
# port = config['data_base_creds']['port']
# databasename = config['data_base_creds']['db_name']
# username = config['data_base_creds']['db_username']
# password = config['data_base_creds']['db_password']


# conn__ = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{str(port)}/{databasename}')
# conn = conn__.connect().execution_options(stream_results=True)
# conn = conn__.connect()
# def file():
#     s= time.time()

    # df1 = cc.read_sql(f'postgresql://{username}:{password}@{host}:{str(port)}/{databasename}'
                    # ,'select * from c1071003.stg_pred limit 1000000')
    # df = pd.read_sql('select * from c1071003.stg_pred',conn)
    # df1 = pd.DataFrame()
    # # ck_ev = pd.read_sql('select distinct ck_event_id from c1071003.stg_pred',conn )
    # for i in pd.read_sql('select * from c1071003.stg_pred',conn,chunksize=100000):
    #     if df1.shape[0]==0:
    #             df1 = i.copy()
    #     else:
    #         print(df1.shape)
    #         df1 = pd.concat([df1,i],ignore_index=True)
    # df1 = pd.read_csv('static/files/download.csv')
    # e = time.time()
    # print(e-s)
    # print(df1.shape)

    # return df1