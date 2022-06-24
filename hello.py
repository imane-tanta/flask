from flask import Flask, render_template




#Creat flask Instance
app = Flask(__name__)

#creat rout decorator html....
@app.route('/')

#def index():
#	return "<h1> Hello Woooorld!</h1>"

def index():
	first_name = "Imane"
	return render_template("index.html", first_name=first_name)

#localhost:5000/user/Imane
@app.route('/user/<name>')

def user(name):
	return render_template("user.html", user_name=name)

#Creaat Error 404Opages

#Invalid URL
@app.errorhandler(404)
def page_note_found(e):
	return render_template("404.html"), 404

#Internal server Error 
@app.errorhandler(500)
def page_note_found(e):
	return render_template("404.html"), 500