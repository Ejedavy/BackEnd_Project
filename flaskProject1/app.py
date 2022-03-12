from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = "d96c082320a02903c22b75cab10fade1"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.column(db.String(20), nullable=False, default="default.jpg")
    posts = db.relationship("Post", lazy=True, backref="author")

    def __repr__(self):
        return f"User({self.username} , {self.email}, {self.image_file})"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"User({self.title} , {self.date})"


posts = [
    {'author': "David",
     "title": "Blog Post 1",
     "content": "This is a little blog post",
     "date": "11th March 2022"
     },

    {'author': "Daniel",
     "title": "Blog Post 2",
     "content": "Why am I doing this",
     "date": "12th March 2022"
     },
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account has been created for {form.username.data}", 'success')
        return redirect(url_for("home"))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "ejeohejidavid@gmail.com" and form.password.data == "password":
            flash("You have been logged in", "success")
            return redirect(url_for("home"))
        else:
            flash("Login Failed: Credentials do not match", "danger")
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
