from flask import Blueprint, render_template, redirect, url_for,Flask,request, session, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy 
from config import settings
from db import connect_to_db
import cloudinary
import cloudinary.uploader



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=settings.sqlalchemy_database_url
app.config["SESSION_PERMANENT"]= False
app.config["SESSION_TYPE"]= "filesystem"
Session(app)
db=SQLAlchemy(app)



@app.route("/")
def home():
    return  render_template("home.html")

@app.route('/create', methods=["GET","POST"])
async def create():
    if request.method == "POST":
        imgs = request.files['img']
        imgs.save(imgs.filename) 
        filename = imgs.filename
        form_type = request.form['form_type']
        db = await connect_to_db()
        x=request.form.get("title")
        if form_type == 'game':
            title_res = await db.fetchrow(
                "SELECT * FROM games WHERE title = $1",
                request.form.get("title")
            )
            if title_res is not None:
                flash("This game was already created!", "error_name")
                return render_template("create.html")
            
            public_photo_id=f'QQAN/Games/{request.form.get("title")}'

            settings.init_cloudinary()
            photo=request.form.get("img")
            uploaded_file_info = cloudinary.uploader.upload(
                filename, public_id=public_photo_id, overwrite=True
            )

            photo_url = uploaded_file_info["secure_url"]


            new_game = await db.fetchrow(
                "INSERT INTO games (title, platforms, companys,descripthion,img) VALUES ($1, $2, $3,$4,$5) RETURNING *",
                request.form.get("title"),
                request.form.get("platforms"),
                request.form.get("companys"),
                request.form.get("description"),
                photo_url
            )
            await db.close()
            return redirect("/games")

        
        elif form_type == 'news':
            title_res = await db.fetchrow(
                "SELECT * FROM news WHERE title = $1",
                request.form.get("title")
            )
            if title_res is not None:
                flash("This news was already created!", "error_name")
                return render_template("create.html")
            
            public_photo_id=f'QQAN/News/{request.form.get("title")}'

            settings.init_cloudinary()
            photo=request.form.get("img")
            uploaded_file_info = cloudinary.uploader.upload(
                filename, public_id=public_photo_id, overwrite=True
            )

            photo_url = uploaded_file_info["secure_url"]
            public_id = uploaded_file_info["public_id"]

            new_news = await db.fetchrow(
                "INSERT INTO news (title, author,descripthion,img) VALUES ($1, $2, $3,$4) RETURNING *",
                request.form.get("title"),
                request.form.get("author"),
                request.form.get("description"),
                photo_url
            )

            await db.close()
            return redirect("/news")
    
    # if not session.get("role"):
    #     return  redirect("/login")

    return render_template("create.html")

@app.route("/sign", methods=["GET","POST"])
async def sign():
    if request.method == "POST":
        db= await connect_to_db()
        name_res = await db.fetchrow(
        "SELECT * FROM users WHERE username = $1 AND password = $2",
        request.form.get("username"),
        request.form.get("password")
    )
        if name_res is None:
            name_res = await db.fetchrow(
                "SELECT * FROM users WHERE username = $1",
                request.form.get("username")
            )
            if name_res is not None:
                flash("This name is already taken, try another one!", "error_name")
                return render_template("sign.html")

            email_res = await db.fetchrow(
                "SELECT * FROM users WHERE email = $1",
                request.form.get("email")
            )
            if email_res is not None:
                flash("This mail is already registered!", "error_email")
                return render_template("sign.html")

            new_user = await db.fetchrow(
                "INSERT INTO users (username, email, password) VALUES ($1, $2, $3) RETURNING *",
                request.form.get("username"),
                request.form.get("email"),
                request.form.get("password")
            )
            await db.close()
            
            session["username"]=request.form.get("username")

            return  redirect("/")
    
    return  render_template("sign.html")

@app.route("/login", methods=["GET","POST"])
async def login():
    if request.method == "POST":
        db = await connect_to_db()
        name_res = await db.fetchrow(
            "SELECT * FROM users WHERE username = $1 AND password = $2",
            request.form.get("username"),
            request.form.get("password")
        )
        if name_res is None:
            flash("You have entered a wrong username or password!", "error")
            return render_template("login.html")
        
        session["username"] = request.form.get("username")
        await db.close()
        return redirect("/")
    
    return render_template("login.html")



@app.route("/out")
def out():
    session.pop('username', None)
    return  redirect("/")



@app.route("/games", methods=["GET","POST"])
async def games():
    conn = await connect_to_db()
    try:
        games = await conn.fetch('SELECT * FROM games')
        return games
    finally:
        await conn.close()
    # if not session.get("username"):
    #     return  redirect("/login")
        return  render_template("games.html", games=games)

@app.route('/games/<int:game_id>')
def game_detail(game_id):
    game = next((game for game in games if game["id"] == game_id), None)
    if game:
        return render_template('game.html', game=game)
    else:
        return "Game not found", 404

@app.route("/news", methods=["GET","POST"])
async def news():
    conn = await connect_to_db()
    try:
        news = await conn.fetch('SELECT * FROM news')
        return news
    finally:
        await conn.close()
    
        return render_template("news.html", news=news)

@app.route('/news/<int:news_id>')
def new_detail(news_id):
    new = next((new for new in games if new["id"] == news_id), None)
    if new:
        return render_template('new.html', new=new)
    else:
        return "Game not found", 404

    # Припустимо, у вас є список `news`, який містить об'єкти новин

# # Сортування новин за рейтингом (припустимо, що рейтинг зберігається у полі `rating`)
# sorted_by_rating = sorted(news, key=lambda x: x.rating, reverse=True)

# # Сортування новин за датою (припустимо, що дата зберігається у полі `date`)
# sorted_by_date = sorted(news, key=lambda x: x.date, reverse=True)

# # Передача відсортованих списків новин до шаблону
# return render_template("news.html", sorted_by_rating=sorted_by_rating, sorted_by_date=sorted_by_date)



app.run(debug=True)