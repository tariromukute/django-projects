from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User as UserModel

# Create your tests here.


class UserTestCase(APITestCase):
    fixtures = ['accounts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_register_user(self):
        data = {'email':'test@gmail.com', 'password':'password', 'first_name':'testfname', 'last_name':'testlname', 'date_of_birth':'1990-10-10'}
        response = self.client.post('/account/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_user(self):
        response = self.client.get('/account/user/1708215211X8KFL2U2TD/')
        #print(response.request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
      
    def test_login(self):
        response = self.client.post('/account/login/', {'username':'tariro@gmail.com', 'password':'password'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class RegisterTestCase(APITestCase):

    def test_register_user_with_valid_data(self):
        data = {'email':'registertest@gmail.com', 'password':'password', 'first_name':'testfname', 'last_name':'testlname', 'date_of_birth':'1990-10-10'}
        response = self.client.post('/account/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = UserModel.objects.get(email='test@gmail.com')
        self.assertEqual(response.data['user_id'], user.user_id)

class VerifyTestCase(APITestCase):
    fixtures = ['accounts/fixtures/test_data.json']
    
    def test_verify_user_email_with_valid_code(self):
        user = UserModel.objects.get(email='notactivetest@gmail.com')
        """ to make sure the account being verified was not active """
        self.assertTrue(not user.is_active)
        response = self.client.get('/account/verify/17082121360H2Q8UNHME/BE5F5DQNZR/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = UserModel.objects.get(email='notactivetestuser@gmail.com')
        self.assertTrue(user.is_active)

class GetUserTestCase(APITestCase):
    fixtures = ['accounts/fixtures/test_data.json']

    def setUp(self):
        token = Token.objects.get(user__email='edittestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        
    def test_get_user_using_valid_user_id(self):
        response = self.client.get('/account/user/17082121360H2Q8UNHME/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ) # data kudzai


class GetDetailedUserTestCase(APITestCase):
    fixtures = ['accounts/fixtures/test_data.json']

    def setUp(self):
        token = Token.objects.get(user__email='edittestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        
    def test_get_user_details_using_valid_user_id(self):
        response = self.client.get('/account/user/details/17082121360H2Q8UNHME/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ) # data kudzai

class EditUserTestCase(APITestCase):
    fixtures = ['accounts/fixtures/test_data.json']

    def setUp(self):
        token = Token.objects.get(user__email='edittestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)    

    def test_edit_user_all_fields_with_valid_data():
        data = {'first_name':'editedfname', 'middle_name':'editedmname', 'date_of_birth':'1992-01-01', 'cell_number':'0777666555', 'country':'zimbabwe'}
        response = self.client.put('account/user/edit/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        """ check if the data has been successfully edited """
        response = self.client.get('/account/user/details/1708215211X8KFL2U2TD/')
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['middle_name'], data['middle_name'])
        self.assertEqual(response.data['last_name'], data['last_name'])
        self.assertEqual(response.data['date_of_birth'], data['date_of_birth'])
        self.assertEqual(response.data['cell_number'], data['cell_number'])
        self.assertEqual(response.data['country'], data['country'])

class DisplayPictureTestCase(APITestCase):
    fixtures = ['accounts/fixtures/test_data.json', 'medias/fixtures/test_data.json']
        
    def test_put_display_picture_with_valid_media_id():
        token = Token.objects.get(user__email='edittestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        response = self.client.put('account/user/display_picture/1708213530I7Z55MK6MH/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_remove_display_picture_where_there_is_one():
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        response = self.client.delete('account/user/display_picture/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    
"""
    Fixture Data Needed
    + User with is_active = false: for account verification
    + User with data to be edit
    + User to be accessed by get user and get user details
    + User with display picture to be put (already on none)
    + User with display picture to be removed (already set)
"""
