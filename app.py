import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import usd, login_required, validate_input

# Configure app
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filestystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure database
db = SQL("sqlite:///project.db")

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index(): # personal finance dashboard
    # pull data from budget using user_id to get user specific data
    row = db.execute("SELECT * FROM Budgets WHERE user_id = ?", session["user_id"])
    wants = row[0]["entertainment"] + row[0]["other"]
    needs = row[0]["bills"] + row[0]["transportation"] + row[0]["auto_budget"]
    savings = row[0]["saving"] + row[0]["debt"]
    income = row[0]["auto_budget"] + row[0]["entertainment"] + row[0]["bills"] + row[0]["saving"] + row[0]["debt"] + row[0]["transportation"] + row[0]["other"]

    # get all rows from Activity table to get users spending history
    activities = db.execute("SELECT amount, category, date FROM Activity WHERE user_id = ? ORDER BY date DESC", session["user_id"])
    categories = {}
    labels = []
    data = []
    needs_total, wants_total, savings_total = 0, 0, 0
    for activity in activities:
        if activity['category'] not in categories:
            labels.append(activity['category'])
            categories[activity['category']] = activity['amount']
        else:
            categories[activity['category']] += activity['amount']
        
        if activity['category'] == 'Transportation' or activity['category'] == 'Bills' or activity['category'] == 'Auto Budget':
            needs_total += activity['amount']
        elif activity['category'] == 'Entertainment' or activity['category'] == 'Other':
            wants_total += activity['amount']
        elif activity['category'] == 'Saving' or activity['category'] == 'Debt':
            savings_total += activity['amount']

    for value in categories.values():
        data.append(value)
    
    total = sum(data)


    return render_template("index.html", labels=labels, data=data, income=income, wants=wants, needs=needs, savings=savings, activities=activities, usd=usd, total=total, needs_total=needs_total, wants_total=wants_total, savings_total=savings_total)

