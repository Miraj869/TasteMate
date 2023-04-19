from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv

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
    user_id = db.Column(db.String(25), db.ForeignKey(Users.user_id))
    business_id = db.Column(db.String(25), db.ForeignKey(Business.business_id))
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

# Create the table in the database
def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print(f'Clear table {table}')
        session.execute(table.delete())
    session.commit()
with app.app_context():
    db.create_all()
    db.session.commit()
    clear_data(db.session)
    db.create_all()
    db.session.commit()
    print("Tables made")
    with open('Data\\business.csv', mode ='r',encoding='utf-8') as file:
    
        # reading the CSV file
        csvFile = csv.reader(file)

        for i,line in enumerate(csvFile):
            # print(i)
            if i==0:
                continue
            # print(len(line))
            # print(line[1])
            # exit()
            # print(type(line))
            business = Business(line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12])
            db.session.add(business)
    file.close()
    print("Business table made")
    db.session.commit()

    with open('Data\\user.csv', mode ='r',encoding='utf-8') as file:
        # reading the CSV file
        csvFile = csv.reader(file)
        for i,line in enumerate(csvFile):
            if i==0:
                continue
            user = Users(line[0],line[1],line[2])
            db.session.add(user)
    file.close()
    print("Users table made")
    db.session.commit()

    with open('Data\\review.csv', mode ='r',encoding='utf-8') as file:
        # reading the CSV file
        csvFile = csv.reader(file)
        for i,line in enumerate(csvFile):
            if i==0:
                continue
            review = Reviews(line[1],line[2],line[3],line[4],line[5], None if line[6] == '' else datetime.strptime(line[6], '%Y-%m-%d %H:%M:%S'))
            db.session.add(review)
    file.close()
    print("Reviews table made")
    db.session.commit()



