# This file controls the database functionality.

import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

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
	password = Column(String)
	
	addresses = relationship('Address', back_populates='user', cascade='all, delete, delete-orphan')

	def __repr__(self):
		return "<User(id: '%s', name: '%s', email:'%s', password: '%s')>" % (self.id, self.name, self.email, self.password)
		
class Address(Base):
	__tablename__ = 'addresses'

	id = Column(Integer, primary_key=True)
	email = Column(String, nullable=False)
	user_id = Column(Integer, ForeignKey('users.id'))

	user = relationship('User', back_populates='addresses')

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
	new_user = User(name=name, password=pwd)
	new_user.addresses = [Address(email=email)]
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
def rem(name):
	session = Session()
	res_user = session.query(User).filter(User.name == name).first()
	if res_user == None:
		raise Exception('Record with name "%s" does not exist!' % name)
	else:
		session.delete(res_user)
		session.commit()
	session.close()