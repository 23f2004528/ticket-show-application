#App routes
from flask import Flask,render_template,request
from .models import *
from flask import current_app as app

@app.route("/")
def home():
    return render_template("index.html")

#for login
@app.route("/login" ,methods=["GET","POST"])#requests by default is GET
def signin():
    #validation code starts
    if request.method=="POST":
        username=request.form.get("Username")
        password=request.form.get("Password")
        usr=User_Info.query.filter_by(email=username,password=password).first() #remember mistake it's not a method query is not a method so remove braces after query
        if usr and usr.role==0:   #it means it exists and is admin
            return render_template("admin_dashboard.html")
        elif usr and usr.role==1:
            return render_template("user_dashboard.html")
        else:
            return render_template("login.html",msg="Invalid user credentials")
        #validation code ends
    return render_template("login.html")
#for register
@app.route("/register",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        uname=request.form.get("Email")
        pwd=request.form.get("Password")
        fullname=request.form.get("Fullname")
        location=request.form.get("Location")
        postal=request.form.get("Zip")
        usr=User_Info.query.filter_by(email=uname).first()
        if usr:
            return render_template("signup.html",msg="Already existed user")
        new_usr=User_Info(email=uname,password=pwd,full_name=fullname,address=location,pincode=postal)
        db.session.add(new_usr)
        db.session.commit()
        return render_template("login.html",msg="Successfully registered")
    return render_template("signup.html")
