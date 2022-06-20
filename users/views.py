from users.models import User


def debug(request):
    tmp = User.objects.create()
    return
