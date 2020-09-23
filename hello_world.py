from flask import Flask, request, make_response,render_template 
from flask_sqlalchemy import SQLAlchemy 


# initializing Flask app 
app = Flask(__name__) 

@app.route('/api/hello')
def hello_world():
	return 'Hello, Xinwei! 2025'

# Google Cloud SQL (change this accordingly) 
PASSWORD = "12345678"
PUBLIC_IP_ADDRESS = "34.72.39.132"
DBNAME = "Students"
PROJECT_ID ="stellar-chariot-290118"
INSTANCE_NAME ="student-account-847"

# configuration 
#app.config["SECRET_KEY"] = "123455678"
app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

db = SQLAlchemy(app) 

# User ORM for SQLAlchemy 
class Users(db.Model): 
	id = db.Column(db.Integer, primary_key = True, nullable = False) 
	name = db.Column(db.String(50), nullable = False) 
	email = db.Column(db.String(50), nullable = False, unique = True) 


@app.route('/api/form', methods=['GET', 'POST']) #allow both GET and POST requests
def form():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        sid = request.form.get('sid')
        firstname = request.form.get('firstname') 
        lastname = request.form.get('lastname') 
        email = request.form.get('email') 
        address = request.form.get('address')  
        gpa = request.form.get('gpa')  

        return '''<h5>StudentID: {}</h5>
		          <h5>First Name: {}</h5>
                  <h5>Last Name: {}</h5>
                  <h5>Email: {}</h5>
                  <h5>Address: {}</h5>
                  <h5>GPA: {}</h5>

                  '''.format(sid, firstname, lastname, email, address, gpa)


    return '''<form method="POST">
				<h2> Student Info </h2>
                Student ID: <input type="text" name="sid"><br>
                First Name: <input type="text" name="firstname"><br>
                Last Name: <input type="text" name="lastname"><br>
                Email: <input type="text" name="email"><br>
                Mailing Address: <input type="text" name="address"><br>
                GPA: <input type="text" name="gpa"><br>


                <input type="submit" value="Submit"><br>
              </form>'''


@app.route('/api/add', methods =['GET', 'POST']) 
def add(): 
	# geting name and email 
	name = request.get_json().get('name') 
	email = request.get_json().get('email') 

	# checking if user already exists 
	user = Users.query.filter_by(email = email).first() 
	db.create_all()

	if not user: 
		try: 
			# creating Users object 
			user = Users( 
				name = name, 
				email = email 
			) 

			# adding the fields to users table 
			db.session.add(user) 
			db.session.commit()
			print("LALALALA")
			# response 
			responseObject = { 
				'status' : 'success', 
				'message': 'Sucessfully registered.'
			} 

			return make_response(responseObject, 200) 
		except Exception as e: 
			responseObject = { 
				'status' : 'fail', 
				'message': 'Error: {}'.format(e)
			} 

			return make_response(responseObject, 400) 
	else: 
		# if user already exists then send status as fail 
		responseObject = { 
			'status' : 'fail', 
			'message': 'User already exists !!'
		} 

		return make_response(responseObject, 403) 

@app.route("/api/result")
def result():
	users = Users.query.all() 
	return render_template('template.html', users=users)

@app.route('/api/view') 
def view(): 
	# fetches all the users 
	users = Users.query.all() 
	response = list() 

	for user in users: 
		response.append({ 
			"name" : user.name, 
			"email": user.email 
		}) 

	return make_response({ 
		'status' : 'success', 
		'message': response 
	}, 200)


if __name__ == "__main__": 
	# app.run()
	app.run(debug=True)
