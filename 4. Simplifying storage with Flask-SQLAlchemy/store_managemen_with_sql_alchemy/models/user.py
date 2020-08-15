import sqlite3
from db import db

class UserModel(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80))
	password = db.Column(db.String(80))
	
	def __init__(self, username, password):
		self.username = username
		self.password = password
	
	def save_to_db(self):
		db.session.add(self)
		db.session.commit()
		
	#classmethod takes class as first argument where methods takes instance of class as first argument
	@classmethod
	def find_by_username(cls, username):
		return cls.query.filter_by(username=username).first()#returs as class object

	@classmethod
	def find_by_userid(cls, userid):
		return cls.query.filter_by(id=_id).first()