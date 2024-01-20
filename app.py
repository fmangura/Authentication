from flask import Flask, render_template, redirect, flash, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LogInForm, fbForm
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///authorization'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "atuhentication"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)
bcrypt = Bcrypt()

connect_db(app)
app.app_context().push()

# db.drop_all()
# db.create_all()

@app.route('/')
def home():
    """Renders register form"""
    if "user_id" in session:
        username = session['user_id']
        return redirect(f'/users/{username}')
    else:
        return redirect('/login')

@app.route('/register', methods=['GET','POST'])
def register_form():
    """Handles register form"""
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first = form.first_name.data
        last = form.last_name.data

        new_user = User.register(username, password, email, first, last)
        db.session.add(new_user)
        db.session.commit()
        flash('Account Successfully Created!')

        session['user_id'] = new_user.username
        return redirect(f'/users/{username}')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_form():
    """Handles Login Form"""
    form = LogInForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['user_id'] = user.username
            return redirect(f'/users/{username}')
        
        else:
            form.username.errors = ["Wrong username/password"]
    
    return render_template('login.html', form=form)

@app.route('/users/<username>', methods=['POST', 'GET'])
def load_user(username):
    """End Page"""
    user = User.query.filter_by(username=username).first()
    fbform = fbForm()

    if fbform.validate_on_submit():
        title = fbform.title.data
        content = fbform.content.data
        post = Feedback(title=title, content=content, username_id=user.username)

        db.session.add(post)
        db.session.commit()
        return redirect('/')

    if session['user_id'] != username:
        redirect('/')
    else:
        feed = Feedback.query.all()

        return render_template('user.html', user=user, feed=feed, fbform=fbform)

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

@app.route('/users/<username>/delete')
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    session.pop('user_id')
    db.session.commit()
    return redirect('/login')

@app.route('/feedback/<int:feedback_id>/update', methods=['POST', 'GET'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    fbform = fbForm(obj=feedback)

    if fbform.validate_on_submit():
        feedback.title = fbform.title.data
        feedback.content = fbform.content.data

        db.session.commit()
        return redirect('/')

    if session['user_id'] != feedback.username_id:
        redirect('/')
    else:
        feed = Feedback.query.all()
        return render_template('feedback.html', fbform=fbform, feedback=feedback)

@app.route('/feedback/<int:feedback_id>/delete')
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    db.session.delete(feedback)
    db.session.commit()

    return redirect(f'/users/{feedback.username_id}')