@app.route("/login", methods=["GET", "POST"])
def login():
    # clear any signed in user
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("error.html", error="Username is required.")
        else:
            username = request.form.get("username")

        # validate password
        if not request.form.get("password"):
            return render_template("error.html", error="Password is required.")
        else:
            password = request.form.get("password")

        # query to check for existing username
        rows = db.execute("SELECT * FROM Users WHERE username=?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["password"], password):
            return render_template("error.html", error="username/password is invalid.")

        # remember which user logged in
        session["user_id"] = rows[0]["id"]

        #redirect to homepage
        return redirect("/")
    else:
        # validate username and password
        return render_template("login.html")

@app.route("/budget", methods=["GET", "POST"])
@login_required
def budget():
    if request.method == "POST":
        # validate the inputs for each form
        income = validate_input(request.form.get("income"))
        if income is None:
            flash("Invalid income. Please enter a valid number.", "error")
            return redirect('/budget')

        housing = validate_input(request.form.get("housing"))
        if housing is None:
            flash("Invalid input. Please enter a valid number.", "error")

        car_payment = validate_input(request.form.get("car"))
        if car_payment is None:
            flash("Invalid input. Please enter a valid number.", "error")
            return redirect('/budget')

        car_insurance = validate_input(request.form.get("car-insurance"))
        if car_insurance is None:
            flash("Invalid input. Please enter a valid number.", "error")
            return redirect('/budget')

        transportation = validate_input(request.form.get("transportation"))
        if transportation is None:
            flash("Invalid input. Please enter a valid number.", "error")

        groceries = validate_input(request.form.get("groceries"))
        if groceries is None:
            flash("Invalid input. Please enter a valid number.", "error")

        entertainment = validate_input(request.form.get("entertainment"))
        if entertainment is None:
            flash("Invalid input. Please enter a valid number.", "error")

        shopping = validate_input(request.form.get("shopping"))
        if shopping is None:
            flash("Invalid input. Please enter a valid number.", "error")

        other = validate_input(request.form.get("other"))
        if other is None:
            flash("Invalid input. Please enter a valid number.", "error")

        debt = validate_input(request.form.get("debt"))
        if debt is None:
            flash("Invalid input. Please enter a valid number.", "error")

        savings = validate_input(request.form.get("savings"))
        if savings is None:
            flash("Invalid input. Please enter a valid number.", "error")

        savings_other = validate_input(request.form.get("saving-other"))
        if savings_other is None:
            flash("Invalid input. Please enter a valid number.", "error")

        bills = housing + groceries
        auto_budget = car_payment + car_insurance
        entertainment += shopping
        other += savings_other

        # check if its adjusting the budget of current user or a new user
        rows = db.execute("SELECT * FROM Budgets WHERE user_id = ?", session["user_id"])
        if rows:
            db.execute("""
                UPDATE Budgets
                SET auto_budget = ?, entertainment = ?, bills = ?, saving = ?, debt = ?, transportation = ?, other = ?
                WHERE user_id = ?
            """, auto_budget, entertainment, bills, savings, debt, transportation, other, session["user_id"])
        else:
            # push the data to the budgets table
            db.execute("""
                INSERT INTO Budgets
                    (user_id, auto_budget, entertainment, bills, saving, debt, transportation, other)
                    VALUES
                    (?,?,?,?,?,?,?,?)
                    """, session["user_id"], auto_budget, entertainment, bills, savings, debt, transportation, other)

        return redirect("/")
    else:
        return render_template("budget.html")

@app.route("/activity", methods=["GET","POST"])
def activity():
    categories = {
        "Auto Budget" : "auto_budget",
        "Entertainment" : "entertainment",
        "Bills" : "bills",
        "Saving" : "saving",
        "Debt" : "debt",
        "Transportation" : "transportation",
        "Other" : "other",
    }

    if request.method == "POST":
        # validate input --> making sure that the user enters a number and category
        amount = validate_input(request.form.get("amount"))
        if amount is None:
            return render_template("error.html", error="Please enter an amount.")

        category = categories[request.form.get("category")]
        # add it to Activity tables to track spending history
        db.execute("""
            INSERT INTO Activity
                   (user_id, amount, category, date)
            VALUES
                   (?,?,?, CURRENT_TIMESTAMP)
        """, session["user_id"], amount, request.form.get("category"))

        # adjust values in the users budget in Budgets table
        row = db.execute("SELECT * FROM Budgets WHERE user_id = ?", session["user_id"])
        budget_category = row[0][category]
        budget_category = budget_category - amount

        # udpate users budget in table
        db.execute("UPDATE Budgets SET ?=? WHERE user_id=?", category, budget_category, session["user_id"])
        return redirect("/")
    else:
        return render_template("activity.html", categories=categories)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST": # user submits new account info
        # validate username
        if not request.form.get("username"):
            return render_template("error.html", error="Username is required.")
        else:
            check_user = db.execute("SELECT * FROM Users WHERE username = ?", request.form.get("username"))
            if check_user:
                return render_template("error.html", error="Username already exists.")
            else:
                username = request.form.get("username")

        # validate password
        if not request.form.get("password"):
            return render_template("error.html", error="Password is required.")
        else:
            password = request.form.get("password")

        # validate confirm password
        if not request.form.get("verify"):
            return render_template("error.html", error="Please confirm your password.")
        else:
            verify = request.form.get("verify")
            if password != verify: # update this to be a pop up only in future
                return render_template("error.html", error="Passwords do not match.")
            else: # hash password for more security
                password = generate_password_hash(password)

        # insert new user into users table
        db.execute("INSERT INTO Users (username, password) VALUES (?,?)", username, password)

        rows = db.execute("SELECT id FROM Users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]

        # send to budget page to set budget
        return redirect("/budget")
    else: # method == "GET" / user needs to register account
        return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    session.clear() #logs out the current user
    return redirect("/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

