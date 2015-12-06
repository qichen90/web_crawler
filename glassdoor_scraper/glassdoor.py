__author__ = 'QiChen'
'''scraped the interview reviews of certain positions from specific glassdoor websites.'''

import urllib2
import re
import sys
import HTMLParser
from db_setup import Base, Interviews
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class GlassDoor:
	engine = create_engine('sqlite:///interviews.db')
	Base.metadata.bind = engine
	DBsession = sessionmaker(bind=engine)
	session = DBsession()

	# initializing...
	def __init__(self):
		self.agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'
		# initialize headers
		self.headers = {'User-agent': self.agent}
		self.allInfo = []
		self.pageNum = 1
		self.total_reviews = 0
		self.count = 0
		self.company = ""

	# get code of one web page
	def getPage(self, url):
		try:
			request = urllib2.Request(url, headers=self.headers)
			response = urllib2.urlopen(request)
			pageCode = response.read().decode('utf-8')
			return pageCode
		except urllib2.URLError, e:
			if hasattr(e, "reason"):
				print e.reason

	# get the information wanted
	def getInterviewInfo(self,url,year):
		pageCode = self.getPage(url)
		if not pageCode:
			print "Failed to load page..."
			return None

		# regular expression
		pattern = re.compile('<time.*?>(.*?)</time>.*?<p.*?interviewDetails.*?>(.*?)</p>',re.S)
		pattern_per_question = re.compile('<span.*?interviewQuestion.*?>(.*?)</span>', re.S)
		pattern_for_question = re.compile('<time.*?>(.*?)</time>.*?<div.*?interviewQuestions.*?>.*?<ul.*?>(.*?)</ul>', re.S)

		
		# find all the content wanted
		contents = re.findall(pattern, pageCode)
		questions = re.findall(pattern_for_question, pageCode)
		i = 0
		for content in contents:
			date = content[0]
			date = date.lstrip().replace(',', '') # reformat the date string
			if int(date[-4:]) <= int(year):
				return True

			date2 = questions[i][0].lstrip().replace(',', '')
			if date == date2: # has posted question in this interview
				# find all questions in this interview
				qs = re.findall(pattern_per_question, questions[i][1])
				i += 1
				all_questions = ""
				for q in qs:
					q = re.sub('\&nbsp;', '', q) # remove the weird substring from the end
					all_questions += q + "\n"
				self.allInfo.append("Date: " + date + "\n" + "Interview: \n" 
									+ content[1] + "\n" + "Question: \n" + all_questions)
				# update the database
				interview = Interviews(company=self.company,year=int(date[-4:]),review=content[1],question=all_questions)
				self.session.add(interview)
				self.session.commit()
			else:
				self.allInfo.append("Date: " + date + "\n" 
									+ "Interview: \n" + content[1] + "\n")
				# update the database
				interview = Interviews(company=self.company,year=int(date[-4:]),review=content[1])
				self.session.add(interview)
				self.session.commit()
			
		self.count += len(contents)
		return False
		
	# get the basic information: the total number of reviews and the company name
	def getBasicInfo(self,url):
		pageCode = self.getPage(url)
		if not pageCode:
			print "Failed to load page..."
			return None
		
		# get the number of total reviews
		review_count = re.compile('<div.*?basicForm.*?>.*?<h2.*?tightTop.*?>(.*?)<span.*?>.*?</span>', re.S)
		counts = re.findall(review_count, pageCode)
		tmp = counts[0].split()
		self.total_reviews = int(tmp[0])

		# get the company name
		pattern_company = re.compile('.*?Interview/(.*?)-.*?', re.S)
		tmp = re.findall(pattern_company, url)
		self.company = tmp[0]

	# get part of the result
	def getAddressInfo(self, url):
		address =[]
		pattern = re.compile('.*?,.*?,(.*?).htm')
		part1 = re.findall(pattern, url)
		
		part2 = url[:-5-len(part1)]
		address.append(part2)
		address.append(part1[0])
		return address 

	# check whether the new url can be open
	def loadPages(self, url):
		try:
			request = urllib2.Request(url, headers=self.headers)
			response = urllib2.urlopen(request)
			return True
		except urllib2.URLError, e:
			return False

	# write all review into file
	def writeToFile(self):
		reviews = open(self.company, 'a')
		for info in self.allInfo:
			# replace some unicode manually
			info = info.replace(u'\u2019', "'")
			info = info.replace(u'\u2013', "-")
			info = info.replace(u'\u2026', "...")

			info = HTMLParser.HTMLParser().unescape(info)
			reviews.write(info)

			reviews.write("\n")
		reviews.close()
		print "Finished writing!"

		# begin to get all the reviews...
	def start(self, url, year):
		# seperate the url into two parts
		print "Getting URL information..."
		address = self.getAddressInfo(url)

		print "Getting page information..."
		self.getBasicInfo(url)

		print "Collecting interview reviews..."
		doNotStop = True
		while doNotStop:
			# get info from each page
			stop = self.getInterviewInfo(url, year)
			if stop:
				break
			# generate new url
			self.pageNum += 1
			url = address[0] + address[1] + "_IP" + str(self.pageNum) + ".htm"

			# termination conditions
			if self.count == self.total_reviews:
				doNotStop = False
				print "Got all interview reviews!"
			elif not self.loadPages(url):
				doNotStop = False
				print "Cannot get the page."

		print "Writing to file..."
		self.writeToFile()


gd = GlassDoor()
url = raw_input('Enter the website: ')
year = raw_input('The year not later than: ')
# url = "http://www.glassdoor.com/Interview/Cvent-Software-Engineer-Interview-Questions-EI_IE104683.0,5_KO6,23.htm"
# year = 2012
gd.start(url, year)
