import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from helpers import apology, login_required

# Configure application
app = Flask(__name__, static_folder='static')

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(image):
    filename = secure_filename(image.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    image.save(filepath)
    return filepath


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    recipes = db.execute("""
        SELECT r.recipe_id, r.title, r.difficulty, r.image_url,
               IFNULL(SUM(rt.rating), 0) as average_rating,
               u.username
        FROM recipes r
        LEFT JOIN ratings rt ON r.recipe_id = rt.recipe_id
        JOIN users u ON r.user_id = u.user_id
        GROUP BY r.recipe_id, u.username
        ORDER BY rating DESC
        LIMIT 36;
    """)
    return render_template("index.html", recipes=recipes)

@app.route("/recipe/<int:recipe_id>", methods=["GET", "POST"])
@login_required
def recipe(recipe_id):
    # Fetch the recipe details
    recipe = db.execute("""
        SELECT r.recipe_id, r.title, r.difficulty, r.image_url, r.ingredients, r.instructions, u.username
        FROM recipes r
        JOIN users u ON r.user_id = u.user_id
        WHERE r.recipe_id = ?
    """, recipe_id)

    if not recipe:
        return apology("Recipe not found", 404)

    recipe = recipe[0]

    # Fetch comments
    comments = db.execute("""
        SELECT c.comment, c.rating, u.username
        FROM comments c
        JOIN users u ON c.user_id = u.user_id
        WHERE c.recipe_id = ?
        ORDER BY c.comment_id DESC
    """, recipe_id)

    # Calculate rating
    average_rating = db.execute("""
        SELECT SUM(r.rating) as avg_rating
        FROM ratings r
        WHERE r.recipe_id = ?
    """, recipe_id)[0]["avg_rating"]

    # Track user history
    db.execute("INSERT INTO history (user_id, recipe_id) VALUES (?, ?)", session["user_id"], recipe_id)

    if request.method == "POST":
        # Check if the user has already rated this recipe
        existing_rating = db.execute("""
            SELECT rating
            FROM ratings
            WHERE user_id = ? AND recipe_id = ?
        """, session["user_id"], recipe_id)

        if 'comment' in request.form:
            # Handle new comments
            comment_text = request.form.get("comment")
            if comment_text:
                db.execute("""
                    INSERT INTO comments (user_id, recipe_id, comment, rating)
                    VALUES (?, ?, ?, 0)
                """, session["user_id"], recipe_id, comment_text)

        if 'upvote' in request.form:
            if existing_rating:
                # Increment the existing rating
                db.execute("""
                    UPDATE ratings
                    SET rating = rating + 1
                    WHERE user_id = ? AND recipe_id = ?
                """, session["user_id"], recipe_id)
            else:
                # Add a new upvote rating
                db.execute("""
                    INSERT INTO ratings (user_id, recipe_id, rating)
                    VALUES (?, ?, 1)
                """, session["user_id"], recipe_id)

        if 'downvote' in request.form:
            if existing_rating:
                # Decrement the existing rating
                db.execute("""
                    UPDATE ratings
                    SET rating = rating - 1
                    WHERE user_id = ? AND recipe_id = ?
                """, session["user_id"], recipe_id)
            else:
                # Add a new downvote rating
                db.execute("""
                    INSERT INTO ratings (user_id, recipe_id, rating)
                    VALUES (?, ?, -1)
                """, session["user_id"], recipe_id)

        return redirect(url_for('recipe', recipe_id=recipe_id))

    return render_template("recipe.html", recipe=recipe, comments=comments, average_rating=average_rating)
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log User IN"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["password_hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["user_id"]
        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        checkexisting = db.execute("SELECT * FROM users WHERE username=?", username)
        if not username:
            return apology("must provide username", 400)
        elif not password:
            return apology("must provide password", 400)
        elif checkexisting:
            return apology("user already registered", 400)
        elif password != confirmation:
            return apology("passwords must match", 400)
        else:
            password_hash = generate_password_hash(password)
            db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?);", username, password_hash)
        return redirect("/login")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload_recipe():
    if request.method == "POST":
        title = request.form.get("title")
        ingredients = request.form.get("ingredients")
        instructions = request.form.get("instructions")
        difficulty = request.form.get("difficulty")
        image = request.files.get("image")

        if not title or not ingredients or not instructions or not difficulty:
            return apology("All fields are required", 400)

        image_url = None
        if image and allowed_file(image.filename):
            image_url = save_image(image)

        db.execute("""
            INSERT INTO recipes (user_id, title, ingredients, instructions, difficulty, image_url)
            VALUES (?, ?, ?, ?, ?, ?)
        """, session["user_id"], title, ingredients, instructions, difficulty, image_url)

        return redirect("/")

    return render_template("upload_recipe.html")

@app.route("/myrecipes", methods = ["GET", "POST"])
@login_required
def myrecipes():
    recipes = db.execute("SELECT * FROM recipes where user_id = ?", session["user_id"])
    return render_template("my_recipes.html", recipes=recipes)

@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    raw_history = db.execute("""
        SELECT recipes.recipe_id, recipes.title, recipes.difficulty, recipes.image_url
        FROM history
        JOIN recipes ON history.recipe_id = recipes.recipe_id
        WHERE history.user_id = ?
        ORDER BY history.history_id DESC
    """, session["user_id"])

    # Remove duplicates
    seen = set()
    unique_history = []
    for item in raw_history:
        if item['recipe_id'] not in seen:
            seen.add(item['recipe_id'])
            unique_history.append(item)

    return render_template("history.html", history=unique_history)


@app.route("/search", methods=["GET"])
@login_required
def search():
    search_input = request.args.get("q")

    recipes = []
    if search_input:
        search_input = f"%{search_input}%"
        recipes = db.execute("SELECT * FROM recipes WHERE title LIKE ?", search_input)

    return render_template("search.html", recipes=recipes)


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    if request.method == "POST":
        userid = session["user_id"]
        oldpw = request.form.get("oldpw")
        pw = request.form.get("pw")
        new = generate_password_hash(pw)
        conf = request.form.get("confirm")
        if not pw:
            return apology("Password cannot be empty", 400)
        if pw != conf:
            return apology("Passwords must match", 400)
        hashed_password = db.execute("SELECT password_hash FROM users WHERE user_id=?", userid)[0]["password_hash"]
        if not check_password_hash(hashed_password, oldpw):
            return apology("Incorrect Old Password", 400)
        else:
            db.execute("UPDATE users SET password_hash = ? WHERE user_id = ?", new, userid)
            return redirect("/")
    else:
        return render_template("change.html")

