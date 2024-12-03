#App routes
from flask import Flask,render_template,request,url_for,redirect
from .models import *
from flask import current_app as app
from datetime import date, datetime

@app.route("/")
def home():
    return render_template("index.html")



@app.route("/user/<name>")
def user(name):
    return render_template("user_dashboard.html",name=name)
#for login
@app.route("/login" ,methods=["GET","POST"])#requests by default is GET
def signin():
    #validation code starts
    if request.method=="POST":
        username=request.form.get("Username")
        password=request.form.get("Password")
        usr=User_Info.query.filter_by(email=username,password=password).first() #remember mistake it's not a method query is not a method so remove braces after query
        if usr and usr.role==0:   #it means it exists and is admin
            return redirect(url_for("admin",name=username))
        elif usr and usr.role==1:
            return redirect(url_for("user",name=username))
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

@app.route("/admin/<name>")
def admin(name):
    theatres=get_theatres()
    return render_template("admin_dashboard.html",name=name,theatres=theatres)
#for venue making
@app.route("/venue/<name>",methods=["POST","GET"])#<> is parameter (from frontend to backend)
def add_venue(name): #() for parameter
    if request.method=="POST":
        vname=request.form.get("name")
        loc=request.form.get("location")
        pin=request.form.get("pincode")
        capacity=request.form.get("capacity")
        new_theatre=Theatre(name=vname,location=loc,pincode=pin,capacity=capacity)
        db.session.add(new_theatre)
        db.session.commit()
        return redirect(url_for("admin",name=name))
    return render_template("addvenue.html",name=name)
#for show purpose
@app.route("/show/<venue_id>/<name>",methods=["POST","GET"])#<> is parameter (from frontend to backend)
def add_show(venue_id,name): #() for parameter
    if request.method=="POST":
        sname=request.form.get("name")
        tags=request.form.get("tags")
        tkt_price=request.form.get("tkt_price")
        date_time=request.form.get("dt_time") #string type of data and processing date/time
        dt_time=datetime.strptime(date_time,"%Y-%m-%dT%H:%M")
        new_show=Show(name=sname,tags=tags,tkt_price=tkt_price,date_time=dt_time,theatre_id=venue_id)
        db.session.add(new_show)
        db.session.commit()
        return redirect(url_for("admin",name=name))
    return render_template("add_show.html",venue_id=venue_id,name=name)
@app.route("/search/<name>",methods=['GET','POST'])
def search(name):
    if request.method=="POST":
        search_txt=request.form.get("search_txt")
        by_venue=search_by_venue(search_txt)
        by_location=search_by_location(search_txt)
        if by_venue:
            return render_template("admin_dashboard.html",name=name, theatres=by_venue)
        elif by_location:
            return render_template("admin_dashboard.html",name=name,theatres=by_location)
    return redirect(url_for("admin_dashboard",name=name))



def get_theatres():
    theatres=Theatre.query.all()
    return theatres

def search_by_venue(search_txt):
    theatres=Theatre.query.filter(Theatre.name.ilike(f"%{search_txt}%")).all()
    return theatres

def search_by_location(search_txt):
    theatres=Theatre.query.filter(Theatre.location.ilike(f"%{search_txt}%")).all()
    return theatres


