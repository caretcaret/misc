from lmc.models import DBSession
from lmc.models import *
from pyramid.httpexceptions import *
from pyramid.view import view_config
from pyramid.renderers import get_renderer
from pyramid.security import remember
from pyramid.security import forget
from pyramid.security import authenticated_userid
from sqlalchemy import desc
from formencode import Schema, validators, national
from formencode.api import FancyValidator, Invalid
from formencode.compound import All
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer
from webhelpers.html import tags
from recaptcha.client import captcha
import hashlib
import datetime
import markdown
import os

def securehash(password):
    hasher = hashlib.sha256()
    hasher.update('rDZFPLHg2DluQQWnWTCeOxFhSrE8wStTh8ask37I')
    hasher.update(password)
    return hasher.hexdigest()

class Breadcrumbs(list):
    """Breadcrumbs object for easy breadcrumbs management."""
    def add(self, title, url):
        """Adds an element to the breadcrumbs object. The parameter url
        is generated from request url functions."""
        self.append({'title': title, 'url': url})

class BaseView(object):
    def setup(self, request):
        self.request = request
        self.breadcrumbs = Breadcrumbs()
        self.dbsession = DBSession()
        self.base = get_renderer('templates/base.pt').implementation()
        self.title = ''
        userid = authenticated_userid(request)
        if userid is None:
            self.user = self._guestUser()
        else:
            try:
                self.user = self.dbsession.query(User).filter(User.id==userid).one()
            except:
                forget(request)
                self.user = self._guestUser()
    
    def _guestUser(self):
        return User(id=0,
                    name='',
                    nickname='',
                    gender=0,
                    email='',
                    phoneNumber='',
                    passwordHash='',
                    graduationYear=0,
                    biography='',
                    lastSeen=datetime.datetime.utcnow(),
                    permissions=Permission.VIEW)
    
    def _validated(self, schema, form, field):
        return schema().fields[field].to_python(form.data[field])
    
    def finalize(self, toRender):
        return dict({'breadcrumbs': self.breadcrumbs,
                     'base': self.base,
                     'Permission': Permission,
                     'title': self.title,
                     'user': self.user}.items() + toRender.items())
    
    def __init__(self, request):
        self.setup(request);
    
    def __call__(self):
        return self.finalize({})


@view_config(route_name='home', renderer='templates/home.pt')
class Home(BaseView):
    def __call__(self):
        settings = self.dbsession.query(Settings).order_by(Settings.id.desc()).first()
        if settings is None:
            raise HTTPNotFound('Site settings not found! Setup the site again.')
        return self.finalize({'settings': settings})

class RecaptchaValidator(FancyValidator):
    messages = {
        'unknown': 'Unknown error',
        'invalid-site-public-key': 'Internal error "invalid public key." \
Please contact an administrator',
        'invalid-site-private-key': 'Internal error "invalid private key." \
Please contact an administrator',
        'invalid-request-cookie': 'Internal error "invalid challenge parameters." \
Please contact an administrator',
        'incorrect-captcha-sol': 'The captcha solution was incorrect',
        'verify-params-incorrect': 'Internal error "invalid verify parameters." \
Please contact an administrator',
        'invalid-referrer': 'Internal error "bad domain name." \
Please contact an administrator',
        'recaptcha-not-reachable': 'The reCAPTCHA service is unavailable at \
this time. Please try again later'
        }

    def validate_python(self, value, state):
        response = captcha.submit(state.POST.get('recaptcha_challenge_field'), value, state.registry.settings['recaptcha.private'], state.environ['REMOTE_ADDR'])
        if not response.is_valid:
            raise Invalid(self.message(response.error_code, state),
                                     value, state)

class UniqueEmail(FancyValidator):
    def _to_python(self, value, state):
        dbsession = DBSession()
        if dbsession.query(User).filter(User.email==value).count() != 0:
            raise Invalid('That email address is already registered', value, state)
        return value

