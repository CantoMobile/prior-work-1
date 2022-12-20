from flask import Flask
from flask import render_template
import os 
from requests import request

assets = os.path.join('static', 'assets')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = assets

@app.route('/Search', methods=['POST'])
def Search():
    query = request.form['query']
    results = Search(query)
    return render_template('searchtemp.html', results=results)

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