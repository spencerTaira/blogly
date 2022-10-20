"""Blogly application."""

from flask import Flask, render_template, request, session, redirect, flash
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "password"

connect_db(app)
db.create_all()


@app.get('/')
def home_page():
    """ Redirects to list of users"""

    return redirect('/users')


@app.get('/users')
def list_users():
    """ Lists all users """

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('user_list.html', users=users)


@app.get('/users/new')
def show_new_user_form():
    """ Shows input form for new user"""

    return render_template('new_user_form.html')


@app.post('/users/new')
def add_new_user():
    """ Process adding a new user"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = image_url if image_url != "" else None

    user = User(first_name=first_name,
                last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.get('/users/<int:user_id>')
def show_user_profile(user_id):
    """Shows the users profile, options to edit info and delete profile"""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id)

    return render_template('user_profile.html', user=user, posts=posts)


@app.get('/users/<int:user_id>/edit')
def edit_user_profile(user_id):
    """ Shows edit profile page and allows users to edit info"""

    user = User.query.get_or_404(user_id)

    return render_template('edit_profile.html', user=user)


@app.post('/users/<int:user_id>/edit')
def update_user_profile(user_id):
    """ Updates sql table with edits """
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    return redirect('/users')


@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """ deletes record referencing primary key (id) """
    User.query.filter(User.id == user_id).delete()
    db.session.commit()

    flash("User has been deleted!")
    return redirect('/users')


@app.get('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """ Render post form html """

    user = User.query.get_or_404(user_id)
    return render_template('new_post_form.html', user=user)


@app.post('/users/<int:user_id>/posts/new')
def add_new_post(user_id):
    """ Adds new record to posts table"""

    title = request.form['title']
    content = request.form['content']
    user = User.query.get_or_404(user_id)

    if content == '' or title == '':
        flash("ERROR: Please enter text in all fields")
        return render_template(
            'new_post_form.html',
            user=user,
            title=title,
            content=content
        )

    post = Post(
        title=title,
        content=content,
        user_id=user_id
    )

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.get('/posts/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('post_detail.html', post=post)


@app.get('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template(
        'edit_post.html',
        title=post.title,
        content=post.content,
        post_id=post.id
    )

@app.post('/posts/<int:post_id>/edit')
def edit_post(post_id):
    title = request.form['title']
    content = request.form['content']
    post = Post.query.get_or_404(post_id)

    if content == '' or title == '':
        flash("ERROR: Please enter text in all fields")
        return render_template(
            'edit_post.html',
            title=title,
            content=content,
            post_id=post_id
        )

    post.title = title
    post.content = content
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.post('/posts/<int:post_id>/delete')
def delete_post(post_id):
    post = Post.query.get(post_id)
    user_id = post.user_id
    Post.query.filter(Post.id == post_id).delete()
    db.session.commit()

    flash("Post has been deleted!")
    return redirect(f'/users/{user_id}')