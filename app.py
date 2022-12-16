from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    apps = [
        {
            'name: Facebook'
            'image': 'facebook.png' 
            'description': 'This is the mobile link for facebook'
        }
        {
            'name: Snapchat'
            'image': 'snap.png' 
            'description': 'This is the mobile link for Snapchat'
        }
        {
            'name: Instagram'
            'image': 'instagram.png' 
            'description': 'This is the mobile link for Instagram'
        }
    ]
    return render_template('index.html', apps=apps)