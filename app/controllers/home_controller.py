import datetime

from flask import url_for, render_template, flash
from werkzeug.utils import redirect

from app import app, db
from flask_login import current_user
from app.forms.add import Add
from app.models.word import Word


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', words=current_user.words)
    return redirect('/login')


@app.route('/add', methods=['post', 'get'])
def add():
    form = Add()
    if form.validate_on_submit():
        word = Word(front=form.front.data, back=form.back.data, user_id=current_user.id)
        db.session.add(word)
        db.session.commit()
        flash('The word has been successfully added.')
    return render_template('add.html', form=form)


@app.route('/practice')
def practice():
    current_date = datetime.datetime.combine(datetime.datetime.today(), datetime.datetime.min.time())
    words = list(
        filter(lambda word: current_date >= datetime.datetime.combine(word.due_date, datetime.datetime.min.time()),
               current_user.words))
    return render_template('practice.html', words=words)
