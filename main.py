from flask import Flask, render_template, redirect, request
from flask import session
# session object in flask is dictionary like object which is used to store information specific to user from one request to next 
# for creating session object we need to assign special secret key to secure session data 
from flask_sqlalchemy import SQLAlchemy
import mail
import secrets

main = Flask(__name__)
main.config["SQLALCHEMY_DATABASE_URI"] = r"sqlite:///data.db"
main.config["SECRET_KEY"] = secrets.token_hex(16)
# here we are genrating special secret key to protect session data 
# This function generates a random 16-byte hexadecimal string. It’s used to generate a cryptographically secure random string
# app.config["SECRET_KEY"]:is used to sign session cookies and protect data stored in them. Without a secure SECRET_KEY, session data could be vulnerable to attacks

db = SQLAlchemy(main)
class Login(db.Model):
    # here db.Model is the base class provided to Login class is the inherited class
    Sr = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    number = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return f"{self.Sr}-{self.name}-{self.number}-{self.email}-{self.password}"


@main.route("/", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        all_data = Login.query.filter_by(email=email, password=password).first()
        if all_data is None:
            ret_val = "Wrong Email address or Password"
            return render_template("index.html", ret_val=ret_val)
        else:
            if email == all_data.email and password == all_data.password:
                return render_template("about.html")
    return render_template("index.html")


# here 'index.html' will render and when form is filled html file will send post request satisfying 'if' condn
# using request method we then gain data from html forms


@main.route("/signup", methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":
        name = request.form["name"]
        # this is a request it is used to access information from client, here it is taking information from 'form' tag in HTML
        number = request.form["number"]
        email = request.form["email"]
        password = request.form["password"]
        OTP = mail.sendEmail(email, "Verification OTP")
        session["email"] = email
        session["number"] = number
        session["name"] = name
        session["password"] = password
        session["OTP"] = OTP
        return redirect("/otp")
    # this condition will execute when user submits the form, html file will send 'POST' request.
    # request.form() method takes the user input from submitted form and assigns the value to coloumns in our database
    return render_template("signup_page.html")


@main.route("/otp", methods=["GET", "POST"])
def otp_genrate():
    if request.method == "POST":
        otp = request.form["otp"]
        if otp == session.get("OTP"):
            new_login = Login(
                email=session.get("email"),
                password=session.get("password"),
                name=session.get("name"),
                number=session.get("number"),
            )
            db.session.add(new_login)
            db.session.commit()
            return redirect("/")
    return render_template("otp.html")


with main.app_context():
    db.create_all()
main.run(debug=True, port=1500)
