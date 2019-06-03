from flask import render_template,request,redirect,url_for, abort
from flask_login import login_required, current_user
from . import main
from .forms import PostForm, UpdateProfile, CommentForm
from ..models import Post, Comment, User, Star
from .. import db, photos
import markdown2
from ..request import get_quote
from ..email import mail_message

@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Welcome to IJPost'
    quote = get_quote()
    posts = Post.query.order_by(Post.posted_p.desc()).all()
    return render_template('index.html', title = title, quote = quote, posts=posts)


@main.route('/posts', methods=['GET', 'POST'])
def posts():
    posts = Post.query.order_by(Post.posted_p.desc()).all()
    return render_template('posts.html', posts=posts)

@main.route('/post/<int:id>')
def post(id):

    '''
    View movie page function that returns the post details page and its data
    '''
    posts = Post.query.filter_by(id=id)
    comments = Comment.query.filter_by(post_id=id).all()

    return render_template('post.html',posts = posts,comments = comments)

@main.route('/post/new', methods = ['GET','POST'])
@login_required
def new_post():

    form = PostForm()
    my_stars = Star.query.filter_by(post_id=Post.id)

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        user_p = current_user
        users = User.query.all()
        new_post = Post(user_p=current_user._get_current_object().id, title=title, description = description)
        for user in users:
            mail_message("New post","email/new_post",user.email,user=users)

        new_post.save_post()
        posts = Post.query.order_by(Post.posted_p.desc()).all()
        return render_template('posts.html', posts=posts)
    return render_template('new_post.html', form=form)

@main.route('/post/<int:id>/delete',methods = ['GET','POST'])
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    comments = Comment.query.filter_by(id=id).all()
    if post is None:
        abort(404)
    for comment in comments:
        db.session.delete(comment)
        db.session.commit()
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('.posts',id=post.id))

    return render_template('posts.html',form =form)


@main.route('/comment/new/<int:post_id>', methods = ['GET','POST'])
@login_required
def new_comment(post_id):
    form = CommentForm()
    post = Post.query.get(post_id)

    if form.validate_on_submit():
        comment = form.comment.data
         
        # Updated comment instance
        new_comment = Comment(comment=comment,user_c=current_user._get_current_object().id, post_id=post_id)

        # save comment method
        new_comment.save_comment()
        return redirect(url_for('.new_comment',post_id = post_id ))

    all_comments = Comment.query.filter_by(post_id=post_id).all()
    return render_template('comment.html', form=form, comments=all_comments, post=post)

@main.route('/post/star/<int:post_id>/star', methods=['GET', 'POST'])
@login_required
def star(post_id):
    post = Post.query.get(post_id)
    user = current_user
    post_stars = Star.query.filter_by(post_id=post_id)
    posts = Post.query.order_by(Post.posted_p.desc()).all()

    if Star.query.filter(Star.user_id == user.id, Star.post_id == post_id).first():
        return render_template('posts.html', posts=posts)

    new_star = Star(post_id=post_id, user=current_user)
    new_star.save_stars()
    
    return render_template('posts.html', posts=posts)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files: 
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname = uname))
    
@main.route('/post/<int:id>/edit',methods = ['GET','POST'])
@login_required
def update_post(id):
    post = Post.query.filter_by(id=id).first()
    if post is None:
        abort(404)

    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('.post',id=post.id))

    return render_template('new_post.html',form =form)