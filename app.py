from flask import Flask
from flask import render_template
import os 
from requests import request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from google.oauth2.credentials import Credentials 
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

assets = os.path.join('static', 'assets')

class SearchForm(FlaskForm):
    query = StringField('Query', validators=[DataRequired()])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = assets
app.config['SECRET_KEY'] = os.urandom(1)

def Search(query):
    req = request.get(f'https://www.google.com/search?q={query}')
    soup = BeautifulSoup(req.text, 'html.parser')

    mobile_links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and '/url?q=' in href and '&sa=U&ved=' in href:
            mobile_link = href.split('/url?q=')[1].split('&sa=U&ved=')[0]
            mobile_links.append(mobile_link)
    return mobile_links

@app.route('/Search', methods=['POST'])
def search_route(form):
    query = form.query.data
    mobile_links = Search(query)
    for i, mobile_link in enumerate(mobile_links): 
        print(f'{i+1}. {mobile_link}')
    return render_template('searchtemp.html', mobile_links=mobile_links, form=form)
    
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
if __name__ == '__main__':
    app.run(debug=True)