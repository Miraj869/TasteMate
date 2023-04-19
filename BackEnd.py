from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
import string
import random
from datetime import datetime
import json
import haversine as hs

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TasteMateDB.db'  # SQLite URI
db = SQLAlchemy(app)

# Define your SQL schema
class Business(db.Model):
    business_id = db.Column(db.String(25), primary_key=True)
    name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    postal_code = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    stars = db.Column(db.Float)
    categories = db.Column(db.String(255))
    hours = db.Column(db.String(255))
    review_count = db.Column(db.Integer)

    def __init__(self, business_id, name,address,city,state,postal_code,latitude,longitude,stars,categories,hours,review_count):
        self.business_id = business_id
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.latitude = latitude
        self.longitude = longitude
        self.stars = stars
        self.categories = categories
        self.hours = hours
        self.review_count = review_count


    def __repr__(self):
        return f"<Business {self.id}>"
    
class Users(db.Model):
    user_id = db.Column(db.String(25), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    # reviews = db.relationship('Review', backref='user')
    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password
    def __repr__(self):
        return f"<User {self.id}>"

class Reviews(db.Model):
    review_id = db.Column(db.String(25), primary_key=True)
    user_id = db.Column(db.String(25), db.ForeignKey('Users.user_id'))
    business_id = db.Column(db.String(25), db.ForeignKey('Business.business_id'))
    stars = db.Column(db.Integer,nullable=False)
    text = db.Column(db.Text)
    date = db.Column(db.DateTime)

    def __init__(self, review_id, user_id, business_id, stars, text, date):
        self.review_id = review_id
        self.user_id = user_id
        self.business_id = business_id
        self.stars = stars
        self.text = text
        self.date = date

    def __repr__(self):
        return f"<Review {self.id}>"
    


def add_review(user_id, business_id, stars, text, date):
    rev_id = ''.join(random.choices(string.ascii_lowercase +string.digits, k=20))
    while(1):
        rev = Reviews.query.filter_by(review_id = rev_id).first()
        if not rev:
            break
        else:
            rev_id = ''.join(random.choices(string.ascii_lowercase +string.digits, k=20))
    new_review = Reviews(rev_id,user_id, business_id, stars, text, date)        
    db.session.add(new_review)
    bus = Business.query.filter_by(business_id = business_id).first()
    bus.stars = (float(bus.stars)*(bus.review_count) + stars)/(bus.review_count + 1)
    bus.review_count += 1
    db.session.commit()

def delete_review(review_id):
    rev = Reviews.query.filter_by(review_id = review_id).first()
    bus = Business.query.filter_by(business_id = rev.business_id).first()
    bus.stars = 0 if bus.review_count == 1 else (float(bus.stars)*(bus.review_count) - rev.stars)/(bus.review_count - 1)
    bus.review_count -= 1
    rev.delete()
    db.session.commit()


def validate_user(user_id,password):
    user = Users.query.filter_by(user_id = user_id).first()
    if user and user.password == password:
        return True
    else:
        return False

def add_user(user_id,username,password):
    user = Users.query.filter_by(user_id = user_id).first()
    if user:
        return False
    else:
        new_user = Users(user_id,username,password)
        db.session.add(new_user)
        db.session.commit()

def openclose(business_id):
    days = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}
    bus = Business.query.filter_by(business_id = business_id).first()
    now = int((''.join(datetime.now().strftime("%d/%m/%Y %H:%M:%S").split(" ")[1].strip().split(":")))[:-2])
    if bus.hours is None:
        return "Data Not Available"
    today = days[datetime.weekday()]
    timing = json.loads(bus.hours.replace("'","\""))
    opt = int(''.join(timing[today].split("-")[0].strip().split(":")))
    clt = opt = int(''.join(timing[today].split("-")[1].strip().split(":")))
    if today not in timing or now < opt or now > clt:
        return "Closed"
    else:
        return "Open"
    
def get_dist(curlat,curlon,buslat,buslon):
    return hs.haversine(tuple(curlat,curlon),tuple(buslat,buslon))


def search_name(name=None,catlist=[],showopen = False , dist = 20, curloc = None):
    if name is not None:
        results = Business.query.filter(Business.name.like(f'%{name}%')).all()
    
    if len(catlist) > 0:
    return results


'''
validate func inp = user_id pass out true false in app.py
add user inp = user_d username pass add to users table
get bus res input dict based on cat.pkl out buss list
open/close based on cur time and day inp check box and cur time date
distance input lat log range
business name input business name
user reviews input user_id
busines reviews input business_id
'''