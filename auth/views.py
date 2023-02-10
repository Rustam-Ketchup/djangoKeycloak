import json
import requests
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from oic.oic.message import AuthorizationResponse
from rest_framework import viewsets, status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.decorators import api_view
from keycloak import KeycloakOpenID, KeycloakAdmin
from rest_framework.response import Response
from rest_framework.views import APIView
from oic.oic import Client
from oic.utils.authn.client import CLIENT_AUTHN_METHOD

SERVER_URL = "http://localhost:8080/"
CLIENT_ID = "django-client"
REALM_NAME = "django"
CLIENT_SECRET_KEY = "oUneMmBdGZ4rhweDaCLe5g6OO3koLtaF"
AUTH_URL = f"http://localhost:8080/admin/realms/{REALM_NAME}/protocol/openid-connect/auth"
TOKEN_URL = f"http://localhost:8080/admin/realms/{REALM_NAME}/protocol/openid-connect/token"
USERS_URL = f"http://localhost:8080/admin/realms/gateway/users"
REDIRECTION_URL = "http://localhost:8000/index/redir"
SCOPE = "openid"

keycloak_openid = KeycloakOpenID(server_url=SERVER_URL,
                                 client_id=CLIENT_ID,
                                 realm_name=REALM_NAME,
                                 client_secret_key=CLIENT_SECRET_KEY)

# keycloak_admin = KeycloakAdmin(server_url=TOKEN_URL,
#                                username='bashh',
#                                password='1234',
#                                realm_name="django",
#                                client_id=CLIENT_ID,
#                                client_secret_key=CLIENT_SECRET_KEY,
#                                verify=True)


class Keycloak(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        code = request.query_params["code"]

        access_token = keycloak_openid.token(grant_type='authorization_code',
                                             code=code,
                                             redirect_uri="http://localhost:8000/index/redir")

        userinfo = keycloak_openid.userinfo(access_token["access_token"])
        print(userinfo)


        # users = keycloak_admin.get_users({})
        # print(users)

        # response = requests.post(
        #     TOKEN_URL,
        #     params=dict(grant_type='authorization_code',
        #                 code=code,
        #                 redirect_uri=['http://localhost:8000/index/redir'],
        #                 client_id=CLIENT_ID),
        #     headers=dict(connection='keep-alive',
        #                  content_type='application/x-www-form-urlencoded'))
        #
        # print(response.text, response.status_code)
        return Response({'body': "access_token"}, template_name="keycloak_login.html")


class Index(APIView):
    template = 'index.html'
    renderer_classes = [TemplateHTMLRenderer]

    config_well_known = keycloak_openid.well_known()

    auth_url = keycloak_openid.auth_url(redirect_uri=REDIRECTION_URL,
                                        scope=SCOPE)

    response = requests.post(
        'http://localhost:8080/realms/django/protocol/openid-connect/token',
        params=dict(grant_type='password',
                    username='bashh',
                    password='1234',
                    client_id='admin-cli'),
        headers=dict(connection='keep-alive', content_type='application/x-www-form-urlencoded'))
    print(response.text)

    # response = requests.get(auth_url, params=dict(grant_type="authorization_code",
    #                                               client_id=CLIENT_ID,
    #                                               client_secret=CLIENT_SECRET_KEY,
    #                                               redirect_uri=[redirection_url],
    #                                               response_type="code",
    #                                               scope=[scope]))

    def get(self, request):
        return Response({'auth_url': self.auth_url}, template_name='index.html')
