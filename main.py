from google.appengine.api import users

import webapp2

class MainHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user is not None:
			self.response.write("Hello Notes")
		else:
			login_url = users.create_login_url(self.request.uri)
			self.redirect(login_url)


app = webapp2.WSGIApplication([
	('/', MainHandler)], debug=True)




