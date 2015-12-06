__author__ = "QiChen"
'''set up the database scheme using SQLAlchemy toolkit, for current version, it only has one table.'''

import os
import sys
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# interview information table
class Interviews(Base):
	__tablename__ = 'interview'

	id = Column(Integer, primary_key=True)
	company = Column(String(250), nullable=False)
	year = Column(Integer, nullable=False)
	review = Column(String, nullable=False)
	question = Column(String)

engine = create_engine('sqlite:///interviews.db')
Base.metadata.create_all(engine)