import transaction

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import ForeignKey
from sqlalchemy import UnicodeText
from sqlalchemy import DateTime
from sqlalchemy import Date
from sqlalchemy import String
from sqlalchemy import Boolean

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

from zope.sqlalchemy import ZopeTransactionExtension

import datetime

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

def user_exists(userid, request):
    dbsession = DBSession()
    if dbsession.query(User).filter(User.id==userid).count() != 0: # if user exists
        return [] # normally returning principals used in authz policy, but not using authz here
    else:
        return None

class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    description = Column(UnicodeText)
    beginTime = Column(DateTime)
    endTime = Column(DateTime)
    location = Column(UnicodeText)
    deadline = Column(DateTime)
    divisions = relationship('Division', backref='event')
    materials = relationship('Material', backref='event')
    chaperones = relationship('Chaperone', backref='event')
    albums = relationship('Album', backref='event')
    #boolean/int require chaperone?

class Division(Base): # if not registerable, no event divisions
    __tablename__ = 'division'
    id = Column(Integer, primary_key=True)
    eventid = Column(Integer, ForeignKey('event.id'))
    title = Column(Unicode)
    description = Column(UnicodeText)
    limit = Column(Integer)
    registrants = relationship('Registration', backref='division')
    restrictions = relationship('Restriction', backref='division')
    results = relationship('Result', backref='division')

class Registration(Base):
    __tablename__ = 'registration'
    id = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey('user.id'))
    divisionid = Column(Integer, ForeignKey('division.id'))
    info = Column(UnicodeText)
    # multiple divisions = multiple entries

class Material(Base): #money, calculator, pencils, etc
    __tablename__ = 'materials'
    id = Column(Integer, primary_key=True)
    eventid = Column(Integer, ForeignKey('event.id'))
    description = Column(UnicodeText)

class Restriction(Base):
    __tablename__ = 'restrictions'
    id = Column(Integer, primary_key=True)
    divisionid = Column(Integer, ForeignKey('division.id'))
    description = Column(UnicodeText)

class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey('user.id'))
    divisionid = Column(Integer, ForeignKey('division.id'))
    description = Column(UnicodeText)

class Chaperone(Base):
    __tablename__ = 'chaperone'
    id = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey('user.id'))
    eventid = Column(Integer, ForeignKey('event.id'))
    carpoolLimit = Column(Integer) # 0 for no carpooling

class Settings(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    homepageHTML = Column(UnicodeText)
    schoolYear = Column(Integer)
    timestamp = Column(DateTime)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    nickname = Column(Unicode)
    gender = Column(Integer)
    email = Column(Unicode)
    phoneNumber = Column(String)
    passwordHash = Column(String)
    graduationYear = Column(Integer)
    biography = Column(UnicodeText)
    lastSeen = Column(DateTime)
    permissions = Column(Integer)
    photos = relationship('Photo', backref='owner')
    files = relationship('File', backref='owner')
    news = relationship('News', backref='owner')

class Gender:
    UNKNOWN = 0
    MALE    = 1
    FEMALE  = 2
    OTHER   = 3

class Permission: # not a database table, but an enum-like class
    VIEW   = 0b00000001 # view the site
    SPEAK  = 0b00000010 # message, discussion/articles
    ACTIVE = 0b00000100 # get emails, register in events
    PHOTO  = 0b00001000 # upload photos
    FILE   = 0b00010000 # upload files
    NEWS   = 0b00100000 # write news
    EVENT  = 0b01000000 # upload events
    ADMIN  = 0b10000000 # do admin stuff
    ALL    = 0b11111111
    NEW    = 0b00000011 # given to new members
# add permissions: Permission.VIEW | Permission.SPEAK
# remove permissions: user.permissions ^ Permission.NEWS
# check for permission: user.permissions & Permission.ADMIN == Permission.ADMIN

class Album(Base):
    __tablename__ = 'album'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    description = Column(UnicodeText)
    submitTime = Column(DateTime)
    albumTime = Column(DateTime)
    eventid = Column(Integer, ForeignKey('event.id'))
    photos = relationship('Photo', backref='album')

class Photo(Base):
    __tablename__ = 'photo'
    id = Column(Integer, primary_key=True)
    albumid = Column(Integer, ForeignKey('album.id'))
    description = Column(UnicodeText)
    submitTime = Column(DateTime)
    photoTime = Column(DateTime)
    ownerid = Column(Integer, ForeignKey('user.id'))
    isDeleted = Column(Boolean)

class File(Base):
    __tablename__ = 'file'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    filename = Column(Unicode(255))
    description = Column(UnicodeText)
    submitTime = Column(DateTime)
    fileDate = Column(Date)
    ownerid = Column(Integer, ForeignKey('user.id'))
    isDeleted = Column(Boolean)

#class Tag(Base):
#    __tablename__ = 'tag'
#    id = Column(Integer, primary_key=True)
#    name = Column(Unicode)

#class Discussion(Base):
#    pass

class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    content = Column(UnicodeText)
    submitTime = Column(DateTime)
    lastModified = Column(DateTime)
    ownerid = Column(Integer, ForeignKey('user.id'))
    isDeleted = Column(Boolean)

#class Event(Base):
#    pass

def populate():
    transaction.begin()
    session = DBSession()
    initHomepage = u"<h1>What is Leland Mathematics Club?</h1><p>We are a group of students attending Leland High School in San Jose, CA who are excited about mathematics. We represent Leland High School in regional and national mathematics competitions. Almost every week, we meet to learn about math, creatively solve math problems, and participate in math-related activities.</p><h1>The Leland Math Team, \"radical z\"</h1><p>The Leland Math Team, also known as \"radical z,\" consists of about twenty students. We meet every Monday at lunch and every Friday after school from 3 pm to 4 pm in room C-3 at Leland. We also participate in over forty events throughout the school year. We compete in competitions, tournaments, and olympiads at Leland, other schools and universities, and online.</p><h1>Contact Us</h1><p>Club email: team@lelandmath.com<br/>Teacher advisor email: Julie_Montgomery@sjusd.org</p>"
    now = datetime.datetime.utcnow()
    # determine the school year, defined by the date of graduation
    if now.month >= 7:
        thisYear = now.year + 1
    else:
        thisYear = now.year
    session.add(Settings(homepageHTML=initHomepage, schoolYear=thisYear, timestamp=now))
    session.flush()
    transaction.commit()

def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    # IMPORTANT: comment out drop_all() and populate() once the system is set up.
    #Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    try:
        pass
        #populate()
    except IntegrityError:
        # already created
        transaction.abort()
