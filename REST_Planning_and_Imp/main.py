#!/usr/bin/env python2
#***************************************************************
 #Name: Molly Arwood
 #Term: Fall 2017
 #Class: CS_496_Mobile/Cloud
 #assignment 2: REST planning and implementation
#**************************************************************

import os
import webapp2
import jinja2
import json
from google.appengine.ext import ndb
from python.public import boatHandler
from python.public import slipHandler
from python.public import boatArrivalHandler


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
	('/boats', boatHandler.BoatHandler),
	('/boats/(.*)', boatHandler.BoatHandler),
	('/slips', slipHandler.SlipHandler),
	('/slips/(.*)/boat', boatArrivalHandler.BoatArrivalHandler),
	('/slips/(.*)', slipHandler.SlipHandler)
], debug=DEBUG)