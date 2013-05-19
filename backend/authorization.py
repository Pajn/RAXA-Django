from django.core.urlresolvers import reverse
from django.utils.crypto import get_random_string
from django.http import HttpResponse

from backend.models.User import User
from RAXA.settings import LOCAL_IP_RANGES


class LoginRedirect(HttpResponse):
    status_code = 307

    def __init__(self, request):
        HttpResponse.__init__(self)
        app = get_app(request.path)
        self['Location'] = reverse(app + '.views.login')
        request.session['url'] = request.get_full_path()


class Auth():
    ip = None

    def process_request(self, request):
        self.ip = self.get_client_ip(request)

        if 'key' in request.REQUEST:
            secret = request.REQUEST['key']
        else:
            secret = None

        if self.is_authorized(request, secret):
            return None
        else:
            return LoginRedirect(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return str(ip)

    def is_local(self):
        for ip in LOCAL_IP_RANGES:
            if self.ip.startswith(ip):
                return True
        return False

    def is_authorized(self, request, secret=None):
        try:
            user = User.objects.get(username='Default')
        except User.DoesNotExist:
            user = User(username='Default')
            user.api_key = get_random_string(length=40)
            user.set_password('')
            user.save()

        request.session['user'] = user
        request.session['theme'] = user.theme

        if not request.path.endswith('/login/'):
            if not request.session.get('auth', default=0) == 1:
                if user.is_active:
                    if not (user.allow_local and self.is_local()):
                        if not secret == user.api_key:
                            if not self.ip.startswith('127.0.0'):
                                if get_app(request.path) == 'api':
                                    request.session['auth'] = -1
                                    return True
                                else:
                                    return False
                request.session['auth'] = 1
        return True


def get_user():
    try:
        user = User.objects.get(username='Default')
    except User.DoesNotExist:
        user = User(username='Default')
        user.api_key = get_random_string(length=40)
        user.set_password('')
        user.save()

    return user


def get_app(url):
    parts = str(url).split('/')
    if parts[1] in ['api', 'backend', 'common', 'desktop', 'mobile', 'tablet']:
        return parts[1]
    if parts.__len__() < 3:
        return 'desktop'
    if parts[2] in ['api', 'backend', 'common', 'desktop', 'mobile', 'tablet']:
        return parts[2]
    return 'desktop'