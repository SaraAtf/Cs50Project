from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask.helpers import get_flashed_messages
from flask_session import Session
from helpers import apology, login_required, lookup, usd, fetch_currency_rates
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import os


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///donation.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    os.environ["API_KEY"] = "123abc"


@app.route("/")
def index():
    if session.get("user_id") is None:
        return render_template("index.html")
    else:
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        charities = db.execute(
            '''SELECT
                    c.name AS charity_name,
                    c.contact_email AS charity_email,
                    c.share_price AS share_price,
                    SUM(d.shares) AS total_shares,
                    SUM(d.price) AS total_price
                FROM charities c
                JOIN donations d ON c.id = d.charityID
                WHERE userID = ?
                GROUP BY c.id, c.name, c.contact_email
                HAVING (SUM(d.shares)) > 0;''',
            session["user_id"],
        )
        total_cash_charities = 0
        for charity in charities:
            total_cash_charities = total_cash_charities + charity["total_price"]

        total_cash = total_cash_charities + user_cash[0]["cash"]
        return render_template(
            "userHome.html", charities=charities, user_cash=user_cash[0], total_cash=total_cash
        )
    
        

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@app.route("/donate", methods=["GET", "POST"])
@login_required
def donate():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        charityId = request.form.get("charity")
        shares = request.form.get("shares")
        try:
            shares = int(shares)
        except ValueError:
            return apology("share must be a positive integer", 400)
        
        if not charityId:
            return apology('you must provide charity',400)
        elif not shares:
            return apology('you must provide shares number',400)
        elif shares < 1:
            return apology('share must be a positive integer',400)
        
        price = db.execute('select share_price from charities where id = ?',charityId)
        
        if not price:
            return apology('must provide valid charity',400)
        
        user_cash = db.execute(
            "SELECT cash FROM users WHERE id = ? ", session["user_id"]
        )[0]["cash"]

        shares_price = shares * price[0]["share_price"]
        if user_cash < (shares_price):
            return apology("cash is not sufficient", 400)
        else:
            db.execute(
                "UPDATE users SET cash = cash - ? WHERE id = ?",
                shares_price,
                session["user_id"],
            )
            db.execute(
                "INSERT INTO donations (userID, charityID, shares, price) VALUES (?, ?, ?, ?)",
                session["user_id"],
                charityId,
                shares,
                shares_price,
            )

            flash("Donation successful")
            return redirect("/")

    else:
        charities = db.execute('select id,name,share_price from charities')
        return render_template("donate.html",charities=charities)



#TODO: edit previous history to transactions
@app.route("/transactions")
@login_required
def transactions():
    """Show history of transactions"""
    charities = db.execute('''
                    SELECT c.name AS charity_name, d.shares,
                        d.price, d.timestamp
                    FROM charities c
                    JOIN donations d ON c.id = d.charityID
                    WHERE userID = ?; '''
                    , session["user_id"])
    return render_template("transactions.html", charities=charities)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        users = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(users) != 1 or not check_password_hash(
            users[0]["password"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = users[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/charity", methods=["GET", "POST"])
@login_required
def charity():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        website = request.form.get("website")
        contact_email = request.form.get("contact_email")
        share_price = request.form.get("share_price")

        # Ensure data was submitted
        if not name:
            return apology("must provide charity name", 400)
        elif not description:
            return apology("must provide description", 400)
        elif not website:
            return apology("must provide website", 400)
        elif not contact_email:
            return apology("must provide contact_email", 400)
        elif not share_price:
            return apology("must provide share_price", 400)
        else:
            db.execute('''
                INSERT INTO charities (name, description, website, contact_email, share_price)
                VALUES (?, ?, ?, ?, ?);''',
                name, description, website, contact_email, share_price)
            
            return render_template(
                "charityDetails.html",
                name = name,
                description = description,
                website = website,
                contact_email = contact_email,
                share_price = share_price
            )
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("charity.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        fullName = request.form.get("fullName")
        username = request.form.get("username")
        email = request.form.get("email")
        confirmation = request.form.get("confirmation")
        password = request.form.get("password")
        
        # Ensure the username was submitted
        if not username:
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)
        # Ensure full name was submitted
        elif not fullName:
            return apology("must provide full name", 400)
        # Ensure email was submitted
        elif not email:
            return apology("must provide email", 400)
        # Ensure confirm password was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide a confirmation password", 400)
        # Ensure passwords match
        elif not password == confirmation:
            return apology("passwords must match", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        # Ensure the username doesn't exists
        if len(rows) != 0:
            return apology("username already exists", 400)
        
        else:
            # Generate the hash of the password
            hash = generate_password_hash(
                password, method="pbkdf2:sha256", salt_length=8
            )
            # Insert the new user
            db.execute(
                "INSERT INTO users (full_name,username,email,password) VALUES (?, ?,?,?)",fullName, username, email, hash
            )
            # Redirect user to home page
            return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/fund", methods=["GET", "POST"])
@login_required
def fund():
    """Add money to your balance"""
    if request.method == "POST":
        currency = request.form.get("currency")
        amount = request.form.get("amount")
        try:
            amount = int(amount)
            if amount < 10:
                return apology("Amount must be at least 10")
        except ValueError:
            return apology("Amount must be a number")
        if not currency:
            return apology("missing Currency")

        newCash = lookup(currency,amount)

        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?",
            newCash,
            session["user_id"],
        )

        flash("Add to balance!")
        return redirect("/")
    else:
        currencies = list(fetch_currency_rates().keys());
        return render_template("fund.html", currencies=currencies)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
