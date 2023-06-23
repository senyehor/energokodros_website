import functools

from django.http import HttpResponse


def admin(function):
    @functools.wraps(function)
    def _wrapper(request, *args, **kwargs):
        return function(request, *args, **kwargs) \
            if request.user.is_authenticated and request.user.is_admin \
            else HttpResponse(status=403)

    return _wrapper
