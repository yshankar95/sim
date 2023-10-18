from flask import Flask, redirect, url_for, session, request, jsonify,render_template,send_file,Response
from authlib.integrations.flask_client import OAuth
import pandas as pd
import connectorx as cc
from  file_generator import *

# import requests

app = Flask(__name__)
app.secret_key = 'test'
client_id = '568987694416-q421d6q05trqnrd32rdnd1smve27vdde.apps.googleusercontent.com'
client_secret = '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'


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
@app.route('/')
def index():
    if 'google_token' in session:
        # print(session['google_token'])
        name = session['google_token']['userinfo']['name']
        email = session['google_token']['userinfo']['email']
        data = {'name':name,'email':email}
        return render_template('download.html',data = data)
    return render_template('login.html')
    # if method == 'GET':
    #     print('test')
    # # request
    # return render_template('login.html') #'Login'

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
    user = token['userinfo']['name']
    print(" Google User ", user)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('google_token',None)
    return redirect(url_for('index'))

@app.route('/download_csv')
def download_csv():
    name = session['google_token']['userinfo']['name']
    df = file()
    return Response(
       df.to_csv(),
       mimetype="text/csv",
       headers={"Content-disposition":
       f"attachment; filename={name}_file.csv"})
    # return send_file('static/files/download.csv',as_attachment=True)



if __name__ =='__main__':
    app.run(port=5001)