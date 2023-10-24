from db_connect import *
import connectorx as cc
from flask import session
import pandas as pd
import time



def check_authorised(id,request):
    views = get_view(id)
    print(request.endpoint,request.endpoint in views,request.full_path)
    if request.endpoint in views:
        return True
    elif request.endpoint == 'download_csv':
        strr = str(request.full_path).split('/')[-1][0:-1]
        # print(strr[0:-1],str(request.full_path),str(request.full_path).split('/'))
        if strr in views:
            return True

    return False

def get_view(id):
    with conn() as connection:
        res = connection.execute(text(f"select * from mulitenant.user_authorised where userid = {id} "))
        result = res.fetchall()
        views = str(result[0][1]).split(',')
        # views = [i for i in views if i not in ['index','logout','login']]
        print(views)
        return views

def check_user(email):
    with conn() as connection:
        res = connection.execute(text(f"select * from mulitenant.users where user_email = '{email}' "))
        result = res.fetchall()
        print(result)
        if len(result)>0:
            return result[0][0],True
        else:
            return 0,False
        
def update_auth(id,bool):
    with conn() as connection:
        res = connection.execute(text(f"update mulitenant.users set is_authenticated = {bool} where userid = {id} "))

def insert_auth(name,email):
    query = f"insert into mulitenant.users (user_name,user_email,is_authenticated) values('{name}','{email}',false)"
    # session['user_id']
    with conn() as connection:
        res = connection.execute(text(query))
        result = connection.execute(text(f"select * from mulitenant.users where user_email = '{email}'"))
        # print('resulttt',result.fetchall())
        id = result.fetchall()[0][0]
        connection.execute(text(f"insert into mulitenant.user_authorised (userid,view_page) values({id},'index,logout,login')"))
    
def authen(info):
    email = info['email']
    name = info['name']
    is_authendicated_True = True
    print('email',email,name)
    id,check = check_user(email)
    if check:
        update_auth(id,'true')
    else:
        insert_auth(name,email)
        id,__=check_user(email)
        update_auth(id,'true')
    return id

def data_table(domain):
    df = cc.read_sql(connection_str_cx,query=f"select * from mulitenant.stg_pred where lower(domain) = '{domain}' order by ck_event_id limit 50" )
    return df.to_html()
    # with conn() as connection:
    #     res = connection.execute(text(f"select * from mulitenant.stg_pred where lower(domain) = '{domain}' "))
    #     result = res.fetchall()
    #     print(result)
    #     df = pd.DataFrame(result)
    #     # df = cc.read_sql(conn==connection,query=f"select * from mulitenant.stg_pred where domain = '{domain}' " )
    #     # df = pd.read_sql(f"select * from mulitenant.stg_pred where domain = '{domain}' ",con=connection )
    #     # print(df.shape)
    #     # res = connection.execute(text(f"select * from mulitenant.stg_pred where user_email = '{email}' "))
    #     # result = res.fetchall()
    #     return df.to_html()
def download_data(domain):
    s = time.time()
    df = cc.read_sql(connection_str_cx,query=f"select * from mulitenant.stg_pred where lower(domain) = '{domain}' order by ck_event_id" )
    
    # with conn() as connection:
    #     res = connection.execute(text(f"select * from mulitenant.stg_pred where lower(domain) = '{domain}' order by ck_event_id"))
    #     result = res.fetchall()
    #     # print(result)
    #     df = pd.DataFrame(result)
    e=time.time()
    print(e-s, (e-s)/60)
    return df
