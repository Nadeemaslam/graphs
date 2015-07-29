from django.conf.urls import url,patterns 
import views
from access.views import LoginView
from access.views import SignupView
from access.views import LogoutView
from access.views import UserEditView,SuperView
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
	url(r'signup/$', SignupView.as_view(), name='account_signup'),
	url(r'edit/$', UserEditView.as_view(), name='user_edit'),
	url(r'^super$',
        login_required(SuperView.as_view()),
        name='super_home'),
	url(r'logout/$', LogoutView.as_view(), name="account_logout"),
	url(r'login/$',LoginView.as_view(),name='account_login'),
	)

