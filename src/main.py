from send import SendMailRequest
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app




application = webapp.WSGIApplication(
                    [
                        (r'/send$', SendMailRequest)
                    ],
                    debug=True
              )

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()