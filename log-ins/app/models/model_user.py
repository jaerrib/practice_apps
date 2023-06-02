import re
from flask import flash
from app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = 'user_logins'


    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_by_username(cls, data):
        query = 'SELECT * FROM users WHERE username = %(username)s;'
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (username, email, password) \
            VALUES (%(username)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def validate_login(cls, data):
        is_valid = True
        if data['username'] == "" or \
            data['password'] == "":
            flash('All fields required', 'login')
            is_valid = False
        return is_valid

    @classmethod
    def validate_new_user(cls, data):
        is_valid = True
        if data['username'] == "" or \
            data['email'] == "" or \
            data['password'] == "":
            flash('All fields required', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email address', 'register')
            is_valid = False
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) != 0:
            flash('This email already exists', 'register')
            is_valid = False
        return is_valid
