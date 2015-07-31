from django.conf.urls import url,patterns
import views
from graphs.views import Audit

urlpatterns = patterns('',
	url(r'^$',Audit.as_view(), name='audit'),
	)