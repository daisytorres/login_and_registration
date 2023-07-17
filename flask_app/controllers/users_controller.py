from flask_app import app
from flask import render_template, redirect, request, session, flash #we will be using session to store the value of the person logged in
from flask_app.models.user_model import User

from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)



#this is the first wireframe that displays the option to register or login
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect ('/dashboard')
    return render_template('index.html')



#create static method for this and hash password
#this is the app route for someone to register and send that into our db
@app.route('/users/register', methods=['POST'])
def register():
    if not User.is_valid(request.form): #first you want to validate the form and then hash
        return redirect ('/')
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hashed_pass
    }
    logged_user_id = User.create(data) #since User.create always returns the id, we create a value to store it
    session['user_id'] = logged_user_id #then we want to store it into session
    return redirect('/dashboard')



#this is the app route that will query our db to validate login fromm
@app.route('/users/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    #checking if the email matches db
    potential_user = User.get_by_email(data)
    if not potential_user:
        flash('Invalid credentials', 'log')
        return redirect('/')
    #checking if password hashed matches
    if not bcrypt.check_password_hash(potential_user.password, request.form['password']):
        flash('Invalid credentials', 'log')
        return redirect('/')
    session['user_id']= potential_user.id
    return redirect('/dashboard')



#this is the route for the user dashboard after creating an account or login
# we are going to make sure the correct user is logged in by using the key the user used to log in -> session['user_id']= potential_user.id
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/') #this is saying if you are not logged in with a matching key, then you are just going to be redirect to the home page
    data = {
        'id' : session['user_id']
    }
    logged_user = User.get_by_id(data)
    return render_template('dashboard.html', logged_user=logged_user)
    # return render_template('dashboard.html', logged_user = User.get_by_id({'id':logged_user_id}))



#this is the route for the user to logout
@app.route('/users/logout')
def logout():
    del session['user_id']
    return redirect ('/')


