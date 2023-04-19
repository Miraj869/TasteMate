# from flask import Flask, render_template, request, redirect, url_for, flash, session
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, BooleanField, SubmitField
# from wtforms.validators import DataRequired, Email, EqualTo, Length
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret_key' # replace with your own secret key
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' # replace with your own database URI
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)

# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember_me = BooleanField('Remember Me')
#     submit = SubmitField('Log In')

# class RegistrationForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
#     password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
#     confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Sign Up')

# @app.route('/', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user and user.password == form.password.data:
#             session['user_id'] = user.id
#             if form.remember_me.data:
#                 session.permanent = True
#             return redirect(url_for('home'))
#         else:
#             flash('Invalid username or password', 'danger')
#     return render_template('login.html', title='Log In', form=form)

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(username=form.username.data, password=form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('Your account has been created! You are now able to log in', 'success')
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Sign Up', form=form)

# @app.route('/home')
# def home():
#     if 'user_id' in session:
#         user = User.query.filter_by(id=session['user_id']).first()
#         return render_template('home.html', title='Home', user=user)
#     else:
#         return redirect(url_for('login'))

# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     session.permanent = False
#     return redirect(url_for('login'))

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, flash, session, Response
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
import datetime
import random
import requests
import csv
import io
import json
from BackEnd import Business, Users, Reviews, validate_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key' # replace with your own secret key
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///businesses.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# class Business(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255))
#     address = db.Column(db.String(255))
#     city = db.Column(db.String(255))
#     state = db.Column(db.String(255))
#     postal_code = db.Column(db.String(255))
#     stars = db.Column(db.Float)
#     review_count = db.Column(db.Integer)
#     attributes = db.Column(db.String(255))
#     categories = db.Column(db.String(255))
#     working_hours = db.Column(db.String(255))

#     def __repr__(self):
#         return f"<Business {self.id}>"

# class Review(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     user = db.relationship('User', backref='reviews')
#     business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
#     stars = db.Column(db.Integer)
#     text = db.Column(db.Text)
#     date = db.Column(db.DateTime)

#     def __repr__(self):
#         return f"<Review {self.id}>"

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)
#     # reviews = db.relationship('Review', backref='user')

#     def __repr__(self):
#         return f"<User {self.id}>"
    
