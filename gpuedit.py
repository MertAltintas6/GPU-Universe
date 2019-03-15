import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from gpu import GPU
from datetime import datetime
JINJA_ENVIRONMENT = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape'],
	autoescape = True)

class GPUEdit(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		user = users.get_current_user()
		if user == None:
			template_values = {'login_url':users.create_login_url(self.request.uri)}
			template = JINJA_ENVIRONMENT.get_template('mainpage_guest.html')
			self.response.write(template.render(template_values))
			return

		gpuname = self.request.get('gpuname')
		gpu_key = ndb.Key('GPU', gpuname)
		gpu = gpu_key.get()
		template_values = {'logout_url':users.create_logout_url(self.request.uri), 'gpu': gpu}
		template = JINJA_ENVIRONMENT.get_template('edit.html')
		self.response.write(template.render(template_values))

	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		
		action = self.request.get('button')
		
		if action=='Apply':
			name = self.request.get('gpuname')
			gpu_key = ndb.Key('GPU', name)
			gpu = gpu_key.get()
			
			gpu.manufacturer = self.request.get('man').strip()
			try:
				gpu.dateIssued = datetime.strptime(self.request.get('date'),'%m/%d/%Y')
			except Exception as e:
				gpu.dateIssued = datetime.strptime(self.request.get('date'),'%Y-%m-%d')
			gpu.geometryShader = self.request.get('geoshader',False) != False
			gpu.tesselationShader = self.request.get('tesshader',False) != False
			gpu.shaderInt16 = self.request.get('shaderint',False) != False
			gpu.sparseBinding = self.request.get('sparse',False) != False
			gpu.textureCompressionETC2 = self.request.get('etc',False) != False
			gpu.vertexPipelineStoresAndAtomics = self.request.get('vertex',False) != False

			gpu.put()
			redirect_url = '/gpu?gpuname=' + name
			self.redirect(redirect_url)

		elif action == 'Cancel':
			self.redirect('/gpulist')

