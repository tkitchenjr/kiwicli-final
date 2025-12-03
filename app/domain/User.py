from database import Base
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import mapped_column

#define User class
class User(Base):
#	def __init__(self, username:str, password:str, firstname:str, lastname:str, balance:float):
#		self.username = username
#		self.password = password
#		self.firstname = firstname
#		self.lastname = lastname
#		self.balance = balance

	__tablename__ = "Users"
	username = mapped_column(String(50), primary_key=True, nullable=False)
	password = mapped_column(String(100), nullable=False)
	firstname = mapped_column(String(50), nullable=False)
	lastname = mapped_column(String(50), nullable=False)
	balance = mapped_column(Float, nullable=False)

def __str__(self):
	return f"User(username={self.username}, firstname={self.firstname}, lastname={self.lastname}, balance={self.balance})"