from db_connect import *


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
    with conn() as connection:
        res = connection.execute(text(query))
    
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