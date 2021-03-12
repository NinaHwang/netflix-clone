import os
import jwt
import json
import my_settings

from pathlib import Path
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.conf import settings

from user.models import Subuser, User

def token(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization', None)
            key = settings.SECRET_KEY
            algorithm = settings.JWT_ALGORITHM

            if token is None:
                return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)

            decode = jwt.decode(token, key, algorithm=algorithm)

            if 'subuser' in decode:
                request.status = 'subuser'
                request.user = Subuser.objects.get(id=decode['subuser'])
            elif 'user' in decode:
                request.status = 'user'
                request.user = User.objects.get(id=decode['user'])

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'EXPIRED_TOKEN'}, status=400)
        
        return func(self, request, *args, **kwargs)

    return wrapper
