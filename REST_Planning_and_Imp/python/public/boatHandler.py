
import os
import webapp2
import jinja2
import json
import slipHandler
from google.appengine.ext import ndb


class Boats(ndb.Model):
	boatId = ndb.StringProperty()
	name = ndb.StringProperty(required=True)
	boat_type = ndb.StringProperty()
	length = ndb.IntegerProperty()
	at_sea = ndb.BooleanProperty()



class BoatHandler(webapp2.RequestHandler):
	#to add a boat
	def post(self):
		#loading info that was entered in post request
		boat_data = json.loads(self.request.body)
		#creating the new boat
		new_boat = Boats(name=boat_data['name'], boat_type=boat_data['boat_type'], 
					length=boat_data['length'], at_sea=True)
		#adding the instance to the datastore and auto-gen key
		new_boat.put()
		#add generated key to id field
		new_boat.boatId = new_boat.key.urlsafe()
		new_boat.put()
		#converting boat to dictionary
		boat_dict = new_boat.to_dict()
		#adding self reference to boat
		boat_dict['self'] = '/boats/' + new_boat.boatId
		#displaying results as response to post
		self.response.write(json.dumps(boat_dict))


	#to list a specific boat and a list of boats
	def get(self, id=None):
		if id:
			#if id was specified in url, get actual id.
			bId = ndb.Key(urlsafe=id).get()
			bId_dict = bId.to_dict()
			bId_dict['self'] = '/boats/' + id 
			self.response.write(json.dumps(bId_dict))
		else:
			boat_d = json.dumps([i.to_dict() for i in Boats.query()])
			self.response.write(boat_d)
				

	#to modify boat properties and set to sea
	def patch(self, id=None):
		if id:
			#if id was specified in url, get actual id.
			bId = ndb.Key(urlsafe=id).get()
			boat_data = json.loads(self.request.body)

			if bId:
				if 'name' in boat_data:
					bId.name = boat_data['name']

				if 'boat_type' in boat_data:
					bId.boat_type = boat_data['boat_type']

				if 'length' in boat_data:
					bId.length = boat_data['length']

				bId.put()
				#put to dict here with self reference
				self.response.write(json.dumps(bId.to_dict()))

		else:
			self.response.out.write("Error: ID not specifed in URL")


	#to replace boat
	def put(self, id=None):
		if id:
			#if id was specified in url, get actual id.
			replaced_boat = ndb.Key(urlsafe=id).get()

			if replaced_boat:	
				#loading info that was entered in post request
				boat_data = json.loads(self.request.body)
				#getting replaced_boat's current at_sea status
				sea_status = replaced_boat.at_sea
				#replacing the new boat
				replaced_boat.name=boat_data['name']
				replaced_boat.boat_type=boat_data['boat_type'] 
				replaced_boat.length=boat_data['length']
				replaced_boat.at_sea=boat_data['at_sea']
				replaced_boat.boatId = id
				#adding the instance to the datastore and auto-gen key
				replaced_boat.put()
				#converting boat to dictionary
				boat_dict = replaced_boat.to_dict()
				#adding self reference to boat
				boat_dict['self'] = '/boats/' + replaced_boat.boatId


				#If at_sea was changed - update the slip accordintly
				if  replaced_boat.at_sea != sea_status and replaced_boat.at_sea == False:
					for slip in slipHandler.Slip.query(slipHandler.Slip.current_boat == ""):
						if slip.current_boat == "":
							slip.current_boat = id
							slip.arrival_date = "5-6-17"
							slip.put()
							break
						else:
							self.response.set_status(403)

				if replaced_boat.at_sea != sea_status and replaced_boat.at_sea == True:
					for slip in slipHandler.Slip.query(slipHandler.Slip.current_boat == ""):
						if slip.current_boat == id:
							slip.current_boat = ""
							slip.arrival_date = ""
							slip.put()
							break
						else:
							self.response.sea_status(403)

				#displaying results as response to post
				self.response.write(json.dumps(boat_dict))


	def delete(self, id=None):
		if id:
			#if id was specified in url, get actual id.
			bId = ndb.Key(urlsafe=id).get()
			if bId:
				if bId.at_sea == False:
					#remove boat from slip if applicable
					for slip in slipHandler.Slip.query(slipHandler.Slip.current_boat == id):
						if slip.current_boat:
							slip.current_boat = ""
							slip.arrival_date = ""
							slip.put()

			#delete boat
			ndb.Key(urlsafe=id).delete()
		else:
			self.response.out.write("Error: ID not specifed in URL")