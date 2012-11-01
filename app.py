from flask import (
    Flask,
    render_template,
    session,
    flash,
    redirect,
    request,
    url_for)
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, username, plaintext):
        self.username = username
        self.password = generate_password_hash(plaintext)

    def check_password(self, plaintext):
        return check_password_hash(self.password, plaintext)


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    text = db.Column(db.String())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User',
        backref=db.backref('entries', lazy='dynamic'))

    def __init__(self, title, text, owner_id):
        self.title = title
        self.text = text
        self.owner_id = owner_id

    def __repr__(self):
        return '<Entry %s>' % self.title

@app.route('/')
def index():
    if not session.get('user_id'):
        return render_template('login.html')

    user_id = session.get('user_id')
    return redirect(url_for('show_entries', user_id=user_id))

@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/logout')
def logout():
    if session.get('user_id'):
        session.pop('user_id')
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
    elif not user.check_password(password):
        flash('Incorrect password. Please try again.')
        return redirect(url_for('index'))
    session['user_id'] = user.id
    return redirect(url_for('index'))

@app.route('/user/<user_id>/entries')
def show_entries(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return redirect(url_for('index'))

    return render_template('index.html', user=user)

@app.route('/add', methods=['POST'])
def add_entry():
    user_id = session.get('user_id')
    if not user_id:
        flash('You must log in to do that.')
        return redirect(url_for('index'))

    title = request.form['title']
    text = request.form['text']

    new_entry = Entry(title, text, user_id)
    db.session.add(new_entry)
    db.session.commit()

    flash('New entry was successfully posted.')
    return redirect(url_for('show_entries', user_id=user_id))

@app.route('/delete/<entry_id>')
def delete_entry(entry_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('You must log in to do that.')
        return redirect(url_for('index'))

    user = User.query.filter_by(id=user_id).first()
    entry = Entry.query.filter_by(id=entry_id).first()

    if user.id != entry.owner_id:
        flash("That isn't your entry.")
        return redirect(url_for('index'))

    db.session.delete(entry)
    db.session.commit()
    flash('Entry deleted.')
    return redirect(url_for('show_entries', user_id=user_id))

if __name__ == '__main__':
    app.run()

