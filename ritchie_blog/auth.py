import functools
from flask import Blueprint, redirect, render_template, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from ritchie_blog.models.all_models import User
#from ritchie_blog import engine

#creating a session to the db
#Session = sessionmaker(bind=engine)
#session = Session()


bp = Blueprint('auth', __name__, url_prefix='/auth')



@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    from ritchie_blog import engine

    Session = sessionmaker(bind=engine)
    session = Session()
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        error = None
        if not username:
            flash("Username is required")
        elif not password:
            flash("password required")

        if error is None:
            try:
                newUser = User(firstname=firstname, lastname=lastname, email=email, username=username, password=generate_password_hash(password))
                session.add(newUser)
                session.commit()
            except Exception as e:
                error = "user already exists"
            else:
                return redirect(url_for('auth.login'))
            finally:
                session.close()
    return render_template('auth/signup.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    from ritchie_blog import engine

    Session = sessionmaker(bind=engine)
    session = Session()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        user = session.query(User).filter(State.username==username).all()
        if user is None:
            error = "Incorrect user name"
        elif not check_password_hash(user['password'], password):
            error = "Incorrect Password"
        return redirect(url_for('layout'))

    return render_template('auth/login.html')
