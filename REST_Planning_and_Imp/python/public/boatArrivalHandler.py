
import os
import webapp2
import jinja2
import json
import boatHandler
import slipHandler
from google.appengine.ext import ndb


class BoatArrivalHandler(webapp2.RequestHandler):

	#get boat info that's occupying slip
	def get(self, id=None):

		if id:
			sId = ndb.Key(urlsafe=id).get()
			if sId.current_boat != "":
				boatId = sId.current_boat
				boat = ndb.Key(urlsafe=boatId).get()
				boat_dict = boat.to_dict()
				boat_dict['self'] = '/boats/' + boatId
				self.response.write(json.dumps(boat_dict))
			else:
				self.response.out.write("No boat in slip\n")

		else:
			self.response.out.write("Error: no id given in url\n")


	#put boat into specified slip (slip id in url)
	def put(self, id=None):

		if id:
			sId = ndb.Key(urlsafe=id).get()
			put_data = json.loads(self.request.body)

			if sId.current_boat == "":
				if 'boat' in put_data:

					#set boat in from sea
					boatId = put_data['boat']
					arrivalD = put_data['arrival_date']
					boat = ndb.Key(urlsafe=boatId).get()
					boat.at_sea = False
					boat.put()

					#set slip's current boat
					sId.arrival_date = arrivalD
					sId.current_boat = boatId
					sId.put()
				else:
					self.response.out.write("Error: no boat id given\n\n")
			else:
				self.response.set_status(403)

			sId_dict = sId.to_dict()
			sId_dict['self'] = '/slips/' + sId.slipId
			sId_dict['current_boat'] = '/boats/' + sId.current_boat
			self.response.write(json.dumps(sId_dict))

		else:
			self.response.out.write("Error: no id given in url\n")


	#remove boat from slip and out to sea
	def delete(self, id=None):

		if id:
			sId = ndb.Key(urlsafe=id).get()

			if sId.current_boat != "":
				#set boat out to sea
				boatId = sId.current_boat
				boat = ndb.Key(urlsafe=boatId).get()
				boat.at_sea = True
				boat.put()

				#set slip's current boat to ""
				sId.current_boat = ""
				sId.arrival_date = ""
				sId.put()

			else:
				self.response.out.write("Error: slip has no boat to remove")

			sId_dict = sId.to_dict()
			sId_dict['self'] = '/slips/' + sId.slipId
			self.response.write(json.dumps(sId_dict))

		else:
			self.response.out.write("Error: no id given in url\n")