class RegisterSchema(Schema):
    filter_extra_fields = True
    allow_extra_fields = True
    name = validators.UnicodeString(not_empty=True, strip=True)
    nickname = validators.PlainText(strip=True, if_empty='', if_missing='', if_invalid='')
    gender = validators.Int(min=0, max=3, if_empty=0, if_missing=0, if_invalid=0)
    email = All(validators.Email(not_empty=True, strip=True), UniqueEmail())
    phoneNumber = national.USPhoneNumber(strip=True, if_empty='', if_missing='', if_invalid='')
    password = validators.String(not_empty=True)
    graduationYear = validators.Int(min=1967, not_empty=True)
    biography = validators.UnicodeString(strip=True, if_empty=u'', if_missing=u'', if_invalid=u'')
    active = validators.StringBool(if_empty=False, if_missing=False, if_invalid=False, strip=True)
    recaptcha_challenge_field = validators.String(strip=True, not_empty=True)
    recaptcha_response_field = RecaptchaValidator(strip=True, not_empty=True)
    _csrf = validators.String(strip=True, not_empty=True)

@view_config(route_name='register', renderer='templates/register.pt')
class Register(BaseView):
    def __call__(self):
        self.breadcrumbs.add('Register', self.request.route_url('register'))
        self.title = 'Register'
        
        settings = self.dbsession.query(Settings).order_by(Settings.id.desc()).first()
        if settings is None:
            raise HTTPNotFound('Site settings not found! Setup the site again.')
        
        form = Form(self.request, schema=RegisterSchema, state=self.request,
                    defaults={'name': u'',
                              'nickname': '',
                              'email': '',
                              'phoneNumber': '',
                              'graduationYear': settings.schoolYear,
                              'biography': u'',
                              'gender': 0,
                              'active': False,})
        if 'submit' in self.request.POST and form.validate():
            token = self.request.POST.get('_csrf')
            if token is None or token != self.request.session.get_csrf_token():
                raise HTTPForbidden('CSRF token is invalid or missing.')
            r = RegisterSchema().fields
            email = r['email'].to_python(form.data['email'])
            # check for first user admin privileges
            if self.dbsession.query(User).count() == 0:
                userPermission = Permission.ALL
            else:
                active = r['active'].to_python(form.data['active'])
                if active:
                    userPermission = Permission.NEW | Permission.ACTIVE
                else:
                    userPermission = Permission.NEW
            user = User(name=r['name'].to_python(form.data['name']),
                        nickname=r['nickname'].to_python(form.data['nickname']),
                        gender=r['gender'].to_python(form.data['gender']),
                        email=r['email'].to_python(form.data['email']),
                        phoneNumber=r['phoneNumber'].to_python(form.data['phoneNumber']),
                        passwordHash=securehash(form.data['password']),
                        graduationYear=r['graduationYear'].to_python(form.data['graduationYear']),
                        biography=r['biography'].to_python(form.data['biography']),
                        lastSeen=datetime.datetime.utcnow(),
                        permissions=userPermission)
            self.dbsession.add(user)
            self.dbsession.flush()
            headers = remember(self.request, user.id)
            redirectURL = self.request.route_url('home')
            return HTTPFound(location=redirectURL, headers=headers)
        
        return self.finalize({'form': form, 'settings': settings, 'recaptchaHTML': captcha.displayhtml(self.request.registry.settings['recaptcha.public'])})

@view_config(route_name='login', renderer='templates/login.pt')
class Login(BaseView):
    def __call__(self):
        self.breadcrumbs.add('Login', self.request.route_url('login'))
        self.title = 'Login'
        
        referrer = self.request.referrer
        if referrer in [None, '', self.request.route_url('login'), self.request.route_url('register')]:
            referrer = self.request.route_url('home')
        # the login form redirects back to the original page;
        # if the original page is /login, redirect to /home
        
        # not using formencode/schemas
        message = ''
        email = ''
        password = ''
        if 'submit' in self.request.POST and self.request.method == 'POST':
            token = self.request.POST.get('_csrf')
            if token is None or token != self.request.session.get_csrf_token():
                raise HTTPForbidden('CSRF token is invalid or missing.')
            email = self.request.POST.get('email', '').strip()
            password = self.request.POST.get('password', '')
            referrer = self.request.POST.get('referrer', referrer)
            try:
                user = self.dbsession.query(User).filter(User.email==email).one()
            except:
                user = self._guestUser()
            if securehash(password) == user.passwordHash:
                headers = remember(self.request, user.id, max_age=2592000)
                self.request.session.flash('You have successfully logged in!')
                return HTTPFound(location=referrer, headers=headers)
            message = 'The email address and/or password provided was incorrect.'
        
        return self.finalize({'message': message, 'email': email, 'referrer': referrer})

