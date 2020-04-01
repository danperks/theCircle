import datetime
import os
import requests
import urllib.parse as urlencode

from flask import Flask
from flask import render_template
from flask import redirect
from flask import send_file
from flask import request
from flask import make_response
from flask import send_from_directory
from flask import url_for

from flask_sslify import SSLify

import json

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


app = Flask(__name__)
app.static_folder = "static"
app.template_folder = "templates"

if 'DYNO' in os.environ:
    sslify = SSLify(app)

# ------------------------- MISC --------------------------

def generate_popup(text,loc): # Don't use single apostophe
    html = "<body><script type=\"text/javascript\">alert('" + text + "'); window.location.href = '" + loc + "';</script></body>";
    return html

def copy_to_clip(text,loc): # Don't use single apostophe
    html = "<script>function copyToClipboard(text) {"
    "if (window.clipboardData) { // Internet Explorer"
    "window.clipboardData.setData('Text', '+ text +');"
    "} else { "
    "unsafeWindow.netscape.security.PrivilegeManager.enablePrivilege('UniversalXPConnect');"
    "const clipboardHelper = Components.classes['@mozilla.org/widget/clipboardhelper;1'].getService(Components.interfaces.nsIClipboardHelper);"
    "clipboardHelper.copyString(text);"
    "}}</script>"
    return html
    
# ------------------------- ACCOUNTS --------------------------

@app.route('/signup')
def signup(error=None):
    return render_template("/account/signup.html", error=error)

@app.route('/verify')
def verify():
    number = None
    if "number" in request.cookies:
        number = request.cookies["number"]
    return render_template("/account/verify.html", number=number)

@app.route('/login')
def login():
    return render_template("/account/login.html")

# ------------------------- API

@app.route('/api/signup', methods=["POST"])
def signupAPI():
    if 'signupCheck' in request.cookies:
        signupCookie = request.cookies["signupCheck"] # previous signup attempt - cookie should be overwritten
    number = request.form["number"]
    username = request.form["username"]
    pass1 = request.form["password"]
    pass2 = request.form["passwordConf"]
    if pass1 != pass2:
        error = "Your passwords did not match"
        return redirect(url_for("/signup",error=error)) # not matching passwords
    # generate verify token
    resp = make_response( redirect("/verify"))
    resp.set_cookie('signupCheck', 'xxxx')
    resp.set_cookie('number', number)
    return resp 

@app.route('/api/verify', methods=["POST"])
def verifyAPI():
    print(request.cookies)
    if 'signupCheck' in request.cookies and 'code' in request.form:
        print("valid")
        cookie = request.cookies["signupCheck"]
        code = request.form["code"]
        if cookie and code:
            state = "valid code"
            # add login to database - valid user
            return generate_popup(("Valid Code: " + str(code)),"/")
        elif cookie:
            state = "invalid code"
            # bad code from text
            return generate_popup("Your code was invalid. Please check the latest text and try again.","/verify")
        elif code:
            state = "invalid cookie"
            # code not from same user
            return generate_popup(("Your signup may have timed out. Try again."),"/signup")
        else:
            state = "bad request"
            # not a usual request
            return redirect("/signup")

    else:
        return redirect("/signup")

@app.route('/api/login', methods=["POST"])
def loginAPI():
    return render_template("/account/login.html")
    
# ------------------------- PAGES --------------------------

@app.route('/favicon.ico')    
def icon():
    return send_file("./static/images/favicon.ico", mimetype='image/ico')

@app.route('/redirect')
def programming():
    return redirect("/")

@app.route('/time')
def time():
    return str(datetime.datetime.now())


# ------------------------ ERRORS --------------------------

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

# ------------------------- INDEX --------------------------

@app.route('/')
def index():
    locations = {"London":("51.5073219","-0.1276474"), "Me":("52.5352881","-2.1847034"),"James":("52.4584169955596","-2.08708015178975")}
    return render_template("index.html", locations=locations)

if __name__ == '__main__':
    
    debug = True
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=debug)