import os
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
from models import Note

# initialize the temaplte engine... Before the MainHanlder class def
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def _render_template(self, template_name, context=None):
        if context is None:
            context = {}

        user = users.get_current_user()
        ancestor_key = ndb.Key("User", user.nickname())
        qry = Note.owner_query(ancestor_key)
        context['notes'] = qry.fetch()

        template = jinja_env.get_template(template_name)
        return template.render(context)

    def get(self):
        user = users.get_current_user()
        if user is not None:
            logout_url = users.create_logout_url(self.request.uri)
            template_context = {
                'user': user.nickname(),
                'logout_url': logout_url,
            }
            self.response.out.write(self._render_template('main.html', template_context))
            #template = jinja_env.get_template('main.html')
            #self.response.out.write(template.render(template_context))
            #self.response.write("Hello Notes")
        else:
            login_url = users.create_login_url(self.request.uri)
            self.redirect(login_url)

    def post(self):
        user = users.get_current_user()
        if user is None:
            self.errror(401)

        note = Note(parent=ndb.Key("User", user.nickname()),
                    title=self.request.get('title'), 
                    content=self.request.get('content'))
        note.put()

        logout_url = users.create_logout_url(self.request.uri)
        template_context = {
            'user': user.nickname(),
            'logout_url': logout_url,
            'note_title': self.request.get('title'),
            'note_content': self.request.get('content'),
        }
        self.response.out.write(self._render_template('main.html', template_context))

        #template = jinja_env.get_template('main.html')
        #self.response.out.write(template.render(template_context))


app = webapp2.WSGIApplication([
    ('/', MainHandler)], debug=True)




