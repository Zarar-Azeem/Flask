from flask import render_template,Blueprint,request,redirect,url_for,flash
from flask_login import login_required,current_user
from .models import Post
from . import db


views = Blueprint('views', __name__)

@views.route('/')
@views.route("/home")
@login_required
def home(): 
    posts = Post.query.all()
    return render_template('home.html', user = current_user, posts=posts)


@views.route('/create-post', methods=['GET', 'POST'])
@login_required
def createpost():
    if request.method == 'POST':

        title = request.form.get('title')
        text = request.form.get('text')

        if len(text) < 10:
            flash("Cant do it")
        post = Post(title=title,text=text, author=current_user.id)

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('views.home'))
    
    return render_template('createpost.html', user=current_user)


@views.route('/delete-post/<id>')
@login_required
def deletepost(id):
    post = Post.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('views.home'))
