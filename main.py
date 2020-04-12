import datetime
import os
import requests
import urllib.parse as urlencode
import random
import bcrypt
import psycopg2
from flask import Flask
from flask import render_template
from flask import redirect
from flask import send_file
from flask import request
from flask import make_response
from flask import send_from_directory
from flask import url_for
from flask import jsonify as jsfy
from flask_table import Table,Col
from twilio.rest import Client
from typing import List

from datetime import datetime
import time
import threading

from flask_sslify import SSLify

import json
import jsonify
import urllib3
from _datetime import timedelta

#DECLERATION : As always, spelling and grammar mistakes withing comments are always for your enjoyment.
#Bought to you by the tip of the Pagoda.

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

conn = psycopg2.connect(host="ec2-79-125-26-232.eu-west-1.compute.amazonaws.com",database="da68ui8vpnunpk", user="bbbtoniaagpfcc", password="a3927fb7aa06479e6146febe7c894fdeaec4bad7771fc74d8335bcc9f5cad4b4")
SQLcursor = conn.cursor()

account_sid = 'AC8dccea54e5befc531e46bb8a02fe61fa'
auth_token = '386ca0c98d54557cb24a72fb1f8e7784'
client = Client(account_sid, auth_token)

app = Flask(__name__)
app.static_folder = "static"
app.template_folder = "templates"

if 'DYNO' in os.environ:
    sslify = SSLify(app)


class Appointment(object):
    def __init__(self,username:str,phonenumber:str,healthcare:str,AppTime:str):
        self.username = username
        self.phonenumber = phonenumber
        self.healthcare = healthcare
        self.AppTime = AppTime

    
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

# -------------------------- DB ---------------------------

def CreateVerificationToken(UserID):
    SQL = "INSERT INTO public.\"VerificationCode\" (\"UserID\", \"VerificationCode\") VALUES (%s, %s);"
    VerificationCode = random.randint(0,99999)
    Data= (UserID,VerificationCode)
    SQLcursor.execute(SQL,Data)
    conn.commit()
    SendTwilioVerificationCode(VerificationCode,UserID)

def IsPhoneNumberDuplicate(PhoneNumber):
    params = {'g':tuple([PhoneNumber])}
    SQLcursor.execute("SELECT \"phoneNumber\" from users WHERE \"phoneNumber\" in %(g)s ",params)
    if SQLcursor.rowcount > 0:
        return True
    else:
        return False;

def GetPhoneNumber(userID):
    params={'p':tuple([userID])}
    SQLcursor.execute("SELECT \"phoneNumber\" from users WHERE \"userID\" in %(p)s ",params)
    for row in SQLcursor:
        return row[0]

def GetUserName(userID):
    params={'p':tuple([userID])}
    SQLcursor.execute("SELECT \"userName\" from users WHERE \"userID\" in %(p)s ",params)
    for row in SQLcursor:
        return row[0]

def GetHealthcareStatus(userID):
    params={'h':tuple([userID])}
    SQLcursor.execute("SELECT \"HealthcareOveride\" from users WHERE \"userID\" in %(h)s ",params)
    for row in SQLcursor:
        if row[0] == False:
            
            return row[0]
        else:
            return True

def SendTwilioVerificationCode(VerificationCode,UserID):
    params = {'g':tuple([UserID])}    
    SQLcursor.execute("SELECT \"phoneNumber\" from users WHERE \"userID\" in %(g)s ",params)
    returneddata = SQLcursor.fetchall()

    message = client.messages \
    .create(
         body="The Circle Test message "+ str(VerificationCode),
         messaging_service_sid='MG22697d1c5c9106d907824433d89fe010',
         to= returneddata[0][0]
     )
    print(message.sid)

def CheckVerificationCode(CodeToCheck):#returns true false and user id
    l = tuple([CodeToCheck])#https://stackoverflow.com/a/40737575
    truefalse = False
    params = {'l': l}
    SQLcursor.execute('SELECT \"UserID\" FROM \"VerificationCode\" WHERE \"VerificationCode\" in %(l)s',params)
    if SQLcursor.rowcount > 0:
        truefalse =True
    for row in SQLcursor.fetchall():
        ChangeUserActivation(row[0])
        return (truefalse,row[0])
        break
    
