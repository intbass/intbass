import os

from app import db, app
from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError

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
        return '<User %r>' % self.name

class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

class FileError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class File:
    def __init__(self, path):
        if not os.access(path, os.R_OK):
            raise FileError(u'Could not open file {0:s}'.format(path))

        self.filename = path
        self.name = os.path.relpath(path, app.config['FILE_PATH'])
        self.size = os.stat(path).st_size / 1024 / 1024
        try:
            audio = MP3(path)
        except:
            raise FileError('Could not open MP3 file.')
        self.bitrate = audio.info.bitrate / 1000
        self.length = audio.info.length / 60
        # getting the id3s not entirely reliable
        if 'TIT2' in audio:
            self.title = audio['TIT2'].text[0]
        if audio.has_key('TDRC'):
            self.date_recorded = audio['TDRC'].text[0]
        if audio.has_key('TALB'):
            self.album = audio['TALB'].text[0]
        if audio.has_key('TPE1'):
            self.artist = audio['TPE1'].text[0]

    def __repr__(self):
        return '<File %r>' % self.filename

    #def size_fmt(num):
    #    for x in ['bytes','KB','MB','GB']:
    #        if num < 1024.0:
    #            return "%3.1f%s" % (num, x)
    #        num /= 1024.0
    #    return "%3.1f%s" % (num, 'TB')
