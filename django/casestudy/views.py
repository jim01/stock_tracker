"""
For more information on setting up DRF views see docs:
https://www.django-rest-framework.org/api-guide/views/#class-based-views
"""
import os

from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q
from casestudy.models import Security


class LoginView(APIView):
    """
    Login view for the API.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        """
        Login view for the API.
        """
        username = request.data['username']
        user = User.objects.get(username=username)
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        return Response(user_data)

class SecurityView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        """
        Login view for the API.
        """
        query = request.GET.get('q', '')
        security_list = Security.objects.filter(Q(ticker__istartswith=query) | Q(name__istartswith=query)).values()
        return Response(security_list)

class UserSecurityView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        """"
        user security
        """
        user_id = request.headers['x-user-id']
        security_list = Security.objects.filter(users=user_id).values()
        return Response(security_list)

    def post(self, request, format=None):
        """"
        Add Security for user
        """
        user_id = request.headers['x-user-id']
        security_id = request.data['id']
        security = Security.objects.get(id=security_id)
        user = User.objects.get(id=user_id)
        security.users.add(user)
        return Response()

    def delete(self, request, format=None):
        """"
        Remove Security for user
        """
        user_id = request.headers['x-user-id']
        security_id = request.data['id']
        security = Security.objects.get(id=security_id)
        user = User.objects.get(id=user_id)
        security.users.remove(user)
        return Response()
