from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User as UserModel

# Create your tests here.


class InviteTestCase(APITestCase):
    fixtures = ['accounts/fixtures/test_data.json', 'fans/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='fantestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_register_user(self):
        data = {'email':'test@gmail.com', 'password':'password', 'first_name':'testfname', 'last_name':'testlname', 'date_of_birth':'1990-10-10'}
        response = self.client.post('/account/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ListRequestTestCase(APITestCase):
    fixtures = ['accounts/fixtures/test_data.json', 'fans/fixtures/test_data.json',]
    
    def setUp(self):
        token = Token.objects.get(user__email='fantestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        
    def test_get_list_of_requests(self):
        response  = self.client.get('/fan/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # check the return data against the known
        

class RequestTestCase(APITestCase):
    fixtures = ['accounts/fixtures/test_data.json', 'fans/fixtures/test_data.json',]
    
    def setUp(self):
        token = Token.objects.get(user__email='fantestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        
    def test_get_number_of_new_requests(self):
        number_of_requests = 2
        response = self.client.get('/fan/count/requests')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, number_of_requests)
        
    def test_request_to_follow_public_user_using_valid_data(self):
        response = self.client.post('/fan/request/requestpubtestuser/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        fan = FanModel.objects.get(o_user__email='requestpubtestuser@gmail.com')
        self.assertEqual(fan.x_user.email, 'fantestuser@gmail.com')
        
    def test_request_to_follow_private_user_using_valid_data(self):
        response = self.client.post('/fan/request/requestpvttestuser/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        follow = RequestModel.objects.get(o_user__email='requestpvttestuser@gmail.com')
        self.assertEqual(follow.x_user.email, 'fantestuser@gmail.com')
        
    def test_accept_follow_request_using_valid_data(self):
        response = self.client.put('/fan/request/accept/requestaccepttestuser/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        follow = RequestModel.objects.get(o_user__email='requestaccepttestuser@gmail.com')
        self.assertEqual(fan.x_user.email, 'fantestuser@gmail.com')
        fan =  FanModel.objects.get(o_user__email='requestaccepttestuser@gmail.com')
        self.assertEqual(fan.x_user.email, 'fantestuser@gmail.com')
        
    def test_decline_follow_request_using_valid_data(self):
        response = self.client.put('/fan/request/decline/requestaccepttestuser/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        follow = RequestModel.objects.get(o_user__email='requestaccepttestuser@gmail.com')
        self.assertEqual(fan.x_user.email, 'fantestuser@gmail.com')
        fan =  FanModel.objects.get(o_user__email='requestaccepttestuser@gmail.com')
        self.assertEqual(fan.x_user.email, 'fantestuser@gmail.com')
        
    def test_delete_follow_request_using_valid_data(self):
        response = self.client.delete('/fan/remove/request/requestdeltestuserid/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        

class FanSeenTestCase(APITestCase):
    fixtures = ['accounts/fixtures/test_data.json', 'fans/fixtures/test_data.json',]
    
    def setUp(self):
        token = Token.objects.get(user__email='fantestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        
    def test_user_seen_all_new_fans_using_valid_data(self):
        response = self.client.post('/fan/seen/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #count number of fan with seen=false
        #assert that they are equal to zero

    def test_user_seen_a_new_fan_using_valid_data(self):
        response = self.client.put('/fan/seen/follwrequestuser/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #query fan that has just been seen
        #assert that the seen status has changed
        
        
"""
    Fixture Data Needed
    + requesttestuser   => to get list of follow request, from: requestaccept...@gmail.com, requestdecline..@gmail.com       
                        => to get number of new request, from: requestaccept...@gmail.com, requestdecline..@gmail.com
                        => to follow public and private user accounts: requestpub..@gmail.com, requestpvt..@gmail.com
                        => to delete follow request, from: requestdel..@gmail.com
                        
    + fantestuser       => put seen on all unseen fans: fanseen1..@gmail.com, fanseen2..@gmail.com
    + fan2testuser      => put seen  on  an  unseen fan: fanseen1..@gmail.com
    
"""  
                   
        
