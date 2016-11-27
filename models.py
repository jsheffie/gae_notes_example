from google.appengine.ext import ndb

class Note(ndb.Model):
	title = ndb.StringProperty()   # up to 500 characters
	content = ndb.TextProperty(required=True) # unlimited length
	date_created = ndb.DateTimeProperty(auto_now=True)

	# create 'ancestor query' support
	@classmethod
	def owner_query(cls, parent_key):
		return cls.query(ancestor=parent_key).order(-cls.date_created)


