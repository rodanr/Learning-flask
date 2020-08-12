import sqlite3
from flask_restful import Resource, reqparse
class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    #classmethod takes class as first argument where methods takes instance of class as first argument
    @classmethod
    def find_by_username(cls, username):
    	connection = sqlite3.connect('data.db')
    	cursor = connection.cursor()
    	#WHERE works as filter in SQL
    	query = "SELECT * FROM users WHERE username=?"
    	#should pass tuple to replace the ? sign
    	#(username,) means tuple with single element where , sign is must if no , sign python thinks as useless bracket
    	#storing the filter rows into result variable
    	result = cursor.execute(query, (username,))
    	#Fetches the first row with the given username as given in filter above
    	my_row = result.fetchone()#returns None if there are no rows
    	#if my_row is not None
    	if my_row:
    		user = cls(*my_row)#equivalent to 'user = User(my_row[0], my_row[1], my_row[2])'
    	else:
    		user = None
    	connection.close()#No things to commit inside the db file so not using connection.commit()
    	return user

    @classmethod
    def find_by_userid(cls, userid):
    	connection = sqlite3.connect('data.db')
    	cursor = connection.cursor()
    	query = "SELECT * FROM users WHERE id=?"
    	result = cursor.execute(query, (userid,))
    	my_row = result.fetchone()
    	if my_row:
    		user = cls(*my_row)
    	else:
    		user = None
    	connection.close()
    	return user

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type = str, required = True, help = "This field cannot be left empty")
    parser.add_argument('password', type = str, required = True, help = "This field cannot be left empty")

    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_by_username(data['username']) is not None:
            return {"message":"user with the name '{}' already exists".format(data['username'])}, 400
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message":"User created successfully"}, 201
