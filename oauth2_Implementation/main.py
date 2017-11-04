#!/usr/bin/env python2
#***************************************************************
 #Name: Molly Arwood
 #Term: Fall 2017
 #Class: CS_496_Mobile/Cloud
 #assignment 3: OAuth2 implementation
#**************************************************************

import os
import webapp2
import json
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import app_identity
import loginHandler



class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.write("hello")


#check to see if program is running on dev server or prod
DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

#allow webapp2 to do a patch request
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods



app = webapp2.WSGIApplication([
	('/', MainPage),
	('/login', loginHandler.authHandler),
	('/token', loginHandler.tokenHandler),
	('/homePage', loginHandler.homePageHandler)
], debug=DEBUG)