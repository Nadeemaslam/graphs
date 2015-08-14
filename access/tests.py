from django.test import TestCase

from access.api import UserInstanceResource
from django.test.client import Client
from django.test.utils import setup_test_environment
setup_test_environment()


class TestData(TestCase):
	'''base class for testing'''
	
	def setUp(self):
		pass

	def test_signup(self):


		UserInstanceResource()._post(email='nadeem@gmail.com',password = '123',user_type='C',first_name='sahil',last_name='khan')
		result=UserInstanceResource()._get(email='nadeem@gmail.com')
		
		self.assertEqual(result.first_name,'sahil')

	def test_update(self):

		UserInstanceResource()._post(email='nadeem@gmail.com',password = '123',user_type='C',first_name='sahil',last_name='khan')
		result=UserInstanceResource()._get(email='nadeem@gmail.com')
		UserInstanceResource()._update(id=result.id,first_name='farhan',last_name='khan')
		s=UserInstanceResource()._get(email='nadeem@gmail.com')
		self.assertEqual(s.first_name,'farhan')

	

	



if __name__ == '__main__':
    unittest.main()