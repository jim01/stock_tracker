from django.test import TestCase
from casestudy.models import Security
from django.contrib.auth.models import User
import json

class TestViews(TestCase):


    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")

        # Create 13 authors for pagination tests
        number_of_stocks= 13

        for id in range(number_of_stocks):
            Security.objects.create(
                id=id,
                name=f'Security {id}',
                ticker=f'XY{id}',
                last_price= 1.1 * id)

        user = User.objects.create(
            id=123,
            username="user123",
            email="test@dev.null",
            first_name="userFirst",
            last_name="userLast"
        )

        pass

    def setUp(self):
        print("setUp: Run once for every test method to set up clean data.")
        pass

    def test_security_search(self):
        response = self.client.get('/security/?q=Security')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 13)

    def test_user_security(self):

        # verify it does not exist
        response = self.client.get('/user/security/', headers={ 'x-user-id': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

        # add security
        request_data = { "id": 2, }
        response = self.client.post('/user/security/', data=request_data,
                                    headers={ 'x-user-id': '123'})
        self.assertEqual(response.status_code, 200)

        # verify it was added
        response = self.client.get('/user/security/', headers={ 'x-user-id': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)


