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
        #validation code ends
    return render_template("login.html")
#for register
@app.route("/register")
def signup():
    return render_template("signup.html")
