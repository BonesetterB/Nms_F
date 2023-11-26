from flask import Blueprint, render_template, redirect, url_for,Flask,request, session
from model import User
from sqlalchemy.future import select
from flask_session import Session
from db import get_db
app = Flask(__name__)

app.config["SESSION_PERMANENT"]= False
app.config["SESSION_TYPE"]= "filesystem"
Session(app)




@app.route("/")
def home():
    return  render_template("home.html")

@app.route('/create')
def create():
    return  render_template("create.html")

@app.route("/sign", methods=["GET","POST"])
async def sign():
    if request.method == "POST":
        db= await get_db()
        name_res=await db.execute(select(User).filter(User.username == request.form.get("username")))
        if  name_res.scalar() != None:
            return  render_template("sign.html" )
        email_res=await db.execute(select(User).filter(User.email == request.form.get("email")))
        if  email_res.scalar() != None:
            return  render_template("sign.html" )

        new_user=User(username=request.form.get("username"), email=request.form.get("email"), password=request.form.get("password"))
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        session["username"]=request.form.get("username")

        return  redirect("/")
    
    return  render_template("sign.html" )

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        session["name"]=request.form.get("name")

        return  redirect("/")
    return  render_template("login.html")



@app.route("/out")
def out():
    return  render_template("out.html")



@app.route("/games", methods=["GET","POST"])
def games():
    if request.method == "POST":
        id=request.form.get("id")
        if id:
            session["cart"].append(id)
        return  redirect("/cart")
    
    if not session.get("name"):
        return  redirect("/login")
    return  render_template("games.html")
    
@app.route("/news", methods=["GET","POST"])
def news():

    if request.method == "POST":
        id=request.form.get("id")
        if id:
            session["cart"].append(id)
        return  redirect("/cart")
    
    if not session.get("name"):
        return  redirect("/login")
    return  render_template("news.html")

app.run(debug=True)