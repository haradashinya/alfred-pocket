#!/usr/bin/env python
#coding: utf-8


import json

import sys
import time
import subprocess
import os
import objc
import appscript
from appscript import *
import requests
from bs4 import BeautifulSoup
from Foundation import *

import os
from subprocess import Popen, PIPE



def get_script_from(browser):
    if browser == "Chrome":
        code = 'tell application "Google Chrome" to return URL of active tab of front window'
    elif browser == "Safari":
        code = 'tell application "Safari" to return URL of front document'

    return code




def run_this_scpt(scpt, args=[]):
    p = Popen(['osascript', '-'] + args, stdin=PIPE, stdout=PIPE,
              stderr=PIPE)
    stdout, stderr = p.communicate(scpt)
    return stdout




url =run_this_scpt(get_script_from("Safari"))









from flask import Flask,make_response,request,redirect,session,render_template
from flask.ext.sqlalchemy import SQLAlchemy
import os

CONSUMER_KEY = "19998-176bbd38240d9672cc47696a"

class G: pass
g = G()
g.code = ""


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/pocket.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(80), unique=True)
    code = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)


    def __init__(self, access_token,code, email):
        self.email = email
        self.code = code
        self.access_token = access_token

    def __repr__(self):
        return "<User {0} >".format(self.email)


def show_usage():
    notify('Timer usage', 'timer [minutes] [optional: title]')


def swizzle(*args):
    cls, SEL = args
    def decorator(func):
        old_IMP = cls.instanceMethodForSelector_(SEL)

        def wrapper(self, *args, **kwargs):
            return func(self, old_IMP, *args, **kwargs)

        new_IMP = objc.selector(wrapper, selector=old_IMP.selector,
                                signature=old_IMP.signature)
        objc.classAddMethod(cls, SEL, new_IMP)
        return wrapper

    return decorator


@swizzle(objc.lookUpClass('NSBundle'), b'bundleIdentifier')
def swizzled_bundleIdentifier(self, original):
    if 'Alfred 2' in os.getcwd():
        return 'com.runningwithcrayons.Alfred-2'
    else:
        return 'com.alfredapp.Alfred'


def notify(title, subtitle=None):
    """Display a NSUserNotification on Mac OS X >= 10.8"""
    NSUserNotification = objc.lookUpClass('NSUserNotification')
    NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')
    if not NSUserNotification or not NSUserNotificationCenter:
        print('no nsusernotification')
        return

    notification = NSUserNotification.alloc().init()
    notification.setTitle_(str(title))
    if subtitle:
        notification.setSubtitle_(str(subtitle))

    notification_center = NSUserNotificationCenter.defaultUserNotificationCenter()
    notification_center.deliverNotification_(notification)


def add_bookmark():
    import datetime
    import time

    u = db.session.query(User).first()
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    title = soup.select("title")[0].get_text()

    data = {
        "url":   url,
        "title":   title,
        "time":  int(time.time()),
        "consumer_key": CONSUMER_KEY,
        "access_token":  u.access_token
    }
    headers = {'content-type': 'application/json; charset=utf-8','x-accept':
               'application/json'}
    r = requests.post("https://getpocket.com/v3/add",data = json.dumps(data),headers = headers)
    notify(u"Bookmarked",u"%s" % url)
    return r.text




@app.route("/callback")
def callback():
    data = {
        "consumer_key":CONSUMER_KEY,
        "code":g.code
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    r2 = requests.post("https://getpocket.com/v3/oauth/authorize",
                       data =data,headers=headers)
    g.access_token = r2.text.split("=",1)[1].split("&")[0]
    session["access_token"] = g.access_token
    u = User(code = g.code,
             access_token = g.access_token,
             email = "")
    try:
        db.session.add(u)
        db.session.commit()
    except :
        print "err"
    return u"""
    Your access_token is {0}.
    please replace ACCESS_TOKEN's value with {0}.
    """.format(g.access_token)

@app.route("/login")
def login():
    import requests
    import json
    headers = {'content-type': 'application/json'}
    url = 'https://getpocket.com/v3/oauth/request'

    data = {"consumer_key": CONSUMER_KEY,
            "redirect_uri":"http://localhost:5000/callback"}
    r = requests.post(url, data=json.dumps(data),headers=headers)
    g.code = r.text.split("=")[1]
    session["code"] = g.code
    redirected_url = """https://getpocket.com/auth/authorize?request_token={0}&redirect_uri={1}""".format(g.code,'http://localhost:5000/callback')

    return redirect(redirected_url)



@app.route("/")
def index():
    return render_template("index.html")

def main():
    db.create_all()
    app.secret_key = "0219"
    app.run(debug=True)

    # safari.windows.first.current_tab



if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "bookmark":
            add_bookmark()
    else:
        main()

