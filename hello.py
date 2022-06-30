from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
#from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
#from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


 


#Creat flask Instance
app = Flask(__name__)

#Add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "my secret key"
Bootstrap(app)

#Initialize the Database
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



#Creat Model

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(15), unique=True)
	email = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(80))
	phone = db.Column(db.String(13), unique=True)
	city = db.Column(db.String(10))



@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

#Create a String


#Creat class LOGIN
class LoginForm(FlaskForm):
	email = StringField('E-mail', validators=[InputRequired(), Length(min=4, max=40)])
	password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=80)])
	remember = BooleanField('Remember me')	


#Creat class Signup
class RegisterForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
	email = StringField('E-mail', validators=[InputRequired(), Length(min=4, max=40)])
	password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=80)])
	phone = StringField('Phone No.', validators=[InputRequired(), Length(max=5)])
	city = StringField('City', validators=[InputRequired(), Length(min=4, max=15)])
	

#creat rout decorator html....
@app.route('/')
def index():
	return render_template('index.html')

#Creaat Error 404pages

#Invalid URL
@app.errorhandler(404)
def page_note_found(e):
	return render_template("404.html"), 404

#Login 
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			if user.password == form.password.data:
					#login_user(user, remember=form.remember.data):
				return redirect(url_for('dashboard'))
		return '<h1> invalid Email or Password </h1>'
		#return '<h1>' + form.email.data + ' ' + form.password.data + '</h1>'
	return render_template('login.html', form=form)


#Signup  
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = RegisterForm()
	if form.validate_on_submit():
		new_user = User(username=form.username.data, email=form.email.data, phone=form.phone.data, password=form.password.data, city=form.city.data)
		db.session.add(new_user)
		db.session.commit()
		flash("New has been created!")
	#return '<h1> New has been created!</h1>'
		#return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.phone.data + ' ' + form.password.data + ' ' + form.city.data + ' ' + form.confirm.data + '</h1>'
	return render_template('signup.html', form=form)


#Dashboard 



if __name__ == '__main__':
	app.run(debug=True)

