import json
import jwt
import jwt_utils
import bcrypt

from django.test import TestCase, Client
from django.conf import settings

from .models import Membership, User, SubUser

# Create your tests here.

class CheckEmailTest(TestCase):
    def setUp(self):
        membership1 = Membership.objects.create(
            name='1',
            subuser_cnt=4
        )
        existing_user = User.objects.create(
            email='1234@hi.com',
            password='12341234',
            membership=membership1,
            is_agreed_marketing=1
        )

    def tearDown(self):
        Membership.objects.all().delete()
        User.objects.all().delete()

    def test_CheckEmailView_post_success_new(self):
        client = Client()

        email = {
            'email': 'nina@hi.com'
        }

        response = client.post(
            '/user/email',
            json.dumps(email),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {'message':'SIGN_UP', 'email':'nina@hi.com'})

    def test_CheckEmailView_post_success_existed(self):
        client = Client()

        email = {
            'email': '1234@hi.com'
        }

        response = client.post(
            '/user/email',
            json.dumps(email),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {'message':'SIGN_IN', 'email':'1234@hi.com'})

    def test_CheckEmailView_post_fail_regex(self):
        client = Client()

        email = {
            'email': 'nina.com'
        }

        response = client.post(
            '/user/email',
            json.dumps(email),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {'message':'INVALID_EMAIL'})



class SignUpTest(TestCase):
    def setUp(self):
        membership1 = Membership.objects.create(
            name='1',
            subuser_cnt=4
        )
        self.membership1_id = membership1.id

    def tearDown(self):
        Membership.objects.all().delete()
        User.objects.all().delete()
        SubUser.objects.all().delete()

    def test_signuptest_post_success(self):
        client = Client()

        data = {
            'email':'nina@hi.com',
            'password':'12341234',
            'membership':self.membership1_id,
            'is_agreed_marketing':0
        }

        response = client.post(
            '/user/signup',
            json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code,201)
        print(User.objects.all().values())
        print(SubUser.objects.all().values())


class SignInTest(TestCase):
    def setUp(self):
        membership1 = Membership.objects.create(
            name='1',
            subuser_cnt=4
        )
        self.membership1_id = membership1.id
        user = User.objects.create(
            email='1234@hi.com',
            password=bcrypt.hashpw('12341234'.encode('utf-8'),
                                  bcrypt.gensalt()).decode('utf-8'),
            membership=membership1,
            is_agreed_marketing=1
        )
        self.user_id = user.id
        subuser1 = SubUser.objects.create(
            user=user,
            name='first'
        )
        subuser2 = SubUser.objects.create(
            user=user,
            name='second'
        )
    
    def tearDown(self):
        Membership.objects.all().delete()
        User.objects.all().delete()
        SubUser.objects.all().delete()

    def test_SignInView_post_success(self):
        client = Client()

        data = {
            'email': '1234@hi.com',
            'password': '12341234',
        }

        response = client.post(
            '/user/signin',
            json.dumps(data),
            content_type='applicaion/json'
        )

        self.assertEqual(response.status_code,200)
        print(response.json())

    def test_SignInView_post_fail_email(self):
        client = Client()

        data = {
            'email': 'nina@hi.com',
            'password': '12341234',
        }

        response = client.post(
            '/user/signin',
            json.dumps(data),
            content_type='applicaion/json'
        )

        self.assertEqual(response.status_code,401)
        self.assertEqual(response.json(),{'message': 'WRONG_EMAIL'})

    def test_SignInView_post_fail_pw(self):
        client = Client()

        data = {
            'email': '1234@hi.com',
            'password': '1234',
        }

        response = client.post(
            '/user/signin',
            json.dumps(data),
            content_type='applicaion/json'
        )

        self.assertEqual(response.status_code,401)
        self.assertEqual(response.json(),{'message': 'WRONG_PASSWORD'})


