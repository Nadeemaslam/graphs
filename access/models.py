from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import user_logged_in
from django.conf import settings

ACCOUNT_ADMIN = 'A'
SUPER_ADMIN = 'S'
TECH_ADMIN = 'T'
CUSTOMER = 'C'

USER_ROLE = (
    (SUPER_ADMIN, 'SUPER_ADMIN'),
    (ACCOUNT_ADMIN, 'ACCOUNT_ADMIN'),
    (TECH_ADMIN, 'TECH_ADMIN'),
    (CUSTOMER, 'CUSTOMER'),
)


class UserProfile(models.Model):
    user_type = models.CharField(max_length=1, choices=USER_ROLE,
                                 default=CUSTOMER)
    user = models.OneToOneField(User, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    def __unicode__(self):
		return self.user_type




