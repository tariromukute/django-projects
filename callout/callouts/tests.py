from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from callouts.models import Remark as RemarkModel

# Create your tests here.

class GetListOfCalloutsTestCase(APITestCase):
    fixtures = ['callouts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_get_list_of_callout_with_valid_token():
        response = self.client.get('/callout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetCalloutTestCase(APITestCase):
    fixtures = ['callouts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_get_another_users_callout_with_valid_callout_id():
        response = self.client.get('/callout/postidforanotheruser')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, )


class DeleteCalloutTestCase(APITestCase):
    fixtures = ['callouts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_remove_callout_using_valid_callout_id():
        response = self.client.delete('/callout/remove/idofpostofuser/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class EditCalloutTestCase(APITestCase):
    fixtures = ['callouts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_edit_callout_using_valid_parameters():
        data = {}
        response = self.client.put('/callout/edit/postidtoedit/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get('/callout/postidforanotheruser')
        self.assertEqual(response.status_code, data)


class ChallengePostsTestCase(APITestCase):
    fixtures = ['callouts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_challenge_post_with_valid_parameters():
        data = {}
        response = self.client.post('/callout/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CalloutChallengeTestCase(APITestCase):
    fixtures = ['callouts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email'edittestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_accept_challenge_using_valid_parameters():
        response = self.client.put('/callout/challenge/accept/xxxxx/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class GetListOfCalloutRemarks(APITestCase):
    fixtures = ['callouts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_get_list_of_callout_remmarks_using_valid_parameters():
        response = self.client.get('/callout/remarks/xxxxxx/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateCalloutRemark(APITestCase):
    fixtures = ['callouts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='edittestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_create_callout_remark_with_valid_parameters():
        data = {}
        response = self.client.post('/callout/remark/xxxxx', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EditCalloutRemarkTestCase(APITestCase):
    fixtures = ['callouts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='edittestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_edit_callout_remark_using_valid_parameters():
        data = {}
        response = self.client.put('/callout/edit/remark/xxxxx/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        remark = RemarkModel.objects.get(remark_id='xxxxx')
        self.assertEqual(remark.remark, 'remark has been successfully edited')

class DeleteCalloutRemarkTestCase(APITestCase):
    fixtures = ['callouts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_remove_callout_remark_using_valid_parameters():
        response = self.client.delete('/callout/remove/remark/xxxxx/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class CountCalloutRemarksTestCase(APITestCase):
    fixtures = ['callouts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_count_number_of_callout_remarks_using_parameters():
        response = self.client.get('/callout/count/remarks/xxxx/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {5})

class GetListOfCalloutReactionsTestCase(APITestCase):
    fixtures = ['callouts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_get_list_of_callout_reactions_using_valid_parameters():
        response = self.client.get('/callout/reactions/xxxx/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateCalloutReactionTestCase(APITestCase):
    fixtures = ['callouts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='edittestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_create_callout_reaction_using_valid_parameters():
        response = self.client.post('/callout/reaction/xxxxx/fancy/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class EditCalloutReactionTestCase(APITestCase):
    fixtures = ['callouts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_edit_callout_reaction_using_valid_parameters():
        response = self.client.put('/callout/edit/reaction/xxxxx/disapproval/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class DeleteCalloutReactionTestCase(APITestCase):
    fixtures = ['callouts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_remove_callout_reaction_using_valid_parameters():
        response = self.client.delete('/callout/remove/reaction/xxxx/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class GetNumberOfCalloutReactionsTestCase(APITestCase):
    fixtures = ['callouts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_get_number_of_callout_reactions_using_valid_parameters():
        response = self.client.get('/callout/count/reactions/xxxxx/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {2})


"""
   Callout Data Needed
   + Callout by gettestuser@gmail.com   => for list of remarks
                                        => to be remarked on (by edittestuser@gmail.com)
                                        => to have remarks counted
                                        => with a remark to be edited (by edittestuser@gmail.com)
                                        => to be reacted (by edittestuser@gmail.com)

   + Callout by gettestuser@gmail.com   => to be deleted

   + Callout by gettestuser@gmail.com   => to be edited

   + Callout challenge to edittestuser@gmail.com => to be accepted

   + Callout challenge to edittestuser@gmail.com => to be declined
    
   + Callout by edittestuser@gmail.com  => with a remark to be deleted (by gettestuser@gmail.com)
                                        => for list of reactions
                                        => with reaction to be deleted (by gettestuser@gmail.com)
                                        => with reaction to be edited (by getestuser@gmail.com)
"""
    

