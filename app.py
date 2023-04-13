from __future__ import print_function
from flask import Flask, g
from flask import render_template
from flask import request
from flask_cors import CORS #comment this on deployment
import os 
import re
import sys
import requests
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
#from google.oauth2.credentials import Credentials 
#from googleapiclient.discovery import build
from bs4 import BeautifulSoup, Comment

query = [""]

assets = os.path.join('static', 'assets')

class SearchForm(FlaskForm):
    query = StringField('Query', validators=[DataRequired()])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = assets
app.config['SECRET_KEY'] = os.urandom(1)
CORS(app) #comment this on deployment

# @app.route('/Search')


def Search(query):
    req = requests.get(f'https://www.google.com/search?q={query}')
    soup = BeautifulSoup(req.text, 'html.parser')

    mobile_links = []
    index = 0
    for link in soup.find_all('a'):
        href = link["href"]
        description = link.find("p")
        print(link, file=sys.stderr)
        if href and '/url?q=' in href and '&sa=U&ved=' in href:
            mobile_link = href.split('/url?q=')[1].split('&sa=U&ved=')[0]
            mobile_links.append({"id": index, "link": mobile_link, "name": mobile_link.split("://")[1].split(".")[1], "description": description})
            index+=1
    return (mobile_links)



@app.route('/Search', methods=['GET','POST'])
def search_route():
    if request.method == 'POST':
        query[0] = request.get_json()['query']
        print(query, file=sys.stderr)
        return "success"
    else:
        if query[0] != None:
            print(query, file=sys.stderr)
            mobile_links = Search(query[0])
            print(f'These are the unfiltered results: {mobile_links}', file=sys.stderr)
            return mobile_links
        return None

# def search_route():
#     query = request.get_json()['query']
#     print(query, file=sys.stderr)
#     form = SearchForm()
#     if form.validate_on_submit():
#         query = form.query.data
#         mobile_links = Search(query)
#         print(f'These are the unfiltered results: {mobile_links}')
#         return render_template('searchtemp.html', mobile_links=mobile_links, form=form)
#     return render_template('searchtemp.html', form=form)

@app.route('/')
@app.route('/Apps')
def Apps():
    form = SearchForm()
    apps = [
        {
            'name': 'Facebook',
            'image': 'facebook.png' ,
            'description': 'This is the mobile link for facebook'
        },
        {
            'name': 'Snapchat',
            'image': 'snap.png' ,
            'description': 'This is the mobile link for Snapchat'
        },
        {
            'name': 'Instagram',
            'image': 'instagram.png',
            'description': 'This is the mobile link for Instagram'
        }
    ]
    if form.validate_on_submit():
        return search_route(form)
    return render_template('temp.html', apps=apps, form=form)

@app.route('/Info')
def Info():
    return render_template('temp.html')

@app.route('/News')
def News():
    return render_template('temp.html')

@app.route('/My Apps')
def MyApps():
    return render_template('temp.html')

@app.route('/Test')
def Test():
    return {"Links": [
        "https://www.amazon.com/",
        "https://www.apple.com/",
        "https://www.google.com/"
    ]}
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)