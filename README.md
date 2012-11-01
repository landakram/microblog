# Microblog! 

This is a simple tutorial based on the official [Flask tutorial](http://flask.pocoo.org/docs/tutorial/).
It uses SQLAlchemy instead of raw sqlite. The `users` branch supports
authentication and different users. Both `users` and `master` support deletion.

## Instructions

1. Read the source.
2. Clone the repo:
    
        $ git clone git@github.com:landakram/microblog.git

3. Install the dependencies:
    
        $ cd microblog
        $ easy_install pip                  # if you don't already have it
        $ pip install -r requirements.txt   # we should use virtualenv, but that's out of scope for this tutorial

4. Build the schema:
        
        $ python
        >>> from app import db
        >>> db.create_all()

5. Run:

        $ python app.py
