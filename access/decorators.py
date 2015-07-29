from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect,Http404
from functools import wraps

def access_required_super():
    '''checks if role is super admin
    then returns the access to which this decorator is applied
    else raises 404'''
    def dec(func):
        def _wrapper(self, request,*args, **kwargs):
            if request.user.userprofile.user_type=="S":
                return func(self,request, *args, **kwargs)
            else:
                raise Http404
        return wraps(func)(_wrapper)
    return dec

def access_required_account():
    '''checks if role is account admin
    then returns the access to which this decorator is applied
    else raises 404'''
    def dec(func):
        def _wrapper(self, request,*args, **kwargs):
            if request.user.userprofile.user_type=="A":
                return func(self,request, *args, **kwargs)
            else:
                raise Http404
        return wraps(func)(_wrapper)
    return dec

def access_required_user():
    '''checks if role is user
    then returns the access to which this decorator is applied
    else raises 404'''
    def dec(func):
        def _wrapper(self, request,*args, **kwargs):
            if request.user.userprofile.user_type=="C":
                return func(self,request, *args, **kwargs)
            else:
                raise Http404
        return wraps(func)(_wrapper)
    return dec