class CreateSubUserTest(TestCase):
    def setUp(self):
        membership1 = Membership.objects.create(
            name='1',
            subuser_cnt=4
        )
        self.membership1_id = membership1.id
        membership2 = Membership.objects.create(
            name='2',
            subuser_cnt=1
        )
        user1 = User.objects.create(
            email='1234@hi.com',
            password=bcrypt.hashpw('12341234'.encode('utf-8'),
                                  bcrypt.gensalt()).decode('utf-8'),
            membership=membership1,
            is_agreed_marketing=1
        )
        self.user1_id = user1.id
        self.user1_token = jwt.encode(
            {'user': user1.id},
            settings.SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        ).decode('utf-8')
        user2 = User.objects.create(
            email='123@hello.com',
            password=bcrypt.hashpw('123123'.encode('utf-8'),
                                  bcrypt.gensalt()).decode('utf-8'),
            membership=membership2,
            is_agreed_marketing=1
        )
        self.user2_id = user2.id
        self.user2_token = jwt.encode(
            {'user': user2.id},
            settings.SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        ).decode('utf-8')
        user2sub = SubUser.objects.create(
            name='서브유저',
            user=user2
        )
        
    def tearDown(self):
        Membership.objects.all().delete()
        User.objects.all().delete()
        SubUser.objects.all().delete()

    def test_CreateSubUserView_post_success(self):
        client = Client()
        header = {'HTTP_Authorization': self.user1_token}
        token = header['HTTP_Authorization']
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.JWT_ALGORITHM
        )
        subuser = {
            'name':'유저1 서브유저'
        }
        
        response = client.post(
            '/user/profile/create',
            json.dumps(subuser),
            **header,
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': 'CREATED'})

    def test_CreateSubUserView_post_fail_max(self):
        client = Client()
        header = {'HTTP_Authorization': self.user2_token}
        token = header['HTTP_Authorization']
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.JWT_ALGORITHM
        )
        subuser = {
            'name':'유저2 서브유저'
        }
        
        response = client.post(
            '/user/profile/create',
            json.dumps(subuser),
            **header,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'NO_MORE_USERS'})


class SubUserSignInTest(TestCase):
    def setUp(self):
        membership1 = Membership.objects.create(
            name='1',
            subuser_cnt=4
        )
        self.membership1_id = membership1.id
        user1 = User.objects.create(
            email='1234@hi.com',
            password=bcrypt.hashpw('12341234'.encode('utf-8'),
                                  bcrypt.gensalt()).decode('utf-8'),
            membership=membership1,
            is_agreed_marketing=1
        )
        self.user1_id = user1.id
        self.user1_token = jwt.encode(
            {'user': user1.id},
            settings.SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        ).decode('utf-8')
        user1sub = SubUser.objects.create(
            name='서브유저1',
            user=user1
        )
        self.user1sub_id = user1sub.id
        user2 = User.objects.create(
            email='123@hello.com',
            password=bcrypt.hashpw('123123'.encode('utf-8'),
                                  bcrypt.gensalt()).decode('utf-8'),
            membership=membership1,
            is_agreed_marketing=1
        )
        self.user2_id = user2.id
        self.user2_token = jwt.encode(
            {'user': user2.id},
            settings.SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        ).decode('utf-8')
        user2sub = SubUser.objects.create(
            name='서브유저2',
            user=user2
        )
        self.user2sub_id = user2sub.id


    def tearDown(self):
        Membership.objects.all().delete()
        User.objects.all().delete()
        SubUser.objects.all().delete()

    def test_SubUserSignInView_post_success(self):
        client = Client()
        header = {'HTTP_Authorization': self.user1_token}
        token = header['HTTP_Authorization']
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.JWT_ALGORITHM
        )
        subuser = {
            'id': self.user1sub_id
        }

        response = client.post(
            '/user/profile/signin',
            json.dumps(subuser),
            **header,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        print(response.json())

    def test_SubUserSignInView_post_fail_invalid(self):
        client = Client()
        header = {'HTTP_Authorization': self.user1_token}
        token = header['HTTP_Authorization']
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.JWT_ALGORITHM
        )
        subuser = {
            'id': self.user2sub_id
        }

        response = client.post(
            '/user/profile/signin',
            json.dumps(subuser),
            **header,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'message':'INVALID_PROFILE'})

