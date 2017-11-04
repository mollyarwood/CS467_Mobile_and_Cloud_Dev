#!/usr/bin/env python2
#***************************************************************
 #Name: Molly Arwood
 #Term: Fall 2017
 #Class: CS_496_Mobile/Cloud
 #assignment 3: OAuth 2.0 implementation
#**************************************************************

import os
import webapp2
import json
import jinja2
import hashlib
import urlparse
import urllib
from google.appengine.ext import ndb
from google.appengine.api import app_identity
from google.appengine.api import urlfetch
import baseHandler

#create a state variable
state = hashlib.sha256(os.urandom(1024)).hexdigest()


class authHandler(baseHandler.BaseHandler):
	
	def get(self):
		self.render_template('login.html')


	def post(self):
		username_entered = self.request.get('username')

		#get clientID info from JSON file
		inFile = open('GoogleOAuthData.json', 'r')
		json_decode = json.load(inFile)
		clientID = json_decode['web']['client_id']
#		clientID = client_id



		authorize_url = str('https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=' + clientID)
		authorize_url = authorize_url + str('&redirect_uri=https://cs496assign3arwoodm.appspot.com/token&scope=email&access_type=offline&state=' + state)
		#authorize_url = authorize_url + str('&redirect_uri=http://localhost:8080/token&scope=email&access_type=offline&state=' + state)

		self.redirect(authorize_url)


class tokenHandler(baseHandler.BaseHandler):

	def get(self):
		stateResp = self.request.get('state')
		if stateResp != state:
			self.response.out.write("Invalid State.")


		elif self.request.get('error'):
			self.responsee.out.write("Not allowed to access stuff\n")

		else:


			#********************************
			#post to google's token site
			#********************************

			#get auth code sent back
			authResp = self.request.get('code')

			#google's token api site
			tokenSite = 'https://www.googleapis.com/oauth2/v4/token'

			#get clientID info from JSON file
			inFile = open('GoogleOAuthData.json', 'r')
			json_decode = json.load(inFile)
			clientID = json_decode['web']['client_id']
			clientSecret = json_decode['web']['client_secret']
#			clientID = client_id
#			clientSecret = client_secret
			headers = {
				'Content-Type' : 'application/x-www-form-urlencoded'
			}

			payload = {
				'code' : authResp,
				'client_id' : clientID,
				'client_secret' : clientSecret,
				'redirect_uri' : 'https://cs496assign3arwoodm.appspot.com/token',
				#'redirect_uri' : 'http://localhost:8080/token',
				'grant_type' : 'authorization_code'
			}


			result = urlfetch.fetch(url=tokenSite, payload = urllib.urlencode(payload), headers=headers, method=urlfetch.POST)
			respData = json.loads(result.content)
			access_token = respData['access_token']
			header_auth_line = "Bearer " + access_token
			emailSite = 'https://www.googleapis.com/plus/v1/people/me'


			#*********************************
			#ask for user's email
			#*********************************
			headers = {
				'Authorization' : header_auth_line
			}

			result2 = urlfetch.fetch(url=emailSite, headers=headers)
			respData2 = json.loads(result2.content)

			#get variables
			firstName  = respData2['name']['givenName']
			lastName = respData2['name']['familyName']
			#email = respData2['emails'][0]['value']
			url = respData2['url']

			redirectString = '/homePage?firstName=' + firstName + '&lastName=' + lastName + '&url=' + url
			self.redirect(redirectString)



class homePageHandler(baseHandler.BaseHandler):

	def get(self):
	
		firstName = self.request.get('firstName')
		lastName = self.request.get('lastName')
		url = self.request.get('url')

		self.render_template('homePage.html', firstName=firstName, lastName=lastName, url=url, state=state)		

