from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import user_logged_in
from django.conf import settings

ACCOUNT_ADMIN = 'A'
SUPER_ADMIN = 'S'
CUSTOMER = 'C'

USER_ROLE = (
    (SUPER_ADMIN, 'Super Admin'),
    (ACCOUNT_ADMIN, 'Account Admin'),
    (CUSTOMER, 'Customer'),
)


class UserProfile(models.Model):
    '''user Profile model'''
    
    user_type = models.CharField(max_length=1, choices=USER_ROLE,
                                 default=CUSTOMER)
    user = models.OneToOneField(User, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    def __unicode__(self):
		return self.user_type