def RemoveVerificationCode(UserID):
    params={'g':tuple([UserID])}
    SQLcursor.execute("DELETE FROM public.\"VerificationCode\" WHERE \"UserID\" in %(g)s",params)
    conn.commit()

def ChangeUserActivation(UserID):
    g = tuple([UserID])
    params = {'g':g}
    SQLcursor.execute("UPDATE public.users SET \"NumberVerified\"= True WHERE \"userID\" in %(g)s",params)
    conn.commit()


# ------------------------- ACCOUNTS --------------------------
@app.route('/accounts')
def accounts(error=None):
    return render_template("/accounts.html", error=error)

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

@app.route("/booking")
def bCreate():
    return render_template("booking.html")

@app.route('/QRPersonal', methods=['GET'])
def QRpersonalFunc():
    #userID = request.cookies["auth"]
    userID = 47
    params = {'y':tuple([userID])}
    output = ""
    userName = GetUserName(userID)
    UserOveride = GetHealthcareStatus(userID);
    PhoneNumber = GetPhoneNumber(userID)
    if UserOveride:
        return jsfy(userName,PhoneNumber,"Healthcare / Vulnerable Override")
    ApptTime = ""
    
    SQLcursor.execute('SELECT * FROM \"Appointments\" WHERE \"userID\" in %(y)s',params)
    for row in SQLcursor.fetchall():
        ApptTime = row[1]
        break;
    
    return jsfy(userName,PhoneNumber,ApptTime,row[2])

@app.route('/shopping')
def shoppingreroute():
    return render_template('shopping.html')
# ------------------------- BUSINESS --------------------------
#Plan for busienss, user selcts from a list from google maps. Enters amount of slots theyll take  ,and how  long a slot is. This information then is veriffied. Will spoof verification whilst its a proof of concept

@app.route('/business/signup')
def bLogin():
    return render_template("business/signup.html")

@app.route('/business/login')
def bSignup():
    return render_template("business/login.html")

@app.route('/business/dashboard')
def bDashboard():
    return render_template("business/dashboard.html")

@app.route('/business/qr')
def bScanner():
    return render_template("business/qrScanner.html")

@app.route('/business/livechat')
def bLivechat():
    return render_template("about.html")

@app.route('/business/tabledata' ,methods = ['POST'])
def TableData():
    output = ""
    businessID ="Test"##this is to be changed to the cookie one, just to make it work atm.
    params={'y':tuple([businessID])}
    SQLcursor.execute('SELECT * FROM \"Appointments\" WHERE \"businessID\" in %(y)s',params)
    AppointmentsFetch = SQLcursor.fetchall()
    count = 0
    
    PluralAppts = [] 
    for row in AppointmentsFetch:
        AppointmentTime = str(row[1])
        params={'g':tuple([row[0]])}
        SQLcursor.execute("SELECT \"userName\",\"phoneNumber\",\"HealthcareOveride\" from users WHERE \"userID\" in %(g)s ",params)
        for item in SQLcursor.fetchall():            
            username = item[0]
            phonenumber = item[1]
            healthcare = item[2]
            if count ==0:
                count=count+1
                PluralAppts.append(Appointment(username=item[0],phonenumber=item[1],healthcare=item[2],AppTime=AppointmentTime))
            else:
               PluralAppts.append(Appointment(username=item[0],phonenumber=item[1],healthcare=item[2],AppTime=AppointmentTime))
            #outputList.append(jsfy(username=username,phonenumber=phonenumber,healthcare=str(healthcare),ApptId=str(AppointmentTime)))
    
    return json.dumps(PluralAppts,default=lambda o:o.__dict__,indent=4)
# ------------------------- API

@app.route('/api/fetchplaces',methods=["GET"])
def returnPlaces():
    
    ArrayOfPlaceID =[]
    SQLcursor.execute("SELECT \"GoogleIdentity\" FROM \"Establishments\"");
    
    for row in SQLcursor.fetchall():
        ArrayOfPlaceID.append(row[0])
        
    return jsfy(ArrayOfPlaceID)

