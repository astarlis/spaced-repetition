from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required, login_user
from app import db, app, bootstrap, migrate
from app.models.user import User
from app.forms.login import LoginForm
from app.forms.registration import Registration
from werkzeug.urls import url_parse


@app.route('/login', methods=['post', 'get'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))

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


@app.route('/registration', methods=['post', 'get'])
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
    app.run(debug=True)
