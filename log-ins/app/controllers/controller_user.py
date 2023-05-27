from app import app
from flask import render_template, redirect, request, session
from app.models.model_user import User


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users/login')
def login():
    pass

@app.route('/users/new_user')
def new_user():
    return render_template('register.html')

@app.route('/users/register')
def register():
    pass