from flask import Blueprint, render_template, redirect, url_for,Flask,request, session, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy 
from config import settings
from db import connect_to_db
import cloudinary
import cloudinary.uploader
import os
import DateTime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=settings.sqlalchemy_database_url
app.config["SESSION_PERMANENT"]= False
app.config["SESSION_TYPE"]= "filesystem"
Session(app)
db=SQLAlchemy(app)



@app.route("/")
def home():
    return  render_template("home.html")


@app.route('/search', methods=['GET', 'POST'])
async def search():
    db= await connect_to_db()
    if request.method == 'POST':
        search = request.form.get('search')
        print(search)

        games=await db.fetchrow("SELECT 'games' AS source_table, * FROM games WHERE title ILIKE $1",f"%{search}%")
        news=await db.fetchrow("SELECT 'news' AS source_table, * FROM news WHERE title ILIKE $1",f"%{search}%")
        print(games)
        return render_template('search.html', games=games,news=news)
    
    await db.close()
    
    return render_template('search.html', games=games,news=news)


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
            tags_input = request.form.get("tags")
            tags = tags_input.split(",") if tags_input else []
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
                "INSERT INTO games (title, platforms, companys,description,img,created_at) VALUES ($1, $2, $3,$4,$5, now()) RETURNING *",
                request.form.get("title"),
                request.form.get("platforms"),
                request.form.get("companys"),
                request.form.get("description"),
                photo_url,
            )

            if tags:
                for tag_name in tags:
                    tag = await db.fetchrow(
                        "SELECT * FROM tags WHERE name = $1",
                        tag_name.strip()
                    )
                    if tag is None:
                        # Створити новий тег, якщо його не існує
                        new_tag = await db.fetchrow(
                            "INSERT INTO tags (name) VALUES ($1) RETURNING *",
                            tag_name.strip()
                        )
                        tag_id = new_tag[0]
                    else:
                        tag_id = tag[0]

                    # Додати зв'язок між грою та тегом
                    await db.execute(
                        "INSERT INTO game_tag_association (game_id, tag_id) VALUES ($1, $2)",
                        new_game[0], tag_id
                    )

            await db.close()
            os.remove(filename)
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
                "INSERT INTO news (title, author,description,img,created_at) VALUES ($1, $2, $3,$4, now()) RETURNING *",
                request.form.get("title"),
                session.get('username'),
                request.form.get("description"),
                photo_url
            )

            await db.close()
            os.remove(filename)
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
                "INSERT INTO users (username, email, password,created_at,role,img) VALUES ($1, $2, $3,now(),$4,$5) RETURNING *",
                request.form.get("username"),
                request.form.get("email"),
                request.form.get("password"),
                'User',
                'https://res-console.cloudinary.com/dhthhnmne/thumbnails/v1/image/upload/v1702913089/0JHQtdC3X9C90LDQt9Cy0LDQvdC40Y9fNF9lenF3dDY=/preview'
            )
            await db.close()
            
            session["username"]=request.form.get("username")
            session["role"] = 'User'
            
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
        session["role"] = name_res[5]

        await db.close()
        return redirect("/")
    
    return render_template("login.html")

@app.route("/profile/<username>", methods=["GET","POST"])
async def profile(username):
    db = await connect_to_db()
    user = await db.fetchrow(
            "SELECT * FROM users WHERE username = $1",
            username
        )
    await db.close()
    if request.method == "POST":
        
        await db.close()
        return redirect("/")
    
    return render_template("profile.html", user=user)

@app.route("/out")
def out():
    session.pop('username', None)
    return  redirect("/")



@app.route("/games", methods=["GET","POST"])
async def games(): 
    conn = await connect_to_db()
    try:
        offset = (1 - 1) * 2
        query = 'SELECT * FROM games LIMIT $1 OFFSET $2'
        games = await conn.fetch(query, 2, offset)
    finally:
        await conn.close()
        return  render_template("games.html", games=games)

@app.route("/games_page/<int:page>")
async def games_page(page):
    conn = await connect_to_db()
    try:
        offset = (page - 1) * 2
        query = 'SELECT * FROM games LIMIT $1 OFFSET $2'
        games = await conn.fetch(query, 2, offset)
    finally:
        await conn.close()
    
        return render_template("games.html", games=games)


