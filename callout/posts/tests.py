from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from posts.models import Remark as RemarkModel

# Create your tests here.

class GetListOfPostsTestCase(APITestCase):
    fixtures = ['posts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_get_list_of_post_with_valid_token():
        response = self.client.get('/post/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetPostTestCase(APITestCase):
    fixtures = ['posts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_get_another_users_post_with_valid_post_id():
        response = self.client.get('/post/postidforanotheruser')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, )


class DeletePostTestCase(APITestCase):
    fixtures = ['posts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_remove_post_using_valid_post_id():
        response = self.client.delete('/post/remove/idofpostofuser/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class EditPostTestCase(APITestCase):
    fixtures = ['posts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_edit_post_using_valid_parameters():
        data = {}
        response = self.client.put('/post/edit/postidtoedit/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get('/post/postidforanotheruser')
        self.assertEqual(response.status_code, data)


class CreatePostTestCase(APITestCase):
    fixtures = ['posts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_create_post_with_valid_parameters():
        data = {}
        response = self.client.post('/post/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetListOfPostRemarks(APITestCase):
    fixtures = ['posts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_get_list_of_post_remmarks_using_valid_parameters():
        response = self.client.get('/post/remarks/xxxxxx/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreatePostRemark(APITestCase):
    fixtures = ['posts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='edittestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_create_post_remark_with_valid_parameters():
        data = {}
        response = self.client.post('/post/remark/xxxxx', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EditPostRemarkTestCase(APITestCase):
    fixtures = ['posts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='edittestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_edit_post_remark_using_valid_parameters():
        data = {}
        response = self.client.put('/post/edit/remark/xxxxx/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        remark = RemarkModel.objects.get(remark_id='xxxxx')
        self.assertEqual(remark.remark, 'remark has been successfully edited')

class DeletePostRemarkTestCase(APITestCase):
    fixtures = ['posts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_remove_post_remark_using_valid_parameters():
        response = self.client.delete('/post/remove/remark/xxxxx/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class CountPostRemarksTestCase(APITestCase):
    fixtures = ['posts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_count_number_of_post_remarks_using_parameters():
        response = self.client.get('/post/count/remarks/xxxx/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {5})

class GetListOfPostReactionsTestCase(APITestCase):
    fixtures = ['posts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_get_list_of_post_reactions_using_valid_parameters():
        response = self.client.get('/post/reactions/xxxx/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreatePostReactionTestCase(APITestCase):
    fixtures = ['posts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='edittestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_create_post_reaction_using_valid_parameters():
        response = self.client.post('/post/reaction/xxxxx/fancy/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class EditPostReactionTestCase(APITestCase):
    fixtures = ['posts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_edit_post_reaction_using_valid_parameters():
        response = self.client.put('/post/edit/reaction/xxxxx/disapproval/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class DeletePostReactionTestCase(APITestCase):
    fixtures = ['posts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_remove_post_reaction_using_valid_parameters():
        response = self.client.delete('/post/remove/reaction/xxxx/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class GetNumberOfPostReactionsTestCase(APITestCase):
    fixtures = ['posts/fixtures/test_data.json',]

    def setUp(self):
        token = Token.objects.get(user__email='gettestuser@gmail.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)

    def test_get_number_of_post_reactions_using_valid_parameters():
        response = self.client.get('/post/count/reactions/xxxxx/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {2})


"""
   Post Data Needed
   + Post by gettestuser@gmail.com   => for list of remarks
                                     => to be remarked on (by edittestuser@gmail.com)
                                     => to have remarks counted
                                     => with a remark to be edited (by edittestuser@gmail.com)
                                     => to be reacted (by edittestuser@gmail.com)

   + Post by gettestuser@gmail.com   => to be deleted

   + Post by gettestuser@gmail.com   => to be edited
    
   + Post by edittestuser@gmail.com  => with a remark to be deleted (by gettestuser@gmail.com)
                                     => for list of reactions
                                     => with reaction to be deleted (by gettestuser@gmail.com)
                                     => with reaction to be edited (by getestuser@gmail.com)
"""
    

