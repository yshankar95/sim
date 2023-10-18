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
import connectorx as cc


config = yaml.safe_load(open('config.yaml','r'))
host = config['data_base_creds']['host']
port = config['data_base_creds']['port']
databasename = config['data_base_creds']['db_name']
username = config['data_base_creds']['db_username']
password = config['data_base_creds']['db_password']


# conn__ = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{str(port)}/{databasename}')
# conn = conn__.connect().execution_options(stream_results=True)
# conn = conn__.connect()
def file():
    s= time.time()

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
    df1 = pd.read_csv('static/files/download.csv')
    e = time.time()
    print(e-s)
    print(df1.shape)

    return df1