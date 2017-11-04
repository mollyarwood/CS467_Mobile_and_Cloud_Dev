#! /usr/bin/env python2

import os
import webapp2
from webapp2_extras import jinja2
from google.appengine.api import app_identity
from google.appengine.ext import ndb

class BaseHandler(webapp2.RequestHandler):

    def render_template(self, filename, **template_args):
        self.response.write(self.jinja2.render_template(filename, **template_args))

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

