from TasteMate import db

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
        return f"<Business {self.name}>"
   
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
        return f"<User {self.username}>"

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