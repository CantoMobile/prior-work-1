from flask import Flask
from flask import render_template
import os 
from requests import request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from google.oauth2.credentials import Credentials 
from googleapiclient.discovery import build

assets = os.path.join('static', 'assets')

class SearchForm(FlaskForm):
    query = StringField('Query', validators=[DataRequired()])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = assets
app.config['SECRET_KEY'] = os.urandom(1)

def Search(query):
    credentials = Credentials.from_api_key('AIzaSyDjwXrvNJ3fNVIY1yAY-FAUffx8VYGMcDE')
    service = build('customsearch', 'v1', credentials=credentials)
    response = service.cse().list(q=f"{query} site:m", cx='017576662512468239146:omuauf_lfve').execute()
    results = response.get('items', [])
    if not results:
        return ["NO RESULTS FOUND"]

    mobile_links = []
    for result in results:
        mobile_links.append(result['link'])
    return mobile_links

@app.route('/Search', methods=['POST'])
def search_route():
    form = SearchForm()
    if form.validate_on_submit():
        query = form.query.data
        mobile_links = Search(query)
        print("Return ")
        return render_template('searchtemp.html', mobile_links=mobile_links)
    return render_template('searchtemp.html', form=form)
    
@app.route('/')
@app.route('/Apps')
def Apps():
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
    return render_template('temp.html', apps=apps)

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