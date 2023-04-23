from flask import  render_template, request, redirect, url_for, flash, session, make_response
from flask_login import login_user
from TasteMate import app
from TasteMate.Models import *
from TasteMate.Forms import *
from TasteMate.BackEnd import *
import datetime
import random
import requests
import csv
import io
import json
from TasteMate.Models import *
from TasteMate.get_menu import *
import pickle
from flask_login import login_required, current_user, login_user, logout_user
# import oidc



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
        user_id = request.form['user_id']
        # print(userid)
        password = request.form['password']
        # print(userid)
        # print(password)
        # if validate_user(userid, password):
        user = Users.query.filter_by(user_id=user_id).first()
        if user and user.password == password:
            # flash('Congratulations! You have successfully signed in')
            login_user(user, remember=False)
            print(user)
            return redirect(url_for('home', user=user.user_id))
        else:
            flash('Incorrect User ID or Password', 'danger')
            return redirect('/')
    return render_template('login.html', title='Log In', form=form, current_user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # user = Users(username=form.username.data, password=form.password.data)
        user_id = request.form['user_id']
        user = Users.query.filter_by(user_id = user_id).first()
        print(user)
        if user:
            print("if")
            flash('Error! User already exists.', 'danger')
            return redirect(url_for('register'))
        else:
            print("inside else")
            username = request.form['username']
            password = request.form['password']
            print(password)
            confirm_password = request.form['confirm_password']
            print(confirm_password)
            if password != confirm_password:
                flash('Error! Passwords do not match.', 'danger')
                return redirect(url_for('register'))
            new_user = Users(user_id,username,password)
            db.session.add(new_user)
            db.session.commit()
            flash('Success! Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form, current_user=current_user)

@app.route('/home/<user>')
@login_required
# @oidc.accept_token(True)
def home(user=None):
    # print(user)
    if user:
        # print(user.user_id)
        businesses = Business.query.all()
        random_businesses = random.sample(businesses, k=4)
        # user = Users.query.filter_by(id=session['user_id']).first()
        user1 = Users.query.filter_by(user_id=user).first()
        return render_template('home.html', title='Home', user=user1, random_businesses=random_businesses, current_user=current_user)
    else:
        return redirect(url_for('login', current_user=current_user))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    session.permanent = False
    return redirect(url_for('login', current_user=current_user))

@app.route('/businesses')
def businesses():
    catlist = []
    with open("Categories.pkl",'rb') as f:
        catlist = pickle.load(f)

    # print(catlist)
    
    # Retrieve search parameters from the URL query string
    search_query = request.args.get('search_query', '')
    showopen = False
    distance = 20
    filterdistance = False

    if request.args.get('open-businesses-checkbox') == 'on':
        showopen = True

    print(showopen)

    if request.args.get('choose-distance') == 'on':
        filterdistance = True
        distance = request.args.get('distance', '')

    catlist1 = request.args.get('cuisine_type')

    print(catlist1)
    if not catlist1:
        catlist1 = []
    

    # Query the businesses based on the search parameters
    # businesses = Business.query.filter(
    #     Business.name.like(f'%{search_query}%'),
    #     Business.hours.like(f'%{opening_hours}%'),
    #     Business.categories.like(f'%{cuisine_type}%'),
    #     # Business.attributes.like(f'%{price_range}%')
    # ).all()

    # Get the current page from the request arguments or default to 1
    page = request.args.get('page', 1, type=int)

    # Set the number of businesses to display per page
    per_page = 10

    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    # if catlist1:
    #     businesses = search_buss(name=search_query, catlist=catlist1, showopen=showopen, dist=distance, filterdist=filterdistance)
    # else:
    #     businesses = search_buss(name=search_query, catlist=[], showopen=showopen, dist=distance, filterdist=filterdistance)
    businesses = search_buss(name=search_query, catlist=catlist1, showopen=showopen, dist=distance, filterdist=filterdistance)
    print(len(businesses))
    return render_template('businesses.html', businesses=businesses, catlist=catlist, page=page, per_page=per_page, end_index=end_index, current_user=current_user)
    # return render_template('businesses.html', businesses=businesses, catlist=catlist, page=page, per_page=per_page, current_user=current_user)
    

@app.route('/businesses/<string:business_id>')
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

@app.route('/businesses/<string:business_id>/reviews/<string:review_id>', methods=['POST'])
def insert_delete_review(business_id, review_id='None'):
    # user_id = session.get('user_id')
    # if not user_id:
    #     return redirect(url_for('login', current_user=current_user))

    if not current_user.is_authenticated:
        return redirect(url_for('login', current_user=current_user))

    # business = Business.query.get_or_404(business_id)
    # print(review_id)
    if review_id == 'None':
        stars = request.form['stars1']
        review_text = request.form['review']
        review_date = datetime.datetime.now()

        add_review(user_id=current_user.user_id, business_id=business_id, stars=stars, text=review_text, date=review_date)
    else:
        delete_review(review_id=review_id)

    return redirect(url_for('business_detail', business_id=business_id, current_user=current_user))


@app.route('/get_menu/<string:business_name>/<string:business_state>', methods=['POST'])
def handle_menu_request(business_name, business_state):
    # Get the restaurant ID from the request parameters
    # restaurant_id = request.args.get('restaurant_id')
    try:
        menu = get_menu(business_name, business_state)
    except:
        menu = None
    print(menu)

    page = request.args.get('page', 1, type=int)

    # Set the number of businesses to display per page
    # per_page = 10

    # start_index = (page - 1) * per_page
    # end_index = start_index + per_page

    # Render the menu template with the menu items
    return render_template('menu.html', menu=menu, page=page)