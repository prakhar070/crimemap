#python script to handle the logic of our main applicaition
from dbhelper import DBHelper
from flask import Flask
from flask import render_template
from flask import request
import json
import datetime
import dateparser
import string 

app = Flask(__name__)
DB  = DBHelper()
categories = ['mugging','break-in']


def format_date(userdate):
	#returns none if not possible to parse
	date = dateparser.parse(userdate)
	try:
		return datetime.datetime.strftime(date, "%Y-%m-%d")
	except TypeError:
		return None

def sanitize_string(userinput):    
	whitelist = string.letters + string.digits + " !?$.,;:-'()&"    
	return filter(lambda x: x in whitelist, userinput) 

@app.route("/")
def home(error = None):
	try:
		crimes = DB.get_all_crimes()
		crimes = json.dumps(crimes)
	except Exception as e:
		print(e)
		crimes = None
	return render_template("home.html", crimes=crimes, categories= categories,error_message= error)


@app.route("/clear")
def clear():
	try:
		DB.clear_all()
	except Exception as e:
		print(e)
	return home()


@app.route("/submitcrime", methods=['POST'])
def submitcrime():
	category = request.form.get("category")
	if not category in categories:
		return home()
	date = format_date(request.form.get("date"))
	if not date:
		return home("Invalid date. Please use yyyy-mm-dd format ")
	try:
		latitude = float(request.form.get("latitude"))
		longitude = float(request.form.get("longitude"))
	except ValueError:
		return home()
	description = request.form.get("description")
	description = sanitize_string(description)
	DB.add_crime(category, date, latitude, longitude, description)
	return home()

if __name__=='__main__':
	app.run(port=5000, debug=True)

