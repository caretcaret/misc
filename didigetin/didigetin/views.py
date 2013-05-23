from didigetin.models import *
from pyramid.httpexceptions import *
from pyramid.view import view_config
from hashlib import sha256
import string
import unicodedata
import re
import os
from pyramid.response import Response

_here = os.path.dirname(__file__)
_css = open(os.path.join(_here, 'main.css')).read()
_css_response = Response(content_type='text/css', body=_css)

@view_config(route_name='css')
def cssview(context, request):
    return _css_response

def securehash(pwd):
    hasher = sha256()
    hasher.update('UsTrv0Mqn9yU40rlHKGxABJ9lPFhkAC8LPbqUfGk')
    hasher.update(pwd)
    return hasher.hexdigest()

def urlsafe(line):
    ret = string.join(string.lower(unicodedata.normalize('NFKD', line.strip()).encode('ascii', 'ignore')).split(), '-')
    return re.sub(r'[^a-z0-9-]+', '', ret)

@view_config(route_name='secret', renderer='templates/secret.pt')
def secretview(self, request):
    db = DBSession()
    user = ''
    error = {'user': False, 'oldsecret': False, 'newsecret': False}
    if 'submit' in request.POST:
        user = request.POST.get('user', '').strip()
        oldsecret = request.POST.get('oldsecret', '').strip()
        newsecret = request.POST.get('newsecret', '').strip()
        error['user'] = len(user) == 0 or re.match(r'^[A-Za-z0-9_-]+$', user) is None
        error['oldsecret'] = len(oldsecret) == 0 or len(user) == 0
        error['newsecret'] = len(newsecret) == 0
        
        oldhash = securehash(oldsecret)
        newhash = securehash(newsecret)
        if db.query(User).filter(User.name==user).count() >= 1:
            userdata = db.query(User).filter(User.name==user).first()
            if oldhash != userdata.secret:
                error['oldsecret'] = True
        else:
            userdata = User()
            error['user'] = True
        if True not in error.values():
            userdata.secret = newhash
            db.add(userdata)
            db.flush()
            redirectURL = request.route_url('home')
            return HTTPFound(location=redirectURL)
    return {'request': request, 'error': error, 'user': user}

@view_config(route_name='home', renderer='templates/home.pt')
def home(self, request):
    db = DBSession()
    error = {'user': False, 'secret': False, 'college': False}
    user = secret = ''
    college = result = info = u''
    if 'submit' in request.POST:
        user = request.POST.get('user', '').strip()
        secret = request.POST.get('secret', '')
        college = request.POST.get('college', u'').strip()
        result = request.POST.get('result', u'').strip()
        info = request.POST.get('info', u'').strip()
        url = urlsafe(college)
        error['user'] = len(user) == 0 or re.match(r'^[A-Za-z0-9_-]+$', user) is None
        error['secret'] = len(secret) == 0 or len(user) == 0
        error['college'] = len(url) == 0
        
        if True not in error.values():
            hash = securehash(secret)
            if db.query(User).filter(User.name==user).count() >= 1:
                userdata = db.query(User).filter(User.name==user).first()
                if hash != userdata.secret:
                    error['secret'] = True
            else:
                userdata = User(name=user, secret=hash)
                db.add(userdata)
                db.flush()
            if True not in error.values():
                if db.query(College).filter(College.url==url).filter(College.userid==userdata.id).count() >= 1:
                    resultdata = db.query(College).filter(College.url==url).filter(College.userid==userdata.id).first()
                    resultdata.college, resultdata.url, resultdata.result, resultdata.info = college, url, result, info
                else:
                    resultdata = College(name=college, url=url, result=result, info=info, userid=userdata.id)
                db.add(resultdata)
                db.flush()
                redirectURL = request.route_url('college', user=user, college=url)
                return HTTPFound(location=redirectURL)
    return {'request': request, 'error': error,
            'input': {'user': user, 'college': college, 'result': result, 'info': info}}

@view_config(route_name='user', renderer='templates/user.pt')
def userview(self, request):
    db = DBSession()
    try:
        userdata = db.query(User).filter(User.name==request.matchdict['user']).one()
        resultlist = db.query(College).filter(College.userid==userdata.id).all()
    except:
        userdata = User()
        resultlist = []
    return {'request': request, 'userdata': userdata, 'resultlist': resultlist}

@view_config(route_name='college', renderer='templates/college.pt')
def collegeview(self, request):
    user = request.matchdict['user']
    college = request.matchdict['college']
    db = DBSession()
    try:
        userdata = db.query(User).filter(User.name==user).one()
        resultdata = db.query(College).filter(College.url==college).filter(College.userid==userdata.id).one()
    except:
        userdata = User()
        resultdata = College()
    return {'request': request, 'userdata': userdata, 'resultdata': resultdata}
