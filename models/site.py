from ../app.py import db

class Site(db.Model):
    id = db.Column(db.Integer, primary=True)
    display_name = db.Column(db.String(300), primary=False)
    link = db.Column(db.String(500), primary=False)
    logo_filename = db.Column(db.String(500), primary=False)
    blurb = db.Column(db.Text, primary=False)

