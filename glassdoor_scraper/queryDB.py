__author__ = "QiChen"
'''database query class: is used to access the data in the database'''

from db_setup import Base, Interviews
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class queryDB:
	engine = create_engine('sqlite:///interviews.db')
	Base.metadata.bind = engine
	DBsession = sessionmaker(bind=engine)
	session = DBsession()

	def __init__(self):
		'''init function'''

	def find(self,company,year):
		'''get the target data by querying interviews.db'''
		if company != "" and year != "":
			interviews = self.session.query(Interviews).filter_by(company=company, year=int(year)).all()
			print "-------------- Interviews of " + company + " in " + year + "-------------"
			for i in  interviews:
				print "#########"
				print "Review: " + i.review + "\n"
				if i.question != "":
					print "Questions: " + i.question
		elif company != "":
			interviews = self.session.query(Interviews).filter_by(company=company).all()
			print "Interviews of " + company + "."
			for i in  interviews:
				print "#########"
				print "Review: " + i.review + "\n"
				if i.question != "":
					print "Questions: " + i.question
		elif year != "":
			interviews = self.session.query(Interviews).filter_by(year=int(year)).all()
			print "Interviews in " + year + "."
			for i in  interviews:
				print "#########"
				print "Review: " + i.review + "\n"
				if i.question != "":
					print "Questions: " + i.question

company = raw_input("Type in the company that you want to get: ")
year = raw_input("The year you want to find: ")
queryDB().find(company,year)



