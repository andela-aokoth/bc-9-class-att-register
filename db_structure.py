import os
import sys
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Student(Base):
	__tablename__ = 'students'
	student_id = Column(Integer, primary_key=True)
	first_name = Column(String(50), nullable=False)
	last_name = Column(String(50), nullable=False)

	def __repr__(self):
		return "Student: '{}' '{}'".format(self.first_name, self.last_name)

class Classes(Base):
	__tablename__ = 'classes'

	class_id = Column(Integer, primary_key=True)
	subject = Column(String(50), nullable=False)

	def __repr__(self):
		return "Class: '{}'".format(self.subject)


engine = create_engine("sqlite:///register.db")

Base.metadata.create_all(engine)