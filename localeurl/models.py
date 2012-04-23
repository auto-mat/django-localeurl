from django.conf import settings
from django.core import urlresolvers
from django.utils import translation
from django.contrib.auth import views as auth_views
from localeurl import utils


def reverse(*args, **kwargs):
    reverse_kwargs = kwargs.get('kwargs') or {}
    locale = utils.supported_language(reverse_kwargs.pop(
            'locale', translation.get_language()))
    url = django_reverse(*args, **kwargs)
    _, path = utils.strip_script_prefix(url)
    return utils.locale_url(path, locale)

django_reverse = None

def patch_reverse():
    """
    Monkey-patches the urlresolvers.reverse function. Will not patch twice.
    """
    global django_reverse
    if urlresolvers.reverse is not reverse:
        django_reverse = urlresolvers.reverse
        urlresolvers.reverse = reverse


def redirect_to_login(next, login_url, *args, **kwargs):
    if not login_url:
        login_url = settings.LOGIN_URL
    login_url = utils.locale_url(login_url, translation.get_language())
    return django_redirect_to_login(next, login_url, *args, **kwargs)

django_redirect_to_login = None

def patch_redirect_to_login():
    """
    Monkey-patches the redirect_to_login function. Will not patch twice.
    """
    global django_redirect_to_login
    if auth_views.redirect_to_login is not redirect_to_login:
        django_redirect_to_login = auth_views.redirect_to_login
        auth_views.redirect_to_login = redirect_to_login


if settings.USE_I18N:
    patch_reverse()
    patch_redirect_to_login()
