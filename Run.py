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


# login_manager = LoginManager()
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     return Users.query.get(int(user_id))   

from TasteMate import app


if __name__ == '__main__':

    app.run(debug=True)