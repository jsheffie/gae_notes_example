import webapp2

class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write('<h1>Hello World</h1>')
		self.response.write('<p>I am using GAE, its something new for me</p>')


app = webapp2.WSGIApplication([
	('/', MainHandler)], debug=True)
