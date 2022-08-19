from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required, login_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = 'mjfpneg94tgrhbgkfhnrugt4o8ygnyhfnvtrgrvhy7bgnv5ty8bg5etnrth85i'


from app.models.user import User
from app.forms.login import LoginForm
from app.forms.registration import Registration
from werkzeug.urls import url_parse

@app.route('/')
@login_required
def index():
    # if form.validate_on_submit:
    #     form =  # right/wrong button
    #     word =  # back
    # else:
    #     form = # check button
    #     word = # front
    return 'this is the practice site'
    # return render_template('index.html', word=word, form=form)


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        flash('Incorrect login/password', 'error')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/registration')
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Registration()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have been successfully registered.')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run()