@view_config(route_name='logout')
class Logout(object):
    def __init__(self, request):
        self.request = request
    def __call__(self):
        headers = forget(self.request)
        self.request.session.flash('You have successfully logged out!')
        return HTTPFound(location=self.request.route_url('home'), headers=headers)

@view_config(route_name='news', renderer='templates/news/index.pt')
class NewsIndex(BaseView):
    def __call__(self):
        self.breadcrumbs.add('News', self.request.route_url('news'))
        self.title = 'News'
        
        articleList = self.dbsession.query(News).filter(News.isDeleted==False).order_by(News.id.desc()).all()
        if articleList:
            articleHTML = markdown.markdown(articleList[0].content, safe_mode='escape')
        else:
            articleHTML = ''
        return self.finalize({'articleList': articleList, 'articleHTML': articleHTML})

@view_config(route_name='news_article', renderer='templates/news/article.pt')
class NewsArticle(BaseView):
    def __call__(self):
        self.breadcrumbs.add('News', self.request.route_url('news'))
        try:
            article = self.dbsession.query(News).filter(News.id==self.request.matchdict['articleid']).one()
        except:
            raise HTTPNotFound('No article found.')
        if article.isDeleted:
            raise HTTPNotFound('No article found.')
        
        self.breadcrumbs.add(article.title, self.request.route_url('news_article', articleid=article.id))
        self.title = article.title
        articleHTML = markdown.markdown(article.content, safe_mode='escape')
        
        return self.finalize({'article': article, 'articleHTML': articleHTML})

class NewsSchema(Schema):
    filter_extra_fields = True
    allow_extra_fields = True
    title = validators.UnicodeString(not_empty=True, strip=True)
    content = validators.UnicodeString(not_empty=True, strip=True)
    _csrf = validators.String(not_empty=True, strip=True)

@view_config(route_name='news_create', renderer='templates/news/create.pt')
class NewsCreate(BaseView):
    def __call__(self):
        if self.user.permissions & Permission.NEWS != Permission.NEWS:
            raise HTTPForbidden('You are not authorized to create news articles.')
        self.breadcrumbs.add('News', self.request.route_url('news'))
        self.breadcrumbs.add('Create', self.request.route_url('news_create'))
        self.title = 'Create News Article'
        
        form = Form(self.request, schema=NewsSchema,
                    defaults={'title': u'',
                              'content': u''})
        if 'submit' in self.request.POST and form.validate():
            token = self.request.POST.get('_csrf')
            if token is None or token != self.request.session.get_csrf_token():
                raise HTTPForbidden('CSRF token is invalid or missing.')
            article = News(title=self._validated(NewsSchema, form, 'title'),
                           content=self._validated(NewsSchema, form, 'content'),
                           submitTime=datetime.datetime.utcnow(),
                           lastModified=datetime.datetime.utcnow(),
                           ownerid=self.user.id,
                           isDeleted=False)
            self.dbsession.add(article)
            self.dbsession.flush()
            return HTTPFound(location=self.request.route_url('news_article', articleid=article.id))
        return self.finalize({'form': form})

@view_config(route_name='news_edit', renderer='templates/news/edit.pt')
class NewsEdit(BaseView):
    def __call__(self):
        if self.user.permissions & Permission.NEWS != Permission.NEWS:
            raise HTTPForbidden('You are not authorized to edit this news article.')
        self.breadcrumbs.add('News', self.request.route_url('news'))
        try:
            article = self.dbsession.query(News).filter(News.id==self.request.matchdict['articleid']).one()
        except:
            raise HTTPNotFound('No article found.')
        if article.isDeleted:
            raise HTTPNotFound('No article found.')
        
        self.breadcrumbs.add(article.title, self.request.route_url('news_article', articleid=article.id))
        self.breadcrumbs.add('Edit', self.request.route_url('news_edit', articleid=article.id))
        self.title = 'Editing "' + article.title + '"'
        
        form = Form(self.request, schema=NewsSchema,
                    defaults={'title': article.title,
                              'content': article.content})
        if 'edit' in self.request.POST and form.validate():
            token = self.request.POST.get('_csrf')
            if token is None or token != self.request.session.get_csrf_token():
                raise HTTPForbidden('CSRF token is invalid or missing.')
            article.title = self._validated(NewsSchema, form, 'title')
            article.content = self._validated(NewsSchema, form, 'content')
            article.lastModified = datetime.datetime.utcnow()
            self.dbsession.add(article)
            self.dbsession.flush()
            return HTTPFound(location=self.request.route_url('news_article', articleid=article.id))
        elif 'delete' in self.request.POST and 'deleteCheck' in self.request.POST:
            token = self.request.POST.get('_csrf')
            if token is None or token != self.request.session.get_csrf_token():
                raise HTTPForbidden('CSRF token is invalid or missing.')
            article.isDeleted = True
            self.dbsession.add(article)
            self.dbsession.flush()
            return HTTPFound(location=self.request.route_url('news'))
        return self.finalize({'form': form, 'article': article})

