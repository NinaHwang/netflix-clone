import json
import jwt
import bcrypt
import re
import jwt_utils

from django.http import JsonResponse
from django.views import View
from django.conf import settings

from .models import User, SubUser, Membership
from profileimage.models import ImageCategory, ProfileImage

# Create your views here.

class CheckEmailView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data['email']
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if not (re.search(regex, email)):
                return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)

            if User.objects.filter(email=email).first() is None:
                return JsonResponse(
                    {
                        'message': 'SIGN_UP',
                        'email': email
                    }, status=200
                )

            return JsonResponse(
                {
                    'message': 'SIGN_IN',
                    'email': email
                }, status=200
            )

        except KeyError as e:
            return JsonResponse({'message': f'KEY_ERROR: {e}'}, status=400)
        except ValueError as e:
            return JsonResponse({'message': f'VALUE_ERROR: {e}'}, status=400)


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data['email']
            password = bcrypt.hashpw(
                data['password'].encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')
            membership = Membership.objects.get(id=data['membership'])

            user = User.objects.create(
                email=email,
                password=password,
                membership=membership,
                is_agreed_marketing=data['is_agreed_marketing']
            )

            SubUser.objects.create(
                user=user,
                name='User' 
            )

            return JsonResponse({'message': 'SIGNUP_SUCCESS'}, status=201)

        except KeyError as e:
            return JsonResponse({'message': f'KEY_ERROR: {e}'}, status=400)
        except ValueError as e:
            return JsonResponse({'message': f'VALUE_ERROR: {e}'}, status=400)


class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data['email']
            pw_input = data['password']

            user = User.objects.prefetch_related(
                'subuser_set'
            ).filter(email=email).first()
            
            if user is None:
                return JsonResponse(
                    {'message': 'WRONG_EMAIL'},
                    status=401
                )

            if bcrypt.checkpw(
                pw_input.encode('utf-8'),
                user.password.encode('utf-8')
            ):
                key = settings.SECRET_KEY
                algorithm = settings.JWT_ALGORITHM
                token = jwt.encode(
                    {'user': user.id},
                    key,
                    algorithm=algorithm
                ).decode('utf-8')

                return JsonResponse(
                    {
                        'message': 'SIGNIN_SUCCESS',
                        'token' : token,
                        'subusers': [
                            {
                                'id': subuser.id,
                                'name': subuser.name,
                                'image': subuser.image.image_url
                            } for subuser in user.subuser_set.all()
                        ]
                    }, status=200
                )

            return JsonResponse({'message': 'WRONG_PASSWORD'}, status=401)

        except KeyError as e:
            return JsonResponse({'message': f'KEY_ERROR: {e}'}, status=400)
        except ValueError as e:
            return JsonResponse({'message': f'VALUE_ERROR: {e}'}, status=400)


class ShowProfileImagesView(View):
    @jwt_utils.token
    def get(self, request):
        categories = ImageCategory.objects.prefetch_related(
            'profileimage_set'
        ).all() 
        return JsonResponse(
            {
                'images': [
                    {
                        'category': category.name,
                        'image': [
                            {
                                'id': image.id,
                                'url': image.url
                            } for image in category.profileimage_set.all()
                        ]
                    } for category in categories
                ]
            }
        )


class CreateSubUserView(View):
    @jwt_utils.token
    def post(self, request):
        try:
            if request.status == 'user':
                target = request.user
            else:
                target = request.user.user

            if target.subuser_set.count() == target.membership.subuser_cnt:
                return JsonResponse({'message': 'NO_MORE_USERS'}, status=200)

            data = json.loads(request.body)
            image = ProfileImage.objects.get(id=data['image'])

            SubUser.objects.create(
                user=target,
                name=data['name'],
                image=image
            )

            return JsonResponse({'message': 'CREATED'}, status=201)

        except KeyError as e:
            return JsonResponse({'message': f'KEY_ERROR: {e}'}, status=400)
        except ValueError as e:
            return JsonResponse({'message': f'VALUE_ERROR: {e}'}, status=400)


class SubUserSignInView(View):
    @jwt_utils.token
    def post(self, request):
        if request.status == 'user':
            target = request.user
        else:
            target = request.user.user

        data = json.loads(request.body)

        subuser = SubUser.objects.filter(
            user=target,
            id=data['id']
        ).first()

        if subuser is None:
            return JsonResponse({'message': 'INVALID_PROFILE'}, status=403)

        key = settings.SECRET_KEY
        algorithm = settings.JWT_ALGORITHM
        token = jwt.encode(
            {'subuser': subuser.id},
            key,
            algorithm=algorithm
        ).decode('utf-8')

        return JsonResponse(
            {
                'message': 'SUBUSER_SIGNIN',
                'token': token,
                'name': subuser.name,
                'image': subuser.image.image_url
            }, status=200
        )

        
class ManageSubUserView(View):
    @jwt_utils.token
    def post(self, request, subuser_id):
        data = json.loads(request.body)

        target = SubUser.obejcts.get(id=subuser_id)

        if 'image' in data.keys():
            image = ProfileImage.objects.get(id=data['image'])
            target.image = image

        if 'name' in data.keys():
            target.name = data['name']

        target.save()

        return JsonResponse({'message': 'UPDATED'}, status=200)
