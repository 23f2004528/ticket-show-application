#Starting of the app
from flask import Flask
from backend.models import db

app=None #app instance is not created. #global variable(just a declaration)

def setup_app():
    app=Flask(__name__) #Flask object is created
    
    app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///ticket_show.sqlite3" #having database file
    db.init_app(app) #connection between app and database
    app.app_context().push() #direct access to other modules 
    app.debug=True
    print("Ticket show app is started....")

# call the setup
#we call also do it like app=setup_app() instead defining app=None
setup_app()

#for many controllers we are using below
from backend.controllers import *

def home():
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True) #instance is created

