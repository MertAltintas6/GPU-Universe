import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from gpu import GPU

JINJA_ENVIRONMENT = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape'],
	autoescape = True)

class GPUList(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		
		user = users.get_current_user()
		if user == None:
			template_values = {'login_url':users.create_login_url(self.request.uri)}

			template = JINJA_ENVIRONMENT.get_template('mainpage_guest.html')
			self.response.write(template.render(template_values))
			return
		
		gpus = GPU.query().fetch()
		template_values = {'logout_url':users.create_logout_url(self.request.uri), 'gpus': gpus}
		template = JINJA_ENVIRONMENT.get_template('gpulist.html')
		self.response.write(template.render(template_values))

	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		
		action = self.request.get('button')

		if action == 'Search':
			filters = self.request.get('filter', allow_multiple=True)
			query = GPU.query()
			for f in filters:
				query = query.filter(getattr(GPU, f)==True)

			gpus = query.fetch()
			template_values = {'logout_url':users.create_logout_url(self.request.uri), 'gpus': gpus}
			template = JINJA_ENVIRONMENT.get_template('gpulist.html')
			self.response.write(template.render(template_values))