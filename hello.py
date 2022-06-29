from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



 


#Creat flask Instance
app = Flask(__name__)

#Add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "my secret key"
Bootstrap(app)

#Initialize the Database
db = SQLAlchemy(app)

#Creat Model

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(15), unique=True)
	email = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(80))
	phone = db.Column(db.String(13), unique=True)
	city = db.Column(db.String(10))

#Create a String


#Creat class LOGIN
class LoginForm(FlaskForm):
	email = StringField('E-mail', validators=[InputRequired(), Length(min=4, max=40)])
	password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
	remember = BooleanField('Remember me')	


#Creat class Signup
class RegisterForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
	email = StringField('E-mail', validators=[InputRequired(), Length(min=4, max=40)])
	password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
	phone = StringField('Phone No.', validators=[DataRequired(), Length(max=13)])
	city = StringField('City', validators=[InputRequired(), Length(min=4, max=15)])
	confirm = PasswordField('Repeat Password')

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
				return redirect(url_for('dashboard'))
		return '<h1> invalid Email or Password </h1>'
		#return '<h1>' + form.email.data + ' ' + form.password.data + '</h1>'
	return render_template('login.html', form=form)


#Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	username = None
	form = RegisterForm()

	if form.validate_on_submit():
		new_user = User(username=form.username.data, email=form.email.data, phone=form.phone.data, password=form.password.data, city=form.city.data, confirm=form.confirm.data)
		db.session.add(new_user)
		db.session.commit()
	#sername = form.username.data = ''
	#orm.username.data = ''
	#orm.email.data = ''
	#orm.phone.data = ''
#form.password.data = ''
#form.city.data = ''
#form.confirm.data = ''
##lash("yeeeep")
##ur_user = User.query.order_by(user.date_added)

		#return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.phone.data + ' ' + form.password.data + ' ' + form.city.data + ' ' + form.confirm.data + '</h1>'
	return render_template('signup.html', form=form)
	#	nuserame=username,
#	our_user=our_user)

#Dashboard 
@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')


if __name__ == '__main__':
	app.run(debug=True)