@app.route('/api/business/signup',methods=["POST"])
def businessSignup(): 
    Output = request.form.to_dict()
    
        
    UniqueID = Output["spanname"]
    LengthOfSession = Output["lengthofsession"]
    LatLong = Output["LatLong"] 
    AmountOfSlots = Output["AmountOfSlots"]
    
    pass1 = Output["password"]
    pass2 = Output["passwordConf"]
    LatLong = LatLong.split("(")[1]
    LatLong = LatLong.split(")")[0]
    Latitude = LatLong.split(",")[0]
    Longitude = LatLong.split(",")[1]
    
    if pass1 != pass2:
        return redirect(url_for("/business/signup",error="Your passwords did not match"))
    passwordhash = bcrypt.hashpw(pass1.encode('utf-8'),bcrypt.gensalt(12)).decode('utf-8')
    
    SQLInsertNewBusiness = "INSERT INTO \"Establishments\"(\"GoogleIdentity\", \"LengthOfSlot\", \"SlotsPerHour\", \"Verified\", \"passHash\",\"Latitude\",\"Longitude\") VALUES (%s,%s,%s,%s,%s,%s,%s)"
    InsertData = (UniqueID,LengthOfSession,AmountOfSlots,False,passwordhash,Latitude,Longitude)
    SQLcursor.execute(SQLInsertNewBusiness,InsertData)
    try:
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        return generate_popup("Your business has already been signed up. You will now be taken to the login page.","/business/login")
    return redirect(url_for("/business/dashboard",error="Your business has been successfully added! You will now be added to "))
    
    
@app.route('/api/business/login',methods=["POST"])
def businessLogin(): 
    
    UniqueID = request.form["spanname"]
    password = request.form["password"]
        
    passwordhash = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt(12)).decode('utf-8')
    statement = 'SELECT \"passHash\",\"GoogleIdentity\" FROM "Establishments"'
    SQLcursor.execute(statement)
    checkhash = SQLcursor.fetchall()
    resp = make_response(generate_popup("You have logged in successfully","/"))
    for item in checkhash:
        if item[1] == UniqueID:
            print(passwordhash)
            if bcrypt.checkpw(item[0].encode("utf-8"), passwordhash.encode("utf-8")):
                print("worked")
                resp = make_response(generate_popup("You have logged in successfully","/"))
                resp.set_cookie('bauth', UniqueID)
                return resp

    print("didnt work")
    return generate_popup("Your details were incorrect","/business/login")


@app.route('/api/signup', methods=["POST"])
def signupAPI():
    print(type(request))
    if 'signupCheck' in request.cookies:
        signupCookie = request.cookies["signupCheck"] # previous signup attempt - cookie should be overwritten
    number = request.form["number"]
    if number[0] != "+":
        return generate_popup("Your phone number need to start with your country code (e.g. +44xxxxxxxx). Please try again.","/signup")
    if IsPhoneNumberDuplicate(number):
        return generate_popup("Your phone number has been previously recorded against this service. Try to Login instead.","/login")
    if not number[1:].isdigit():
        return generate_popup("Your phone number was invalid, please try again.","/signup")
    username = request.form["username"]
    pass1 = request.form["password"]
    pass2 = request.form["passwordConf"]
    if pass1 != pass2:
        error = "Your passwords did not match"
        return redirect(url_for("signup",error=error)) # not matching passwords
    # generate verify token
    resp = make_response( redirect("/verify"))
    resp.set_cookie('signupCheck', 'xxxx')
    resp.set_cookie('number', number)
    passwordhash = bcrypt.hashpw(pass1.encode('utf-8'),bcrypt.gensalt(12)).decode('utf-8')#decode done in same manner then decode the string
    if 'X-Forwarded-For' in request.headers: ##https://stackoverflow.com/a/60093677
        proxy_data = request.headers['X-Forwarded-For']
        ip_list = proxy_data.split(',')
        user_ip = ip_list[0]  # first address in list is User IP
    else:
        user_ip = request.remote_addr 


    SQLInsertNewUser = "INSERT INTO public.users(\"phoneNumber\", \"passHash\", \"signupIP\", \"userName\", \"NumberVerified\") VALUES (%s,%s,%s,%s,%s) RETURNING \"userID\""
    InsertData = (number,passwordhash,user_ip,username,False)
    SQLcursor.execute(SQLInsertNewUser,InsertData)
    returnedID = SQLcursor.fetchone()[0]
    conn.commit()
    CreateVerificationToken(returnedID)
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
            (truefalse,userID) = CheckVerificationCode(code)
            if truefalse == True:
                RemoveVerificationCode(userID)
                return generate_popup(("The code " + str(code) + " was valid, you can now login."),"/login")

            else:
                return generate_popup(("No."))
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