@view_config(route_name='discuss', renderer='templates/discuss/index.pt')
class DiscussIndex(BaseView):
    def __call__(self):
        self.breadcrumbs.add('Discussion', self.request.route_url('discuss'))
        self.title = 'Discussion'
        return self.finalize({})

@view_config(route_name='archives', renderer='templates/archives/index.pt')
class ArchiveIndex(BaseView):
    def __call__(self):
        self.breadcrumbs.add('Archives', self.request.route_url('archives'))
        self.title = 'Archives'
        
        fileList = self.dbsession.query(File).filter(File.isDeleted==False).order_by(File.fileDate.desc()).all()
        
        return self.finalize({'fileList': fileList})

class FileSchema(Schema):
    filter_extra_fields = True
    allow_extra_fields = True
    fileUpload = validators.FieldStorageUploadConverter(not_empty=True)
    title = validators.UnicodeString(not_empty=True, strip=True)
    fileDate = validators.DateConverter(month_style='mm/dd/yyyy', strip=True)
    description = validators.UnicodeString(strip=True)
    _csrf = validators.String(not_empty=True, strip=True)

@view_config(route_name='archives_upload', renderer='templates/archives/upload.pt')
class ArchiveUpload(BaseView):
    def __call__(self):
        if Permission.FILE & self.user.permissions != Permission.FILE:
            raise HTTPForbidden('You are not authorized to upload files.')
        
        self.breadcrumbs.add('Archives', self.request.route_url('archives'))
        self.breadcrumbs.add('Upload', self.request.route_url('archives_upload'))
        self.title = 'Upload File'
        
        form = Form(self.request, schema=FileSchema,
                    defaults={'title': '',
                              'fileDate': '',
                              'description': ''})
        
        if 'submit' in self.request.POST and form.validate():
            token = self.request.POST.get('_csrf')
            if token is None or token != self.request.session.get_csrf_token():
                raise HTTPForbidden('CSRF token is invalid or missing.')
            file = File(name=self._validated(FileSchema, form, 'title'),
                        filename=self._validated(FileSchema, form, 'fileUpload').filename,
                        description=self._validated(FileSchema, form, 'description'),
                        submitTime=datetime.datetime.utcnow(),
                        fileDate=form.data['fileDate'] or datetime.date.today(),
                        ownerid=self.user.id,
                        isDeleted=False)
            self.dbsession.add(file)
            self.dbsession.flush()
            here = os.path.dirname(__file__)
            thisFile = self._validated(FileSchema, form, 'fileUpload').file
            open(os.path.join(here, os.path.pardir, 'data', 'archive', str(file.id)), 'wb').write(\
                thisFile.read())
            return HTTPFound(location=self.request.route_url('archives_file', fileid=file.id))
        return self.finalize({'form': form})

@view_config(route_name='archives_file', renderer='templates/archives/file.pt')
class ArchiveFile(BaseView):
    def __call__(self):
        self.breadcrumbs.add('Archives', self.request.route_url('archives'))
        try:
            file = self.dbsession.query(File).filter(File.id==self.request.matchdict['fileid']).one()
        except:
            raise HTTPNotFound('No file found.')
        if file.isDeleted:
            raise HTTPNotFound('No file found.')
        
        self.breadcrumbs.add(file.name, self.request.route_url('archives_file', fileid=file.id))
        self.title = file.name
        descriptionHTML = markdown.markdown(file.description, safe_mode='escape')
        return self.finalize({'file': file, 'descriptionHTML': descriptionHTML})

