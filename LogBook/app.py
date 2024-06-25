import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, current_app
from flask_mail import Mail, Message
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from itertools import zip_longest

app = Flask(__name__)

app.config["SECRET_KEY"] = "minhachavesecreta"
app.config["MAIL_SERVER"] = "smtp-relay.brevo.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "youremailhere" 
app.config["MAIL_PASSWORD"] = "gG4CXTxBPphDqjQ1"
app.config["MAIL_DEFAULT_SENDER"] = "***"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "youremailhere"

Session(app)
mail = Mail(app)

db = SQL("sqlite:///database.db")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def apology(message, code=400):
    def escape(s):
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get("user_id")
        if user_id is None:
            return redirect("/login")

        user = db.execute("SELECT is_approved FROM users WHERE id = ?", user_id)

        if not user:
            return apology("User not found", 403)

        if not user[0]["is_approved"]:
            return apology("Permission denied", 403)

        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
@login_required
def index():
    table = db.execute("SELECT * FROM task")

    status_info = []
    for row in table:
        deadline = datetime.datetime.strptime(row["deadline"], "%Y-%m-%d").date()
        current_date = datetime.date.today()

        if current_date <= deadline:
            status = "on time"
            status_style = "color: green;"
        else:
            status = "delayed"
            status_style = "color: red;"

        status_info.append({"status": status, "style": status_style})

    zipped_info = zip_longest(table, status_info)

    return render_template("index.html", zipped_info=zipped_info)



@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        user_email = request.form.get("email")

        if not username or not password or not confirmation or not user_email:
            return apology("You must fill in all fields")

        elif password != confirmation:
            return apology("Your password is different from the confirmation")

        hash = generate_password_hash(password)

        try:
            new_user_id = db.execute("INSERT INTO users (username, hash, user_email) VALUES (?, ?, ?);", username, hash, user_email)
        except:
            return apology("The username or email has already been registered")

        send_approval_notification(username, user_email, new_user_id)

        return redirect("/login")


@app.route("/approve/<int:user_id>/<int:decision>")
def approve(user_id, decision):
    user_info = db.execute("SELECT * FROM users WHERE id = ?", user_id)

    if not user_info:
        return apology("User not found")

    if decision == 1:
        db.execute("UPDATE users SET is_approved = 1 WHERE id = ?", user_id)
        message = "You have been approved as an administrator. You can now access admin features."
        message1 = "You approved user to have administrative access"
    else:
        message = "Your registration request has been declined. You do not have admin powers."
        message1 = "You declined user to have administrative access"

    subject = "Registration Approval Decision"
    body = f"Hello {user_info[0]['username']},\n\n{message}"

    msg = Message(subject, recipients=[user_info[0]['user_email']], body=body)
    msg.sender = "zanetteproject@gmail.com"
    mail.send(msg)

    return render_template("approval_result.html", message1=message1)


def send_approval_notification(username, user_email, user_id):
    subject = "Registration Approval"
    body = f"Hello,\n\nA user with username {username} and email {user_email} has registered as an administrator. Click the links below to approve or decline:\n\n{request.url_root}approve/{user_id}/1 (Yes)\n\n{request.url_root}approve/{user_id}/0 (No)"

    msg = Message(subject, recipients=["zanetteproject@gmail.com"], body=body)
    msg.sender = "zanetteproject@gmail.com"
    mail.send(msg)


@app.route("/leader", methods=["GET", "POST"])
@login_required
@admin_required
def leader():

    if request.method == "GET":
        return render_template("leader.html")
    else:
        date = str(datetime.date.today())
        description = request.form.get("description")
        tasktitle = request.form.get("tasktitle")
        deadline = request.form.get("deadline")
        if not deadline:
            deadline = datetime.date.today()
        
        db.execute("INSERT INTO task (user_id, date, tasktitle, description, deadline) VALUES (?, ?, ?, ?, ?)", session["user_id"], date, tasktitle, description, deadline)

    return render_template("leader.html")


@app.route("/description/<int:id>")
@login_required
def description(id):
    history_entry = db.execute("SELECT * FROM history WHERE id = ?", id)

    if history_entry:
        description = history_entry[0]["description"]
        return render_template("description.html", description=description)

    task_entry = db.execute("SELECT * FROM task WHERE id = ?", id)

    if task_entry:
        description = task_entry[0]["description"]
        return render_template("description.html", description=description)

    return apology("Description not found")


@app.route("/finished/<int:id>")
@login_required
def finished(id):
    task = db.execute("SELECT * FROM task WHERE id = ?", id)

    if not task:
        return apology("Task not found")

    date = str(datetime.date.today())
    if task[0]["deadline"] >= date:
        status = "on time"
    else:
        status = "delayed"

    db.execute("INSERT INTO history (user_id, date, tasktitle, description, deadline, status) VALUES (?, ?, ?, ?, ?, ?)",
               session["user_id"], task[0]["date"], task[0]["tasktitle"], task[0]["description"], task[0]["deadline"], status)

    db.execute("DELETE FROM task WHERE id = ?", id)

    return redirect("/")


@app.route("/history")
@login_required
def history():
    history_data = db.execute("SELECT history.*, users.username FROM history JOIN users ON history.user_id = users.id")
    return render_template("history.html", history_data=history_data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

