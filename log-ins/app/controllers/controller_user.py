from app import app
from flask import render_template, redirect, request, session, flash
from app.models.model_user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    session.clear()
    return render_template('index.html')


@app.route('/users/login', methods=['POST'])
def login():

    if not User.validate_login(request.form):
        return redirect('/')
    data = {
        'username': request.form['username'],
        'password': request.form['password']
    }
    user_in_db = User.get_by_username(data)
    print(user_in_db.password)
    if not user_in_db:
        flash('Invalid username/password')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, data['password']):
        flash('Invalid username/password')
        return redirect('/')
    session['user_id'] = user_in_db.id
    return render_template('success.html', username=data['username'])


@app.route('/users/new_user')
def new_user():
    return render_template('register.html')


@app.route('/users/register', methods=['POST'])
def register():
    if not User.validate_new_user(request.form):
        return redirect('/users/new_user')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'username': request.form['username'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return render_template('success.html', username=data['username'])