@app.route('/api/requestbusiness',methods=["POST"])

def AddNewShopRequest():

    if "shopID" in request.form:
        placeID = request.form["shopid"]
        parmas = {"t":tuple([placeID])}
        SQLcursor.execute("INSERT INTO \"ShopRequests\"(\"GoogleIdentity\") VALUES (%(t)s)",parmas)
        conn.commit()

    
    return "s"

@app.route('/api/getstores',methods=["POST"])
def ReturnMatches():
    LocalBusinessess = []
    Offers = []
    currentLocation =json.loads(request.data)
    radius = 0
    userID = request.cookies["auth"]
    TotalReturn = []
    FutileCount = 0
    while len(Offers)< 6:
        if FutileCount ==60:
            break;
        radius = radius +1#increase radius by 1 point
        params={"lat":tuple([currentLocation["lat"]]),"long":tuple([currentLocation["lng"]]),"radius":tuple([radius]),"userID":tuple([userID])}#parameters for quert
        SQLcursor.execute("SELECT \"GoogleIdentity\"  FROM \"Establishments\" WHERE \"Latitude\" BETWEEN %(lat)s -%(radius)s AND %(lat)s +%(radius)s AND  \"Longitude\" BETWEEN %(long)s -%(radius)s AND %(long)s + %(radius)s LIMIT 6",params)
        for row in SQLcursor.fetchall():#get all establishements within the lat and long range of the user , increases until 5 offers found
            LocalBusinessess.append(row[0])
            print("test")#adds the businesses to the table of businesses
          #gets all the unaimed appointments     
        SQLsmt= ("SELECT * FROM \"Appointments\" WHERE \"businessID\" IN"+str(tuple(LocalBusinessess))+" AND \"userID\" IS NULL")
        SQLcursor.execute(SQLsmt)
        #print(SQLsmt)
        
        #print(SQLcursor.mogrify("SELECT \"appointmentID\" FROM \"Appointments\" WHERE \"businessID\" in ANY(%s)  AND \"userID\" = null"),tuple(LocalBusinessess)))
        for row in SQLcursor.fetchall():
            #if row[2] in Offers:
            #    continue
            print("call")
            Offers.append(row[2])
            print(len(Offers))
            TotalReturn.append(str(row[0])+":@:"+str(row[1])+":@:"+str(row[2])+":@:"+str(row[3]))#append the offers
        #params["offers"] = Offers
        FutileCount = FutileCount+1
   #ClaimSlotsSQL = ("UPDATE \"Appointments\" SET \"userID\" = %(userID)s WHERE \"appointmentID\" IN" + str(tuple([Offers])))
    #SQLcursor.commit()      

    return jsfy(TotalReturn)


@app.route('/api/BookSlot',methods=["POST"])

def BookSlot():
    SelectAppID = request.form["AppID"]
    userID = request.form["userID"]

    params = {'u':tuple([userID]),'a':tuple([SelectAppID])}
     
    SQLcursor.execute("SELECT \"phoneNumber\" from users WHERE \"userID\" in %(u)s ",params)
    returneddata =SQLcursor.fetchall()
    #rememeber to send off the text message
    message = client.messages \
    .create(
         body="The Circle Booking Message . You have a booking,details to be viewed at https://thecircle.digital/QRCreator",
         messaging_service_sid='MG22697d1c5c9106d907824433d89fe010',
         to= returneddata[0][0]
     )
    SQLcursor.execute("DELETE FROM \"Appointments\" WHERE \"userID\" in %(u)s  AND \"appointmentID\" ! in %(a)s ",parmas)
    return "slot booked"

