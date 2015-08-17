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


class TestData(unittest.TestCase):
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

	# def test_call_view_loads(self):
 #    	self.client.login(username='sa@sa.com', password='123')
 #    	response = self.client.get('/super_home')
 #    	self.assertEqual(response.status_code, 200)
 #    	self.assertTemplateUsed(response, 'superadmin_dashboard.html')

	
 	def tearDown(self):
 		self.test_user.delete()
 		
	def test_login(self):
	 	self.client = Client()
	 	# self.first_name = 'agconti'
	 	self.email = 'sa@sa.com'
	 	self.password = '123'
	 	# self.test_user = User.objects.create_user(self.email, self.password)
	 	login = self.client.login(email=self.email, password=self.password)
	 	self.assertEqual(login, False)


	# def setUp(self):
	# 	self.factory = RequestFactory()

	# def test_list_view(self):
	# 	request = self.factory.get(reverse('super_home'))
 #        # additional params can go after request
 #        response = LoginView.as_view()(request)
 #        self.assertEqual(response.status_code, 200)





if __name__ == '__main__':
    unittest.main()