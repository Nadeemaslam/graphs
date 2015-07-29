from django.conf.urls import url,patterns
import views
from graphs.views import Audit

urlpatterns = patterns('',
	# url(r'^$', views.index, name='index'),
	url(r'^$',Audit.as_view(), name='audit'),
	# url(r'^$', views.pie, name='pie'),

	)