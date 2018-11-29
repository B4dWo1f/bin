#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
here = os.path.dirname(os.path.realpath(__file__))

### Obsolete
#class mail():
#     def __init__(self,frm,to,body,subj,date='',attach=None):
#        self.frm = frm
#        self.to = to
#        self.date = date # So far a string, but should be a datetime object
#        self.body = body
#        self.subj = subj
#        self.attach = attach
#     def __str__(self):
#        msg = '-'*80
#        msg += '\n'
#        msg += '   From: %s\n'%(self.frm)
#        msg += '     To: %s\n'%(self.to)
#        msg += '   Date: %s\n'%(self.date)
#        msg += 'Subject: %s\n'%(self.subj)
#        msg += 'Attached files: %s\n'%(self.attach)  # TODO several attachs ???
#        msg += 'Body of the message:\n'
#        msg += self.body
#        msg += '-'*80
#        msg += '\n'
#        return msg


def send_mail(body,toaddr=[],fromaddr='',frompass='',subj='',att=None,v=False):
   """
     This function sends an e-mail to the specified addreses with the
     body, attachments and subject specified.
   If fromaddr or frompass are not specified, they are retrieved 
                                                           from mail.private
   If toaddr is not specified, it is read from toaddr.private
   """
   ## Get account details
   if fromaddr == '' or frompass == '':
      fromaddr,frompass = get_password('%s/mail.private'%(here))
   if isinstance(toaddr,str): toaddr = [toaddr]
   else: toaddr = get_dest('%s/toaddr.private'%(here))
   ## Build e-mail
   msg = MIMEMultipart()
   msg['From'] = fromaddr
   msg['To'] = ', '.join(toaddr)
   msg['Subject'] = subj
   msg.attach(MIMEText(body, 'plain'))
   if att != None:
      if not isinstance(att,list):
         att = [att]
      for at in att:
         filename = at.split('/')[-1]
         attachment = open(at, "rb")
         part = MIMEBase('application', 'octet-stream')
         part.set_payload((attachment).read())
         encoders.encode_base64(part)
         part.add_header('Content-Disposition',\
                         "attachment; filename= %s" % filename)
         msg.attach(part)
   server = smtplib.SMTP('smtp.gmail.com', 587)
   server.starttls()
   server.login(fromaddr, frompass)
   text = msg.as_string()
   server.sendmail(fromaddr, toaddr, text)
   if v: print('Mail sent to %s'%(toaddr))
   server.quit()

def get_dest(fname='%s/toaddr.private'%(here)):
   from base64 import b64decode as decode
   with open(fname,'r') as f:
      aux = f.readlines()
   lines = []
   for l in aux:
      ## Ignore everything after "#"
      li = l.lstrip().rstrip().split('#')[0].lstrip().rstrip()
      lines.append(decode(li).decode('utf-8'))
   return lines

def get_password(fname='%s/mail.private'%(here)):
   from base64 import b64decode as decode
   with open(fname,'r') as f:
      aux = f.readlines()
   lines = []
   for l in aux:
      ## Ignore everything after "#"
      li = l.lstrip().rstrip().split('#')[0].lstrip().rstrip()
      lines.append(li)
   fromaddr = decode(lines[0]).decode('utf-8')
   frompass = decode(lines[1]).decode('utf-8')
   return fromaddr,frompass


if __name__ == '__main__':
   body = 'Testing the e-mailer'
   subj = 'test'
   att = None
   send_mail(body,subj=subj,att=att)
