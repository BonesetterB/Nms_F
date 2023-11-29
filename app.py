from flask import Blueprint, render_template, redirect, url_for,Flask,request, session, flash
from model import User, Game, News
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

@app.route('/create', methods=["GET","POST"])
async def create():
    if request.method == "POST":
        form_type = request.form['form_type']
        db= await get_db()
        if form_type == 'game':
            title_res=await db.execute(select(Game).filter(Game.title == request.form.get("title")))
            if  title_res.scalar() != None:
                flash("This game was already created!", "error_name")
                return  render_template("create.html" )
            
            new_games=Game(title=request.form.get("title"), platforms=request.form.get("platforms"), companys=request.form.get("companys"), descripthion=request.form.get("description"), img=request.form.get("img"))
            db.add(new_games)
            await db.commit()
            await db.refresh(new_games)
            return  render_template("create.html")
        elif form_type == 'news':
            title_res=await db.execute(select(News).filter(News.title == request.form.get("title")))
            if  title_res.scalar() != None:
                flash("This news was already created!", "error_name")
                return  render_template("create.html" )

            new_news=News(title=request.form.get("title"), author=request.form.get("author"), descripthion=request.form.get("description"), img=request.form.get("img"))
            db.add(new_news)
            await db.commit()
            await db.refresh(new_news)
            return  render_template("create.html")

    # if not session.get("role"):
    #     return  redirect("/login")

    return  render_template("create.html")

@app.route("/sign", methods=["GET","POST"])
async def sign():
    if request.method == "POST":
        db= await get_db()
        name_res=await db.execute(select(User).filter(User.username == request.form.get("username")))
        if  name_res.scalar() != None:
            flash("This name is already taken, try another one!", "error_name")
            return  render_template("sign.html" )
        email_res=await db.execute(select(User).filter(User.email == request.form.get("email")))
        if  email_res.scalar() != None:
            flash("This mail is already registered!", "error_email")
            return  render_template("sign.html" )

        new_user=User(username=request.form.get("username"), email=request.form.get("email"), password=request.form.get("password"))
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        session["username"]=request.form.get("username")

        return  redirect("/")
    
    return  render_template("sign.html" )

@app.route("/login", methods=["GET","POST"])
async def login():
    if request.method == "POST":
        db= await get_db()
        name_res=await db.execute(select(User).filter(User.username == request.form.get("username"), User.password == request.form.get("password")))
        if  name_res.scalar() == None:
            flash("You  have wrong username or password!", "error")
            return  render_template("login.html")
        
        session["username"]=request.form.get("username")

        return  redirect("/")
    return  render_template("login.html")



@app.route("/out")
def out():
    session.pop('username', None)
    return  redirect("/")



@app.route("/games", methods=["GET","POST"])
async def games():
    db= await get_db()
    result= await db.execute(select(Game))
    games=result.scalars().all()
    # if request.method == "POST":
    #     id=request.form.get("id")
    #     if id:
    #         session["cart"].append(id)
    #     return  redirect("/cart", games=game)
    
    # if not session.get("username"):
    #     return  redirect("/login")
    return  render_template("games.html", games=games)
    
@app.route("/news", methods=["GET","POST"])
async def news():
    db= await get_db()
    result= await db.execute(select(News))
    news=result.scalars().all()
    # if request.method == "POST":
    #     id=request.form.get("id")
    #     if id:
    #         session["cart"].append(id)
    #     return  redirect("/cart")
    
    # if not session.get("username"):
    #     return  redirect("/login")
    return  render_template("news.html", news=news)

app.run(debug=True)