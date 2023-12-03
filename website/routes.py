from flask import Blueprint
from flask import render_template, request,flash,url_for,redirect
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user,logout_user,current_user
from . import db

routes = Blueprint('routes', __name__)
                   

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form. get('password')

        user = User.query.filter_by(email=email).first()

        if not user:
            flash('Please enter correct credentials' , category='login_email_error')
        elif not check_password_hash(user.password, password):
            flash('Please enter correct credentials' , category='login_password_error')
        else:
            flash('Logged in successfully', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
    
    return render_template('login.html', user = current_user)
  
@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        print('reached here')

        if user:
            flash("This user already exists", category='error')
        else:
            new_user = User(email=email, username = username, password=generate_password_hash(
                    password, method='pbkdf2'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('register.html',user = current_user)
@routes.route('/logout')    
def logout():
    logout_user()
    return redirect('/login')