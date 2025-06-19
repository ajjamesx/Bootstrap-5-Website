from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Initialize DB
with app.app_context():
    db.create_all()

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    email = request.form["email"]
    password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("login_page"))

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        session["username"] = user.username
        return redirect(url_for("dashboard"))
    else:
        return "Invalid credentials. Try again!"

@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return f"Welcome {session['username']}!"
    else:
        return redirect(url_for("login_page"))

if __name__ == "__main__":
    app.run(debug=True)