@app.route('/games/<int:game_id>', methods=["GET","POST"])
async def game_detail(game_id):
    conn = await connect_to_db()
    if request.method == 'POST':
        form_type = request.form['form_type']
        try:
            if form_type=='rating':
                rating = request.form['rating']
                name=session['username']
                user=await conn.fetchrow(
                    "SELECT * FROM users WHERE username=$1",
                    name
                )
                new_rating = await conn.fetchrow(
                    "INSERT INTO ratings (user_id, rating, games_id) VALUES ($1, $2, $3) RETURNING *",
                    user[0], 
                    int(rating),
                    game_id,
                )
            elif form_type == 'coments':
                comment = request.form['comment']
                name=session['username']
                user=await conn.fetchrow(
                    "SELECT * FROM users WHERE username=$1",
                    name
                )
                new_coments = await conn.fetchrow(
                    "INSERT INTO coments (user_id, content,created_at, games_id) VALUES ($1, $2,now(), $3) RETURNING *",
                    user[0], 
                    comment,
                    game_id,
                )
        except: 
                flash("You cannot rate without authorization!", "error")
                return redirect(f"/games/{game_id}")
        
        finally:
            await conn.close()
        return redirect(f"/games/{game_id}")
    else:
        try:
            tags=await conn.fetch('SELECT * FROM game_tag_association WHERE game_id=$1',game_id)
            tag=[]
            for i in tags:
                tt=await conn.fetchrow(
                    "SELECT * FROM tags WHERE id=$1",
                    i[1]
                )
                tag.append(tt[1])
            comments=await conn.fetch('SELECT * FROM coments WHERE games_id=$1', game_id)
            com=[]
            for C in comments:
                user=await conn.fetchrow(
                        "SELECT * FROM users WHERE id=$1",
                        C[1]
                    )
                com.append({"User":user[1], "Content":C[2]})
            ratings= await conn.fetch('SELECT * FROM ratings WHERE games_id=$1', game_id)
            game = await conn.fetch('SELECT * FROM games WHERE id=$1', game_id)
            rating=[]
            for i in ratings:
                rating.append(int(i[1]))
            r=sum(rating)/len(rating)
        
        except:
            r='There are no ratings yet'
            return  render_template("game.html", game=game[0],rating=r,comments=com,tags=tag)

        finally:
            await conn.close()

            return  render_template("game.html", game=game[0],rating=r,comments=com,tags=tag)


@app.route("/news")
async def news():
    conn = await connect_to_db()
    try:
        offset = (1 - 1) * 2
        query = 'SELECT * FROM news LIMIT $1 OFFSET $2'
        news = await conn.fetch(query, 2, offset)
    finally:
        await conn.close()
    
        return render_template("news.html", news=news)

@app.route("/news_page/<int:page>")
async def news_page(page):
    conn = await connect_to_db()
    try:
        offset = (page - 1) * 2
        query = 'SELECT * FROM news LIMIT $1 OFFSET $2'
        news = await conn.fetch(query, 2, offset)
    finally:
        await conn.close()
    
        return render_template("news.html", news=news)

@app.route('/news/<int:news_id>', methods=["GET","POST"])
async def new_detail(news_id):
    conn = await connect_to_db()

    if request.method == 'POST':
        form_type = request.form['form_type']
        try:
            if form_type=='rating':
                rating = request.form['rating']
                name=session['username']
                user=await conn.fetchrow(
                    "SELECT * FROM users WHERE username=$1",
                    name
                )
                new_rating = await conn.fetchrow(
                    "INSERT INTO ratings (user_id, rating, news_id) VALUES ($1, $2, $3) RETURNING *",
                    user[0], 
                    int(rating),
                    news_id,
                )
            elif form_type == 'coments':
                comment = request.form['comment']
                name=session['username']
                user=await conn.fetchrow(
                    "SELECT * FROM users WHERE username=$1",
                    name
                )
                new_coments = await conn.fetchrow(
                    "INSERT INTO coments (user_id, content,created_at, news_id) VALUES ($1, $2,now(), $3) RETURNING *",
                    user[0], 
                    comment,
                    news_id,
                )

        except: 
                flash("You cannot rate without authorization!", "error")
                return redirect(f"/news/{news_id}")
        
        finally:
            await conn.close()
        return redirect(f"/news/{news_id}")
    try:
        tags=await conn.fetch('SELECT * FROM news_tag_association WHERE news_id=$1',news_id)
        tag=[]
        for i in tags:
                tt=await conn.fetchrow(
                    "SELECT * FROM tags WHERE id=$1",
                    i[1]
                )
                tag.append(tt[1])

        comments=await conn.fetch('SELECT * FROM coments WHERE news_id=$1', news_id)
        com=[]
        for C in comments:
             user=await conn.fetchrow(
                    "SELECT * FROM users WHERE id=$1",
                    C[1]
                )
             com.append({"User":user[1], "Content":C[2]})
        ratings= await conn.fetch('SELECT * FROM ratings WHERE news_id=$1', news_id)
        new = await conn.fetch('SELECT * FROM news WHERE id=$1', news_id)
        rating=[]
        for i in ratings:
            rating.append(int(i[1]))
        r=sum(rating)/len(rating)
    except:
        r='There are no ratings yet'
        return  render_template("new.html", new=new[0],rating=r,comments=com,tags=tag)
    finally:
        await conn.close()

        return  render_template("new.html", new=new[0],rating=r,comments=com,tags=tag)


# # Сортування новин за рейтингом (припустимо, що рейтинг зберігається у полі `rating`)
# sorted_by_rating = sorted(news, key=lambda x: x.rating, reverse=True)

# # Сортування новин за датою (припустимо, що дата зберігається у полі `date`)
# sorted_by_date = sorted(news, key=lambda x: x.date, reverse=True)

# # Передача відсортованих списків новин до шаблону
# return render_template("news.html", sorted_by_rating=sorted_by_rating, sorted_by_date=sorted_by_date)



app.run(debug=True)