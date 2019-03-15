import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from gpu import GPU
from gpulist import GPUList
from gpudetail import GPUDetail
from gpuedit import GPUEdit
from gpucompare import GPUCompare

from datetime import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape'],
	autoescape = True)

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'

		user = users.get_current_user()		

		if user == None:
			template_values = {'login_url':users.create_login_url(self.request.uri)}

			template = JINJA_ENVIRONMENT.get_template('mainpage_guest.html')
			self.response.write(template.render(template_values))
			return

		template_values = {'logout_url':users.create_logout_url(self.request.uri), 'control': False}
		template = JINJA_ENVIRONMENT.get_template('mainpage.html')
		self.response.write(template.render(template_values))

	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		
		action = self.request.get('button')
		
		if action == 'Add GPU':
			name = self.request.get('name').strip()
			gpu_key = ndb.Key('GPU',name)
			gpu = gpu_key.get()
			
			if gpu != None:
				template_values = {'logout_url':users.create_logout_url(self.request.uri), 'control': True}
				template = JINJA_ENVIRONMENT.get_template('mainpage.html')
				self.response.write(template.render(template_values))
				return
			
			man = self.request.get('man').strip()
			try:
				date = datetime.strptime(self.request.get('date'),'%m/%d/%Y')
			except Exception as e:
				date = datetime.strptime(self.request.get('date'),'%Y-%m-%d')
			geoshader = self.request.get('geoshader',False) != False
			tesshader = self.request.get('tesshader',False) != False
			shaderint = self.request.get('shaderint',False) != False
			sparse = self.request.get('sparse',False) != False
			etc = self.request.get('etc',False) != False
			vertex = self.request.get('vertex',False) != False
			
			gpu = GPU(name = name, manufacturer = man, dateIssued = date, geometryShader = geoshader, tesselationShader=tesshader, shaderInt16 = shaderint, sparseBinding=sparse,
				textureCompressionETC2 = etc, vertexPipelineStoresAndAtomics=vertex)
			
			gpu.key = ndb.Key('GPU', name)

			gpu.put()
			self.redirect('/')

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/gpulist',GPUList),
	('/gpu',GPUDetail),
	('/edit', GPUEdit),
	('/gpucompare', GPUCompare)], debug = True)

  
