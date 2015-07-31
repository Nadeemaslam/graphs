__author__ = 'Nadeem' 

from django.conf import settings
from django.contrib.auth.models import User
import re
from models import UserProfile


class UserProfileListResource:
    """ Operations related to SuperAdminProfile """

    def _post(self, user_obj, user_type=None):
        """ Create a  userprofile """
        user_profile = UserProfile()
        if user_type:
            user_profile.user_type = user_type
        user_profile.user = user_obj
        user_profile.save()
        return user_profile


class UserInstanceResource:
    def _get(self, id=None, email=None):
        if email:
            return User.objects.get(username=email)
        return User.objects.get(pk=id)

    def _post(self, email, first_name=None, last_name=None, password=None,
              user_type=None):
        user = User(username=email,email=email)
        # user.email = email
        # user.username = email
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if password:
            user.set_password(password)
        user.save()
        if user:
            UserProfileListResource()._post(user_obj=user, user_type=user_type)
        return user


    def _update(self, id, password=None, first_name=None, last_name=None,
                email=None):
        user = User.objects.get(id=id)
        if password:
            user.set_password(password)
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.username = email
            user.email = email
        user.save()
        return user

    def _filter(self,email=None,user_type=None):
        # filter by
        if email:
            return User.objects.filter(username=email)
        return User.objects.all() 
        




