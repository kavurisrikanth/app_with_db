# This file controls the database functionality.

import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

'''
Create the database.
'''
def createDB():
	engine = create_engine('sqlite:///app.db')
	return engine
	
Base = declarative_base()

class User(Base):
	__tablename__ = 'users'
	
	id = Column(Integer, primary_key=True)
	name = Column(String)
	email = Column(String)
	password = Column(String)
	
	def __repr__(self):
		return "<User(id: '%s', name: '%s', email:'%s', password: '%s')>" % (self.id, self.name, self.email, self.password)
		
Session = None

'''
Create the table.
'''
def create_table(engine):
	Base.metadata.create_all(engine)
	global Session
	Session = sessionmaker(bind=engine)
	
'''
Add data to database.
'''
def ins(name, email, pwd):
	new_user = User(name=name, email=email, password=pwd)
	session = Session()
	session.add(new_user)
	session.commit()
	session.close()

'''
Extract data from database. Added for debugging.
'''
def view(name):
	session = Session()
	ans_user = session.query(User).filter(User.name == name).first()
	if ans_user == None:
		print ('No such user exists in database')
	else:
		print (ans_user)
	session.close()
	
'''
Deletes records based on email address (?)
'''
def rem(email):
	session = Session()
	res_user = session.query(User).filter(User.email == email).first()
	if res_user == None:
		raise Exception('Email "%s" does not exist!' % email)
	else:
		session.query(User).filter(User.email == email).delete()
		session.commit()
	session.close()