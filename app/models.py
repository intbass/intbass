from app import db

ROLE_DISABLED = 0
ROLE_USER = 1
ROLE_DJ = 2
ROLE_ADMIN = 3

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    pic = db.Column(db.String(250))
    email = db.Column(db.String(120), unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    location = db.Column(db.String(64))
    password = db.Column(db.String(64))
    #posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    
    def is_admin(self):
        if self.role > 2:
            return True

    # required for flask-login
    def is_authenticated(self):
        if self.role > 0:
            return True

    # required for flask-login
    def is_active(self):
        if self.role > 0:
            return True

    # required for flask-login
    def is_anonymous(self):
        return False

    # required for flask-login
    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.name)

class Sessions(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(250), unique = True)
    date = db.Column(db.DateTime)
    name = db.Column(db.String(128), unique = True)

    def __repr__(self):
        return '<Session %r>' % (self.name)

class Roles(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64), unique = True)
