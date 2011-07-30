from google.appengine.ext import webapp
from google.appengine.api import mail

from mail import *
import logging


class SendMailRequest(webapp.RequestHandler):
    _TYPE_ARG = 'mail-type'
    _FROM_ARG = 'mail-from'
    _TO_ARG   = 'mail-to'
    _CC_ARG   = 'mail-cc'
    _BCC_ARG  = 'mail-bcc'
    _SUBJ_ARG = 'mail-subj'
    _TXT_ARG  = 'mail-txt'


    def post(self):
        logging.debug(str(self.request.arguments()))
        # From
        try:
            self._from = EmailAddress.from_string(self.request.get(SendMailRequest._FROM_ARG)).__repr__()
        except ValueError:
            logging.debug('invalid %s: \'%s\'' % (SendMailRequest._FROM_ARG, self.request.get(SendMailRequest._FROM_ARG)))
            self.error(400)
            return
        
        # To
        self._to = []
        tos = self.request.get(SendMailRequest._TO_ARG).split(',')
        try:
            for to in tos:
                self._to.append(EmailAddress.from_string(to).__repr__())
        except ValueError:
            logging.debug('invalid %s: \'%s\'' % (SendMailRequest._TO_ARG, self.request.get(SendMailRequest._TO_ARG)))
            self.error(400)
            return
        
        if not len(self._to):
            logging.debug('invalid %s: \'%s\'' % (SendMailRequest._TO_ARG, self.request.get(SendMailRequest._TO_ARG)))
            self.error(400)
            return

        # Cc
        self._cc = []
        ccs = self.request.get(SendMailRequest._CC_ARG).split(',')
        if ccs != ['']:
            try:
                for cc in ccs :
                    self._cc.append(EmailAddress.from_string(cc).__repr__())
            except ValueError:
                logging.debug('invalid %s: \'%s\'' % (SendMailRequest._CC_ARG, self.request.get(SendMailRequest._CC_ARG)))
                self.error(400)
                return

        # Bcc
        self._bcc = []
        bccs = self.request.get(SendMailRequest._BCC_ARG).split(',')
        if bccs != ['']:
            try:
                for bcc in bccs:
                    self._bcc.append(EmailAddress.from_string(bcc).__repr__())
            except ValueError:
                logging.debug('invalid %s' % SendMailRequest._BCC_ARG)
                self.error(400)
                return

        # Subj
        self._subj = self.request.get(SendMailRequest._SUBJ_ARG)

        # Text
        self._txt = self.request.get(SendMailRequest._TXT_ARG)

        try:
            self.send_mail()
            logging.debug("successfully sent message")
        except Exception, e:
            logging.debug("error sending message: \'%s\'" % e)
            # do something on error
            self.error(500)
            return

        # successfully completed request (204: no content)        
        self.response.set_status(204)

    def send_mail(self):
        message = mail.EmailMessage()
        message.sender  = self._from
        message.to      = self._to
        if len(self._cc):
            message.cc      = self._cc
        if len(self._bcc):
            message.bcc     = self._bcc
        message.subject = self._subj
        message.body    = self._txt

        message.send()






  # def initialize(self, **kw):
  #   """Keyword initialization.

  #   Used to set all fields of the email message using keyword arguments.

  #   Args:
  #     kw: List of keyword properties as defined by PROPERTIES.
  #   """
  #   for name, value in kw.iteritems():
  #     setattr(self, name, value)
