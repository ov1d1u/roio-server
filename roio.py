#!/usr/bin/env python
import re, os, cgi, json, time
import cgitb

from dbmanager import User, Message, Category
from utils import log

print "Content-Type: text/html"
print

cgitb.enable()

version = 0.1

class Roio():
    def __init__(self, form):
        # init the database
        log('Client connected')
        log('Preparing database')

        """
        ACTIONS
        --------------------------------
        """
        do = form.getvalue("action", '')
        log('Action choosed: ' + do)
        try:
            if do == 'hello':
                self.hello(form)
            elif do == 'register':
                self.register(form)
            elif do == 'signin':
                self.signin(form)
            elif do == 'recover':
                self.recover(form)
            elif do == 'categories':
                self.categories(form)
            else:
                log('No action: ' + do)

        except Exception, e:
            log('Whow! There was an exception: ' + str(e))

        log('Request ended with success')
        """
        ---------------------------------
        """

    def hello(self, form):
        log("Let's say 'Hi!' to " + os.environ.get("REMOTE_ADDR", "0.0.0.0"))
        data = {
            'status': 'ok',
            'version': str(version)
        }
        print json.dumps(data)
        return

    def register(self, form):
        username = form.getvalue('username', '')
        password = form.getvalue('password', '')
        realname = form.getvalue('realname', '')
        email = form.getvalue('email', '')
        log('New account request as: ' + username)

        status = 'ok'
        message = ''
        if len(username) < 6:
            status = 'fail'
            message = 'Invalid username'
            log('Username was wrong.')
        elif len(realname) < 6:
            status = 'fail'
            message = 'Invalid real name'
            log('Username was wrong.')
        elif re.match("^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", email) == None:
            status = 'fail'
            message = 'Invalid email address'
            log('E-mail was wrong.')

        if status == 'ok':
            try:
                user = User(username, password, email, realname)
                user.save()
                log('Registration ended with status: ' + status)
            except Exception, e:
                status = 'fail'
                message = 'Server error'
                log('DB ERROR: ' + str(e))
        data = {
            'status': status,
            'message': message
        }
        print json.dumps(data)
        return

    def signin(self, form):
        username = form.getvalue('username', '')
        password = form.getvalue('password', '')
        log('Signin in as {0}.'.format(username))

        status = 'ok'
        message = ''
        sessionkey = ''
        realname = ''
        try:
            user = User.auth(username, password)
            if user:
                log('User was succesfully authenticated: {0}'.format(username))
                sessionkey = '111'
                realname = user.real_name
                message = Message.get_latest().message
            else:
                log('Invalid username or password for: {0}'.format(username))
                status = 'fail'
                message = 'Invalid username or password'
        except Exception, e:
            log('DB ERROR: ' + str(e))
            status = 'fail'

        data = {
            'status': status,
            'message': message,
            'realname': realname
        }
        print json.dumps(data)
        return

    def recover(self, form):
        email = form.getvalue('email', '')
        log('Reset password for {0}.'.format(email))

        status = 'ok'
        try:
            user = User.get_by_email(email)
            if user:
                status = 'ok'
            else:
                status = 'fail'
        except Exception, e:
            status = 'fail'
            log('DB ERROR: ' + str(e))

        data = {
            'status': status
        }
        log(json.dumps(data))
        print json.dumps(data)
        return

    def categories(self, form):
        status = 'ok'
        categories = []
        try:
            categories = Category.get()
            if categories:
                status = 'ok'
            else:
                status = 'fail'
        except:
            status = 'fail'
            log('DB ERROR: ' + str(e))
        print json.dumps(categories)
        return

form = cgi.FieldStorage()
roio = Roio(form)