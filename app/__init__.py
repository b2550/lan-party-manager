from flask import Flask, render_template, redirect, flash, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config.from_pyfile('configs.py')

db = SQLAlchemy(app)

#TODO: Atom add something that edits tags on both sides
#TODO: Edit and delete entrys
#TODO: INSTALL ALIEN SWARM + SERVER, PLANETSIDE, AND MOONBASE

class IPlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    game = db.Column(db.String(248))
    ip = db.Column(db.String(32), unique=True)

db.create_all()
db.session.commit()

class addIP(FlaskForm):
    name = StringField('First Name', validators=[DataRequired()])
    game = StringField('Game', validators=[DataRequired()])
    ip = StringField('IP', validators=[DataRequired()])

class login_user(FlaskForm):
    passkey = StringField('Passkey', validators=[DataRequired()])

@app.route('/', methods=('GET', 'POST'))
def index():
    form = addIP()
    iplist = IPlist.query.all()
    if not session.has_key('logged_in'):
        session['logged_in'] = False
    if request.method == 'POST':
        if form.validate_on_submit():
            newip = IPlist(name=form.name.data.title(), game=form.game.data.title(), ip=form.ip.data)
            db.session.add(newip)
            db.session.commit()
            flash('IP Added', 'success')
            return redirect(url_for('index'))
        else:
            flash('You are missing information', 'danger')
    return render_template('main.html.j2', form=form, list=iplist)

@app.route('/delete/<item>')
def delete(item):
    if session['logged_in']:
        IPlist.query.filter_by(id=item).delete()
        db.session.commit()
        flash('Deleted', 'info')
        return redirect(url_for('index'))
    else:
        flash('Not logged in', 'warning')
        return redirect(url_for('index'))


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = login_user()
    if session['logged_in']:
        flash('Already logged in', 'info')
        return redirect(url_for('index'))
    if form.validate_on_submit():
        if form.passkey.data == app.config.get('ADMIN_PASSKEY'):
            session['logged_in'] = True
            flash('Logged in to party manager', 'success')
            return redirect(url_for('index'))
        else:
            flash('Wrong passkey', 'danger')
            return render_template('login.html.j2', form=form)
    return render_template('login.html.j2', form=form)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    flash('Logged out', 'info')
    return redirect(url_for('index'))
