from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    phone = db.Column(db.String(24), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


@app.route('/')
def home():
    users = Users.query.all()
    return render_template('home.html', users=users)


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/sign-up/', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        new_user = Users(
            name=name,
            email=email,
            phone=phone,
            password=password
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect('/')
    return render_template('sign-up.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
