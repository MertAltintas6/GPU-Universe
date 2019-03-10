#GPU class 
from google.appengine.ext import ndb

class GPU(ndb.Model):
	id = ndb.StringProperty()
	name = ndb.StringProperty()
	manufacturer = ndb.StringProperty()
	dateIssued = ndb.DateTimeProperty(auto_now=True)
	geometryShader = ndb.BooleanProperty()
	tesselationShader = ndb.BooleanProperty()
	shaderInt16 = ndb.BooleanProperty()
	sparseBinding = ndb.BooleanProperty()
	textureCompressionETC2 = ndb.BooleanProperty()
	vertexPipelineStoresAndAtomics = ndb.BooleanProperty()

