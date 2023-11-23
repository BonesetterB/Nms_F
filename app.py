from flask import Blueprint, render_template, redirect, url_for,Flask,request, session
from db import session as db
from model import User
from sqlalchemy.future import select
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"]= False
app.config["SESSION_TYPE"]= "filesystem"
Session(app)




@app.route("/")
def home():
    if not session.get("name"):
        return  redirect("/login")
    return  render_template("index.html", sports=SPORTS)



app.run(debug=True)