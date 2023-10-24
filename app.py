from authlib.integrations.flask_client import OAuth
import pandas as pd
# import connectorx as cc
# from  file_generator import *
from sqlalchemy import *
from operation import *
from flask import Flask, redirect, url_for, session, request, jsonify,render_template,send_file,Response


# create_pool_from_url()
# print(session)

# conn__ = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{str(port)}/{databasename}')

# import requests

app = Flask(__name__)
app.secret_key = 'test'
client_id = '568987694416-q421d6q05trqnrd32rdnd1smve27vdde.apps.googleusercontent.com'
client_secret = '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'

# engine = create_engine('"sqlite:////file.db"')
# app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:////file.db"

oauth = OAuth(app)
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    client_id=client_id,
    client_secret=client_secret,
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@app.before_request
def before_request():
    if 'google_token' not in session and request.endpoint != 'login':
        # return index()
        print('before',request.endpoint,request.full_path)
        if request.endpoint == 'resp':
            pass
        else:
            return index()
    elif 'google_token' not in session and request.endpoint == 'login':
        pass
    else:# 'google_token' in session :
        print('before1',request.endpoint)
        if request.endpoint== 'logout' :
            print('logging out')
            pass 
        elif check_authorised(session['user_id'],request):
            print('authorized')
            pass
        else:
            pass 
            # print('unauthorized')
            return unauthorised()

@app.route('/')
def index():
    if 'google_token' in session:
        # print(session['google_token'])
        name = session['google_token']['userinfo']['name']
        email = session['google_token']['userinfo']['email']
        views = get_view(session['user_id'])
        views = [i for i in views if i not in ['index','logout','login']]
        print(views)
        data = {'name':name,'email':email,"view":views}
        return render_template('download.html',data = data)
    return render_template('login.html')
    # if method == 'GET':
    #     print('test')
    # # request
    # return render_template('login.html') #'Login'

@app.route('/unauthorised')
def unauthorised():
    return '<h1>Your unauthorised to veiw this page</h1>'


@app.route('/login')
def login():
    redirect_uri = url_for('resp', _external=True)
    print(redirect_uri)
    return oauth.google.authorize_redirect(redirect_uri)
    return google.authorize(callback=url_for('resp', _external=True))

@app.route('/login/resp')
def resp():
    token = oauth.google.authorize_access_token()
    session['google_token'] = token
    print(token)
    id = authen(token['userinfo'])
    session['user_id'] = id
    # print(session)
    user = token['userinfo']['name']
    print(" Google User ", user)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    update_auth(session['user_id'],'false')
    session.pop('google_token',None)
    return redirect(url_for('index'))

@app.route('/download_csv/<domain>')
def download_csv(domain):
    name = session['google_token']['userinfo']['name']
    df = download_data(domain)
    return Response(
       df.to_csv(),
       mimetype="text/csv",
       headers={"Content-disposition":
       f"attachment; filename={name}_{domain}_file.csv"})
    # return send_file('static/files/download.csv',as_attachment=True)

@app.route('/ae')
def ae():
    data = data_table('ae')
    data = '<button><a href="/download_csv/ae">Download CSV</a></button>'+data
    return str(data)
@app.route('/cm')
def cm():
    data = data_table('cm')
    data = '<button><a href="/download_csv/ae">Download CSV</a></button>'+data
    return str(data)

@app.route('/mh')
def mh():
    data = data_table('mh')
    data = '<button><a href="/download_csv/ae">Download CSV</a></button>'+data
    return str(data)


if __name__ =='__main__':
    app.run(host='0.0.0.0',port=5001)