@view_config(route_name='archives_download')
class ArchiveDownload(BaseView):
    def __call__(self):
        try:
            file = self.dbsession.query(File).filter(File.id==self.request.matchdict['fileid']).one()
        except:
            return HTTPNotFound('No file found.')
        if file.isDeleted:
            return HTTPNotFound('No file found.')
        here = os.path.dirname(__file__)
        thisFile = open(os.path.join(here, os.path.pardir, 'data', 'archive', str(file.id)), 'rb')
        return Response(content_disposition='attachment; filename=' + file.filename, app_iter=thisFile)

class EditFileSchema(Schema):
    filter_extra_fields = True
    allow_extra_fields = True
    fileUpload = validators.FieldStorageUploadConverter()
    filename = validators.UnicodeString(not_empty=True, strip=True, max=254)
    title = validators.UnicodeString(not_empty=True, strip=True)
    fileDate = validators.DateConverter(month_style='mm/dd/yyyy', strip=True)
    description = validators.UnicodeString(strip=True)
    _csrf = validators.String(not_empty=True, strip=True)

@view_config(route_name='archives_edit', renderer='templates/archives/edit.pt')
class ArchiveEdit(BaseView):
    def __call__(self):
        if Permission.FILE & self.user.permissions != Permission.FILE:
            raise HTTPForbidden('You are not authorized to edit files.')
        
        self.breadcrumbs.add('Archives', self.request.route_url('archives'))
        
        try:
            file = self.dbsession.query(File).filter(File.id==self.request.matchdict['fileid']).one()
        except:
            return HTTPNotFound('No file found.')
        if file.isDeleted:
            return HTTPNotFound('No file found.')
        
        self.breadcrumbs.add(file.name, self.request.route_url('archives_file', fileid=file.id))
        self.breadcrumbs.add('Edit', self.request.route_url('archives_edit', fileid=file.id))
        self.title = 'Editing "' + file.name + '"'
        
        form = Form(self.request, EditFileSchema,
                    defaults={'filename': file.filename,
                              'fileDate': file.fileDate.strftime('%m/%d/%Y'),
                              'title': file.name,
                              'description': file.description})
        
        if 'edit' in self.request.POST and form.validate():
            token = self.request.POST.get('_csrf')
            if token is None or token != self.request.session.get_csrf_token():
                raise HTTPForbidden('CSRF token is invalid or missing.')
            file.filename = self._validated(EditFileSchema, form, 'filename')
            file.name = self._validated(EditFileSchema, form, 'title')
            file.fileDate = form.data['fileDate'] or datetime.date.today()
            file.description = self._validated(EditFileSchema, form, 'description')
            if hasattr(self.request.POST['fileUpload'], 'file'):
                here = os.path.dirname(__file__)
                thisFile = self._validated(FileSchema, form, 'fileUpload').file
                open(os.path.join(here, os.path.pardir, 'data', 'archive', str(file.id)), 'wb').write(\
                    thisFile.read())
                file.submitTime = datetime.datetime.utcnow()
            self.dbsession.add(file)
            self.dbsession.flush()
            return HTTPFound(location=self.request.route_url('archives_file', fileid=file.id))
        elif 'delete' in self.request.POST and 'deleteCheck' in self.request.POST:
            token = self.request.POST.get('_csrf')
            if token is None or token != self.request.session.get_csrf_token():
                raise HTTPForbidden('CSRF token is invalid or missing.')
            file.isDeleted = True
            self.dbsession.add(file)
            self.dbsession.flush()
            return HTTPFound(location=self.request.route_url('archives'))
        
        return self.finalize({'form': form, 'file': file})

@view_config(route_name='events', renderer='templates/events/index.pt')
class EventsIndex(BaseView):
    def __call__(self):
        self.breadcrumbs.add('Events', self.request.route_url('events'))
        self.title = 'Events'
        
        return self.finalize({})

@view_config(route_name='events_add', renderer='templates/events/add.pt')
class EventsAdd(BaseView):
    def __call__(self):
        self.breadcrumbs.add('Events', self.request.route_url('events'))
        self.breadcrumbs.add('Add', self.request.route_url('events_add'))
        self.title = 'Add New Event'
        
        return self.finalize({})