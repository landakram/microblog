from flask import (
    Flask,
    render_template,
    session,
    flash,
    redirect,
    request,
    url_for)
from flask.ext.sqlalchemy import SQLAlchemy

SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    text = db.Column(db.String())

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __repr__(self):
        return '<Entry %s>' % self.title

@app.route('/')
def show_entries():
    entries = Entry.query.all()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    title = request.form['title']
    text = request.form['text']

    new_entry = Entry(title, text)
    db.session.add(new_entry)
    db.session.commit()

    flash('New entry was successfully posted.')
    return redirect(url_for('show_entries'))

@app.route('/delete/<entry_id>')
def delete_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first()
    db.session.delete(entry)
    db.session.commit()
    flash('Entry deleted.')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()

