import os
import bcrypt

from app import app, db, validate
from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError
from sqlalchemy.orm import validates

from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey
from flask_login import AnonymousUserMixin


class UserCapabilities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    capability = db.Column(db.String(12))


class AnonymousUser(AnonymousUserMixin):
    def has_capability(self, capability):
        return False


class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    pic = db.Column(db.String(250))
    email = db.Column(db.String(120), unique = True)
    location = db.Column(db.String(64))
    password = db.Column(db.String(64))
    capabilities = db.relationship('UserCapabilities', backref='user', lazy='dynamic')

    def has_capability(self, capability):
        for c in self.capabilities:
            if c.capability in (capability, 'admin'):
                return True

    def is_admin(self):
        if self.has_capability('admin'):
            return True

    # required for flask-login
    def is_authenticated(self):
        if self.has_capability('user'):
            return True

    # required for flask-login
    def is_active(self):
        #if self.role > 0:
        #    return True
        return True

    # required for flask-login
    def is_anonymous(self):
        return False

    # required for flask-login
    def get_id(self):
        return unicode(self.id)

    @validates('name')
    def set_name(self, key, name):
        return validate.username(name)

    @validates('password')
    def set_password(self, key, password):
        return validate.password(password)

    @validates('email')
    def set_email(self, key, email):
        return validate.email(email)

    def authenticate(self, password):
        submit = password.encode("utf-8")
        stored = self.password.encode("utf-8")
        return bcrypt.hashpw(submit, stored) == stored

    def __repr__(self):
        return '<User %r>' % self.name

#class Roles(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(64), unique=True)


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
        self.size = os.stat(path).st_size
        try:
            audio = MP3(path)
        except:
            raise FileError('Could not open MP3 file.')
        self.bitrate = audio.info.bitrate
        self.length = audio.info.length
        # getting the id3s not entirely reliable
        if 'TIT2' in audio:
            self.title = audio['TIT2'].text[0]
        if audio.has_key('TDRC'):
            self.date_recorded = audio['TDRC'].text[0].text
        if audio.has_key('TALB'):
            self.album = audio['TALB'].text[0]
        if audio.has_key('TPE1'):
            self.artist = audio['TPE1'].text[0]

    def __repr__(self):
        return '<File %r>' % self.filename

class Listener(db.Model):
    __tablename__ = 'listeners'

    id = db.Column(db.Integer, primary_key=True)
    # Icecast Identity
    iid = db.Column(db.String)
    address = db.Column(db.String)
    agent = db.Column(db.String)
    connected = db.Column(db.Integer)
    last = db.Column(db.DateTime)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    city = db.Column(db.String)
    region = db.Column(db.String)
    country = db.Column(db.String)
    mountid = db.Column(db.Integer, ForeignKey('mounts.id'))
    mount = relationship("Mount", backref=backref('listeners', order_by=id))

    def __init__(self, mount, iid, ip, ua, connected):
        self.mountid = mount.id
        self.iid = iid
        self.address = ip
        self.agent = ua
        self.connected = connected
        gir = gi.record_by_addr(ip)
        if gir != None:
            self.lat = gir['latitude']
            self.long = gir['longitude']
            self.city = gir['city']
            self.region = gir['region_name']
            self.country = gir['country_name']

    def __repr__(self):
        return "<Listener('%s')>" % self.iid

class Station(db.Model):
    __tablename__ = 'stations'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String, unique=True)
    live = db.Column(db.Boolean)
    name = db.Column(db.String)
    artist = db.Column(db.String)
    playing = db.Column(db.String)

    def __init__(self, tag, name, playing, artist, live):
        self.tag = tag
        self.name = name
        self.live = live
        self.artist = artist
        self.playing = playing

    def __repr__(self):
        return "<Station('%s')>" % self.tag

class Mount(db.Model):
    __tablename__ = 'mounts'

    id = db.Column(db.Integer, primary_key=True)

    info = db.Column(db.String)
    genre = db.Column(db.String)
    count = db.Column(db.String)
    peak = db.Column(db.String)
    url = db.Column(db.String)
    max = db.Column(db.String)
    public = db.Column(db.String)
    slow = db.Column(db.String)
    source = db.Column(db.String)
    start = db.Column(db.String)
    title = db.Column(db.String)
    bytesread = db.Column(db.Integer)
    bytessent = db.Column(db.Integer)
    useragent = db.Column(db.String)

    serverid = db.Column(db.Integer, ForeignKey('servers.id'))
    server = relationship("Server", backref=backref('mounts', order_by=id))
    stationid = db.Column(db.Integer, ForeignKey('stations.id'))
    station = relationship("Station", backref=backref('mounts', order_by=id))

    def __init__(self, server, info, genre, count, peak, url, max, public, slow, source, start, title, bytesread, bytessent, useragent):
        self.serverid = server.id
        self.info = info
        self.genre = genre
        self.count = count
        self.peak = peak
        self.url = url
        self.max = max
        self.public = public
        self.slow = slow
        self.source = source
        self.start = start
        self.title = title
        self.bytesread = bytesread
        self.bytessent = bytessent
        self.useragent = useragent

    def __repr__(self):
        return "<Mount(%s:%d)>" % (self.url, self.serverid)

class Server(db.Model):
    __tablename__ = 'servers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    host = db.Column(db.String)
    port = db.Column(db.Integer)
    user = db.Column(db.String)
    word = db.Column(db.String)

    def __init__(self, name, host, port, user, word):
        self.name = name
        self.host = host
        self.port = port
        self.user = user
        self.word = word

    def __repr__(self):
        return "<Server('%s')>" % (self.name)

class Comments:
    __tablename__ = 'comments' 
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.Text(1024))
    file = db.Column(db.String)
 

