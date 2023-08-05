from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from django.utils.timezone import now
from django.contrib.sessions.models import Session

import requests
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest


def include_auth_urls():
    return include([
        path(r'login/', login),
        path(r'logout/', logout)
    ])

def include_internal_urls():
    return include([
        path(r'sessions/flush/', flush_session_view),
    ])

@api_view(["GET"])
@authentication_classes([])
def login(request):
    auth_redirect_url: str = request.build_absolute_uri().split("?")[0]
    # since the app is running in container, no way to know its on ssl
    auth_redirect_url = auth_redirect_url.replace('http', 'https')
    auth_code: str = request.query_params.get("code", "")
    app_redirect_url: str = request.query_params.get("state", "")

    client_id = settings.IDENTITY_CLIENT_ID
    client_secret = settings.IDENTITY_CLIENT_SECRET

    reply = requests.post(
        f"{settings.IDENTITY_HOST}/o/token/",
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": auth_redirect_url,
        },
        auth=(client_id, client_secret),
    )
    try:
        reply.raise_for_status()
    except requests.exceptions.HTTPError as e:
        message = (
            "Auth request failed with status %s: %s; %s",
            e.response.status_code,
            e.response.content,
            auth_redirect_url
        )
        return HttpResponse(f"Unauthorized: {message}", status=401)

    tokens = reply.json()
    introspect_response = requests.post(
        f"{settings.IDENTITY_HOST}/o/introspect/",
        data={"token": tokens["access_token"],},
        headers={"Authorization": "Bearer " + tokens["access_token"]},
    )
    try:
        reply.raise_for_status()
    except requests.exceptions.HTTPError as e:
        message = (
            "Auth request failed with status %s: %s; %s",
            e.response.status_code,
            e.response.content,
            tokens["access_token"]
        )
        return HttpResponse(f"Unauthorized: {message}", status=401)

    email = introspect_response.json()["username"]
    # here we can also get additional user info, GUID, etc
    user, _ = User.objects.get_or_create(email=email, username=email)
    request.session["username"] = email

    return HttpResponseRedirect(redirect_to=app_redirect_url)


@api_view(["GET"])
@authentication_classes([])
def logout(request):
    app_redirect_url: str = request.query_params.get("state", "")
    request.session.flush()
    response = HttpResponseRedirect(redirect_to=app_redirect_url)
    response.delete_cookie("sso_shared_session")
    return response

@api_view(["POST"])
def flush_session_view(request):
    email = request.data["email"]
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponseBadRequest({"reason": "no such user!"})
    delete_all_unexpired_sessions_for_user(user)
    return Response({"flushed_session": f"{email}"})


def delete_all_unexpired_sessions_for_user(user):
    """
    This is pretty inefficient, and will log the user out across all devices
    however, on our scale should work fine.
    We can upgrade this setup later to store session/user pairs in a separate
    custom table
    :param user:
    :return:
    """
    all_sessions = Session.objects.filter(expire_date__gte=now())
    user_sessions = [
        session.pk
        for session in all_sessions
        if str(user.pk) == session.get_decoded().get("_auth_user_id")
    ]
    Session.objects.filter(pk__in=user_sessions).delete()
