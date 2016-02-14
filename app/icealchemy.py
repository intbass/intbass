#!/usr/bin/env python

import GeoIP
import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey


gi = GeoIP.open("/usr/local/share/GeoIP/GeoIPCity.dat",GeoIP.GEOIP_STANDARD)
class ExportDict():
    def dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

class Server(Base):
    __tablename__ = 'servers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    host = Column(String)
    port = Column(Integer)
    user = Column(String)
    word = Column(String)

    def __init__(self, name, host, port, user, word):
        self.name = name
        self.host = host
        self.port = port
        self.user = user
        self.word = word

    def __repr__(self):
        return "<Server('%s')>" % (self.name)


class Mount(Base):
    __tablename__ = 'mounts'

    id = Column(Integer, primary_key=True)

    info = Column(String)
    genre = Column(String)
    count = Column(String)
    peak = Column(String)
    url = Column(String)
    max = Column(String)
    public = Column(String)
    slow = Column(String)
    source = Column(String)
    start = Column(String)
    title = Column(String)
    bytesread = Column(Integer)
    bytessent = Column(Integer)
    useragent = Column(String)
    published = Column(Boolean)
    preference = Column(Integer)

    serverid = Column(Integer, ForeignKey('servers.id'))
    server = relationship("Server", backref=backref('mounts', order_by=id))
    stationid = Column(Integer, ForeignKey('stations.id'))
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


class Listener(Base, ExportDict):
    __tablename__ = 'listeners'

    id = Column(Integer, primary_key=True)
    # Icecast Identity
    iid = Column(String)
    address = Column(String)
    agent = Column(String)
    connected = Column(Integer)
    last = Column(DateTime)
    lat = Column(Float)
    long = Column(Float)
    city = Column(String)
    region = Column(String)
    country = Column(String)
    mountid = Column(Integer, ForeignKey('mounts.id'))
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


class Station(Base, ExportDict):
    __tablename__ = 'stations'
    id = Column(Integer, primary_key=True)
    tag = Column(String, unique=True)
    live = Column(Boolean)
    name = Column(String)
    artist = Column(String)
    playing = Column(String)

    def __init__(self, tag, name, playing, artist, live):
        self.tag = tag
        self.name = name
        self.live = live
        self.artist = artist
        self.playing = playing

    def __repr__(self):
        return "<Station('%s')>" % self.tag