@app.route('/api/login', methods=["POST"])
def loginAPI():
    if "number" in request.form and "password" in request.form:
        number = request.form["number"]#request so passes in to the form as '+4475...'
        password = request.form["password"]
        # check against database 
        g=tuple([number])    
        params = {'g':g}
        SQLcursor.execute('SELECT \"passHash\",\"userID\" FROM users WHERE \"phoneNumber\" in %(g)s',params)
        for row in SQLcursor.fetchall():
            storedpassword = row[0]
            authkey = int(row[1])
            break
        if bcrypt.checkpw(password.encode('utf-8'),storedpassword.encode('utf-8')): # if valid
            resp = make_response(redirect("/"))
            resp.set_cookie('auth', str(authkey)) # change xxx to auth key - ive changed this to just use the user id for now - can check up on later
            return resp 
        elif False: # if invalid
            message = "The information you entered was not correct. Please double check the form and try again."
            generate_popup(message,"/login")
        else: # should never run
            message = "An error occured. Please double check the form and try again. Please contact us if this continues to happen."
            generate_popup(message,"/login")
    else:
        message = "Not all the required infomation was entered. Please double check the form and try again."
        generate_popup(message, "/login")
        
@app.route('/api/logout')
def logout():
    resp = make_response(redirect("/"))
    resp.set_cookie("auth", '', expires=0)
    resp.set_cookie("bauth", '', expires=0)
    return resp
    
# ------------------------- PAGES --------------------------

@app.route('/favicon.ico')    
def icon():
    return send_file("./static/images/favicon.ico", mimetype='image/ico')

@app.route('/addashop')
def requestShop():
    return render_template("addashop.html")

@app.route('/book')
def requestaslot():
    return render_template("request.html")

@app.route('/about')
def About():
    return render_template("about.html")
# ------------------------- DEV --------------------------

@app.route('/qr')
def testqr():
    return send_file("./static/images/qr.png", mimetype='image/png')

@app.route('/qrtest')
def qrtest():
    return render_template("qrtest.html")

# ------------------------ ERRORS --------------------------

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

# ------------------------- INDEX --------------------------

@app.route('/')
def index():
    return render_template("index new.html")

def midnightRun():
    time.sleep(10)
    while True:
        now = datetime.now()
        tfmidnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
        t2midnight = int(86400 - tfmidnight)
        print("Waiting " + str(t2midnight) + " seconds until midnight")
        time.sleep(t2midnight)
        print("It's midnight, flushing database")
        SQLcursor.execute("DELETE FROM \"Appointments\ RETURNING *")#table cleared
        SQLcursor.execute("SELECT \"GoogleIdentity\",\"LengthOfSlot\",\"SlotsPerHour\" FROM \"Establishments\"")
        EstabLi = SQLcursor.fetchall()
        daynumber = datetime.today().weekday()
        for row in EstabLi:
            url = "https://maps.googleapis.com/maps/api/place/details/json?place_id="+row[0]+"&fields=opening_hours/weekday_text&key=AIzaSyB8CEzbZy17dmq1BS6-mtxZ1KLwo3iRCms"
            response = requests.get(url).json()
            if(response.get("result")):
                Times  = response["result"]["opening_hours"]["weekday_text"][daynumber]
    
                OpeningTime = Times.split("day:")[1].split(" – ")[0].strip(" ")
                ClosingTime = Times.split(" – ")[1].strip(" ")
                OpeningTime = datetime.strptime(OpeningTime, '%I:%M %p')#.strftime("%H:%M")
                ClosingTime = datetime.strptime(ClosingTime, '%I:%M %p')#.strftime("%H:%M")
      
                CurrentTimeCount =OpeningTime#-timedelta(hours =0,minutes=int(row[1]))
                LastSlot =  ClosingTime-timedelta(hours =0,minutes=int(row[1]))
                while CurrentTimeCount != LastSlot:
                    for i in range(0,int(row[2])):
                        SQLstmt = ("INSERT INTO \"Appointments\"(\"startTime\",\"businessID\") VALUES('"+CurrentTimeCount.strftime("%H:%M")+"','"+row[0]+"')")
                        SQLcursor.execute(SQLstmt)
                        CurrentTimeCount=CurrentTimeCount+timedelta(hours =0,minutes=int(row[1]))
                print("Shop Done"+row[0])
          

      
            else:
                print("No Data Returned")
                continue;


if __name__ == '__main__':
    
    debug = True
    
    t = threading.Thread(target=midnightRun)
    t.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=debug)