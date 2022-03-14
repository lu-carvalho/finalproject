import os
from sys import intern

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from sqlalchemy import null
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timezone

from helpers import apology, login_required, usd, when


# Configure application 
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finalproject.db")

# Custom filter
app.jinja_env.filters["usd"] = usd

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """"Homepage"""

    # User submited a form via POST
    if request.method == "POST":

        # Make sure income is a valid float number
        try: 
            income = float(request.form.get("income"))
        except:
            return apology("I don't think", "that income is a valid value")

        # Make sure expense is a valid float number
        try: 
            expense = float(request.form.get("expense"))
        except:
            return apology("I don't think", "that expense is a valid value")
        
        # Avoid category error if user is inputting only expense or only income
        if request.form.get("category") == None: 
            pass
        else:
            category = request.form.get("category")
        
        user_id = session["user_id"]
        balance = float(db.execute("SELECT balance FROM users WHERE id = ?", user_id)[0]["balance"])
        
        new_balance = balance + income - expense

        # Avoid storage of empty values 
        if income > 0:
            db.execute("INSERT INTO balance (user_id, value, type, timestamp, category) VALUES (?, ?, ?, ?, ?)", user_id, income, "Income", when(), category)
        
        if expense > 0:
            db.execute("INSERT INTO balance (user_id, value, type, timestamp, category) VALUES (?, ?, ?, ?, ?)", user_id, expense, "Expense", when(), category)
    
        db.execute("UPDATE users SET balance = ? WHERE id = ?", new_balance, user_id)

        return redirect("/")

    # User reached route via GET
    else:
        user_id = session["user_id"]
        balance = float(db.execute("SELECT balance FROM users WHERE id = ?", user_id)[0]["balance"])
        return render_template("index.html", balance=usd(balance))

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User submited a form via POST
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("I don't think", "that's an username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("I don't think", "that's a password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password matches
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Are you really you?", "username and password do not match")

        # Keep track of which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """"Register user"""

    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    # User submited a form via POST
    if request.method == "POST":

        # Once that form is submited, check for errors.

        # Make sure the username is not already taken
        if len(db.execute("SELECT username FROM users WHERE username = ?", username)) > 0:
            return apology("I think that", "that username is already taken")

        # Make sure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("I don't think", "your confirmation is the same as your password")

        # If there are no errors, insert the new user into the users table and log in
        else:
            hash = generate_password_hash(password)

            # Add the user to the database
            db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, hash)

            # Keep track of which user has logged in

            rows = db.execute("SELECT * FROM users WHERE username = ?", username)
            session["user_id"] = rows[0]["id"]

            return redirect("/")

    # User reached route via GET
    else:
        # Display form for registering new account
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Display transaction history
    rows = db.execute("SELECT type, value, timestamp, category FROM balance WHERE user_id = ?", session["user_id"])
    return render_template("history.html", rows=rows)

@app.route("/summary")
@login_required
def summary():
    """Show history of transactions"""
    # Display transaction history
    # Income table:

    categoryI = db.execute("SELECT DISTINCT category FROM balance WHERE type = 'Income' AND user_id = ?", session["user_id"])
    categoryE = db.execute("SELECT DISTINCT category FROM balance WHERE type = 'Expense' AND user_id = ?", session["user_id"])

    #value = db.execute("SELECT SUM (value) FROM balance WHERE user_id = ? AND category = 'Salary' AND type = 'Income'", session["user_id"])[0]['SUM (value)']

    return render_template("summary.html", categoryI=categoryI, categoryE=categoryE)
