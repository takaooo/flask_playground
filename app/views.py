from app.OAuthSignIn import OAuthSignIn
from flask import render_template, flash, redirect, g,url_for,session
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm
from .models import tk_User

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Test User'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])



@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = tk_User.query.filter_by(social_id=social_id).first()
    if not user:
        user = tk_User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))

@lm.user_loader
def load_user(id):
    return tk_User.query.get(int(id))


