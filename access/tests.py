import unittest
from django.test import TestCase

from access.api import UserInstanceResource
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from access.views import LoginView
from django.contrib.auth.models import User
from django.test.utils import setup_test_environment
setup_test_environment()


class TestData(TestCase):
	'''base class for testing'''
	
	# def setUp(self):
	# 	client = Client()

	def test_views(self):
		'''test to check working of views'''

		response = self.client.get("/access/login/")
		self.assertEqual(response.status_code, 200)

	def test_signup(self):
		'''Unit test to check signup view'''


		UserInstanceResource()._post(email='nadeem@gmail.com',password = '123',user_type='C',first_name='sahil',last_name='khan')
		result=UserInstanceResource()._get(email='nadeem@gmail.com')
		
		self.assertEqual(result.first_name,'sahil')

	def test_update(self):

		UserInstanceResource()._post(email='nadeem@gmail.com',password = '123',first_name='sahil',last_name='khan')
		result=UserInstanceResource()._get(email='nadeem@gmail.com')
		UserInstanceResource()._update(id=result.id,first_name='farhan',last_name='khan')
		s=UserInstanceResource()._get(email='nadeem@gmail.com')
		self.assertEqual(s.first_name,'farhan')




	
 	
 		
	def test_login(self):
		'''unit test to check login form'''
		
		c = Client()
		UserInstanceResource()._post(email='nad@gmail.com',password = '123',user_type='C',first_name='sahil',last_name='khan')	 	
		response=c.post('/access/login/', {'email':'nad@gmail.com','password' : '123'})
	 	self.assertEqual(response.status_code, 302)  # Redirect on form success

	 	response = self.client.post("/access/login/", {})
	 	self.assertEqual(response.status_code, 200) # we get our page back with an error


	








if __name__ == '__main__':
    unittest.main()