
import os
import webapp2
import jinja2
import json
import boatHandler
from google.appengine.ext import ndb


class Slip(ndb.Model):
	slipId = ndb.StringProperty()
	number = ndb.StringProperty()
	current_boat = ndb.StringProperty()
	arrival_date = ndb.StringProperty()
	#departure_history = ndb.JsonProperty(repeated=True)

class SlipHandler(webapp2.RequestHandler):
	def post(self):
		#loading info that was entered in post request
		slip_data = json.loads(self.request.body)
		#creating the new slip
		new_slip = Slip(slipId="",number=slip_data['number'], 
					current_boat="", 
					arrival_date="")
		#adding the instance to the datastore and auto-gen key
		new_slip.put()
		#add generated key to id field
		new_slip.slipId = new_slip.key.urlsafe()
		new_slip.put()
		#converting boat to dictionary
		slip_dict = new_slip.to_dict()
		#adding self reference to slip
		slip_dict['self'] = '/slips/' + new_slip.slipId		
		#displaying results as response to post
		self.response.write(json.dumps(slip_dict))


	def get(self, id=None):
		if id:
			#if id was specified in url, get actual id.
			sId = ndb.Key(urlsafe=id).get()
			sId_dict = sId.to_dict()
			sId_dict['self'] = '/slips/' + id 
			self.response.write(json.dumps(sId_dict))
		else:
			slip_d = json.dumps([i.to_dict() for i in Slip.query()])
			self.response.write(slip_d)


	#to modify slip properties
	def patch(self, id=None):
		if id:
			#if id was specified in url, get actual id.
			sId = ndb.Key(urlsafe=id).get()
			slip_data = json.loads(self.request.body)

			if sId:
				if 'number' in slip_data:
					sId.number = slip_data['number']

				sId.put()

				self.response.write(json.dumps(sId.to_dict()))
		else:
			self.response.out.write("Error: ID not specifed in URL")


	#to replace slip
	def put(self, id=None):
		if id:
			#if id was specified in url, get actual id.
			replaced_slip = ndb.Key(urlsafe=id).get()

			if replaced_slip:	
				#loading info that was entered in post request
				slip_data = json.loads(self.request.body)
				#replacing the new slip
				replaced_slip.number=slip_data['number']
				replaced_slip.current_boat=slip_data['current_boat'] 
				replaced_slip.arrival_date=slip_data['arrival_date']
				replaced_slip.slipId = id
				#adding the instance to the datastore and auto-gen key
				replaced_slip.put()
				#converting slip to dictionary
				slip_dict = replaced_slip.to_dict()
				#adding self reference to slip
				slip_dict['self'] = '/slips/' + replaced_slip.slipId
				#displaying results as response to post
				self.response.write(json.dumps(slip_dict))



	def delete(self, id=None):
		if id:
			#if id was specified in url, get actual id.
			sId = ndb.Key(urlsafe=id).get()
			if sId:
				if sId.current_boat != "":
					bId = sId.current_boat
					boat = ndb.Key(urlsafe=bId).get()
					boat.at_sea = True
					boat.put()
				ndb.Key(urlsafe=id).delete()
		else:
			self.response.out.write("Error: ID not specifed in URL")