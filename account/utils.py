from django.contrib.auth import login, logout, user_logged_in, user_logged_out
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.authtoken.models import Token


def encode_uid(pk):
    return force_str(urlsafe_base64_encode(force_bytes(pk)))


def decode_uid(pk):
    return force_str(urlsafe_base64_decode(pk))


def login_user(request, user):
    token, _ = Token.objects.get_or_create(user=user)

    # TODO session management
    login(request, user)
    user_logged_in.send(sender=user.__class__, request=request, user=user)
    return token