class LoginForm(FlaskForm):
    userid = StringField('UserID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # isloggedIn = False
    # if form.validate_on_submit():
    #     user = User.query.filter_by(username=form.username.data).first()
    #     if user and user.password == form.password.data:
    #         session['user_id'] = user.id
    #         if form.remember_me.data:
    #             session.permanent = True
    #             isloggedIn = True
    #         return redirect(url_for('home', current_user=current_user))
    #     else:
    #         flash('Invalid username or password', 'danger')
    if form.validate_on_submit():
        userid = request.form['userid']
        password = request.form['password']
        if validate_user(userid, password):
            return redirect(url_for('home'))
        else:
            flash('Incorrect username or password')
            return redirect('/')
    return render_template('login.html', title='Log In', form=form, current_user=current_user)

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = Users(username=form.username.data, password=form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('Your account has been created! You are now able to log in', 'success')
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Sign Up', form=form, current_user=current_user)

@app.route('/home')
def home():
    if 'user_id' in session:
        # business_id1 = 1
        # business_id2 = 2
        # business_id3 = 3
        # business_id4 = 4
        # business1 = Business.query.get_or_404(business_id1)
        # business2 = Business.query.get_or_404(business_id2)
        # business3 = Business.query.get_or_404(business_id3)
        # business4 = Business.query.get_or_404(business_id4)
        businesses = Business.query.all()
        # business1 = random.choice(businesses)
        # business2 = random.choice(businesses)
        # business3 = random.choice(businesses)
        # business4 = random.choice(businesses)
        random_businesses = random.sample(businesses, k=4)
        user = Users.query.filter_by(id=session['user_id']).first()
        return render_template('home.html', title='Home', user=user, random_businesses=random_businesses)
    else:
        return redirect(url_for('login', current_user=current_user))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.permanent = False
    return redirect(url_for('login', current_user=current_user))

@app.route('/businesses')
def businesses():
    # Retrieve search parameters from the URL query string
    search_query = request.args.get('search_query', '')
    opening_hours = request.args.get('opening_hours', '')
    cuisine_type = request.args.get('cuisine_type', '')
    price_range = request.args.get('price_range', '')
    distance = request.args.get('distance', '')

    # Query the businesses based on the search parameters
    businesses = Business.query.filter(
        Business.name.like(f'%{search_query}%'),
        Business.working_hours.like(f'%{opening_hours}%'),
        Business.categories.like(f'%{cuisine_type}%'),
        Business.attributes.like(f'%{price_range}%')
    ).all()

    # Get the current page from the request arguments or default to 1
    page = request.args.get('page', 1, type=int)

    # Set the number of businesses to display per page
    per_page = 10

    return render_template('businesses.html', businesses=businesses, page=page, per_page=per_page, current_user=current_user)

@app.route('/businesses/<int:business_id>')
def business_detail(business_id, page=1):
    business = Business.query.get_or_404(business_id)
    reviews = Reviews.query.filter_by(business_id=business_id).all()

    # Sort reviews by date in descending order
    reviews = sorted(reviews, key=lambda r: r.date, reverse=True)

    page = request.args.get('page', 1, type=int)
    per_page = 10
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    # reviews = business.reviews.order_by(Review.date.desc()).slice(start_index, end_index)

    return render_template('business_detail.html', business=business, reviews=reviews, page=page, per_page=per_page, end_index=end_index)

# @app.route('/businesses/<int:business_id>/reviews', methods=['POST'])
# def add_review(business_id):
#     user_id = session.get('user_id')
#     if not user_id:
#         return redirect(url_for('login', current_user=current_user))

#     business = Business.query.get_or_404(business_id)

#     stars = request.form['stars1']
#     review_text = request.form['review']
#     review_date = datetime.datetime.now()

#     review = Review(user_id=user_id, business_id=business_id, stars=stars, text=review_text, date=review_date)
#     db.session.add(review)
#     db.session.commit()

#     return redirect(url_for('business_detail', business_id=business.id, current_user=current_user))

# Route to handle the API call to get menu data for a restaurant
@app.route('/get_menu/<restaurant_name>')
def get_menu(restaurant_name):
    # print("Hello")
    # Call the pylunch API to get the restaurant's menu in CSV format
    api_url = 'https://pylunch.herokuapp.com/api/menus?restaurant=' + restaurant_name
    response = requests.get(api_url)

    # Check for errors with the API call
    if response.status_code != 200:
        return 'Error: Failed to retrieve menu data from API'
    
    # # print(response.content)
    # menu_data = response.json()['data']

    # Check for errors with the API response
    try:
        menu_data = response.json()['data']
    except:
        return 'Error: Invalid response from API'

    # Convert the API response to CSV format
    csv_data = io.StringIO()
    csv_writer = csv.writer(csv_data)
    csv_writer.writerow(['Item', 'Price', 'Image URL'])
    for item in menu_data:
        csv_writer.writerow([item['name'], item['price'], item['image']])
    csv_data.seek(0)

    # Return the CSV data as a response
    return csv_data.getvalue(), {'Content-Type': 'text/csv', 'Content-Disposition': 'attachment; filename=menu.csv'}

# Route to handle the button click on the business_detail.html page
@app.route('/get_menu', methods=['POST'])
def handle_menu_request():
    # Get the restaurant name from the form data
    restaurant_name = request.form['restaurant_name']

    # Call the API to get the menu data
    menu_data_csv = requests.get('http://localhost:5000/get_menu/' + restaurant_name).text

    # Parse the CSV data into a list of menu items
    menu_data = []
    reader = csv.reader(io.StringIO(menu_data_csv))
    next(reader)  # skip header row
    # for row in reader:
    #     menu_data.append({
    #         'name': row[0],
    #         'price': row[1],
    #         'image': row[2],
    #     })
    for row in reader:
        if len(row) >= 3:
            menu_data.append({'name': row[0], 'price': row[1], 'image': row[2]})
        # print(menu_data)

    # print(menu_data)
    # Render the menu.html template with the menu data
    return render_template('menu.html', restaurant_name=restaurant_name, menu_data=menu_data)

if __name__ == '__main__':
    app.run(debug=True)