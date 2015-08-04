from django.shortcuts import render
from django.views.generic import TemplateView, View, FormView
from django.core.urlresolvers import reverse
from forms import LoginForm
from forms import SignUpForm
from forms import UserEditForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render_to_response
from api import UserInstanceResource
from decorators import access_required_super,access_required_user,access_required_account
from django.contrib.auth.tokens import default_token_generator
from access.models import UserProfile
import datetime
from django.db.models import Count
import json


class LoginView(FormView):
    '''Base class for Login'''

    template_name = 'access/login.html'
    form_class = LoginForm
    
    def get(self, request, *args, **kwargs):
        '''
        returns Login Page with Login Form for unauthenicated user
        where as  authenticated user are returned to dashboard
         '''
        if request.user.is_authenticated():
            if  request.user.userprofile.user_type=="S":
                return  HttpResponseRedirect(reverse('super_home'))
            else:
                return HttpResponseRedirect(reverse('audit'))
        # if request.user.is_authenticated():
        #     return HttpResponseRedirect('/graphs/')

        context = {'form':self.form_class()}
        return self.render_to_response(context)

    
    def post(self, request, *args, **kwargs):
        '''
        authentication is done here after givings username and password
        if user is authenticated returned to dashboard page
        where as unauthenticated user or invalid email
        or passwords are turned back to login page with
        validation errors or invalid user
        '''
        data = request.POST.copy()
        form = self.form_class(data)
        context = {}
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email,password=password)

            if user is not None:
                login(request,user)
                if user.is_active:
                    login(request, user)
                  
                    next = request.GET.get('next', None)
                    if next:
                        return HttpResponseRedirect(next)
                    if request.user.userprofile.user_type=="S":
                        return  HttpResponseRedirect(reverse('super_home'))
                    if request.user.userprofile.user_type=="A":
                        return HttpResponseRedirect(reverse('audit'))
                    else:
                        return HttpResponseRedirect(reverse('audit'))
                    
                else:
                  # Return a 'disabled account' error message
                    return HttpResponse("You're account is disabled.")
            else:
              # Return an 'invalid login' error message.
                context['form'] = form
                return self.render_to_response(context)
        else:  
            context['form']= form
            return self.render_to_response(context)

'''Signup view'''
class SignupView(FormView):
    ''' Class View for signup page'''

    form_class = SignUpForm
    template_name = 'access/signup.html'

    def get(self, request, *args, **kwargs):

        form = self.form_class()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):

        data = request.POST
        form = self.form_class(data)
        if form.is_valid():
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['user_type']
            UserInstanceResource()._post(email=email,password = password,user_type=user_type,first_name=first_name,last_name=last_name)
            return HttpResponseRedirect(reverse('account_login'))
        return self.render_to_response({'form': form})



'''Logout view'''
class LogoutView(View):
    '''base class for logout'''

    def get(self, *args, **kwargs):

        '''authenticated users are returned back to Login page'''

        if self.request.user.is_authenticated():
            logout(self.request)
        return HttpResponseRedirect(reverse('account_login'))







class UserEditView(FormView):
    '''User Edit-profile view'''

    form_class = UserEditForm
    template_name = 'access/user_edit.html'

    def get(self, request, *args, **kwargs):

        id=request.user.id
        user_data = UserInstanceResource()._get(id=id)
        if user_data:
            initial_data = {'firstname':user_data.first_name,
                            'lastname':user_data.last_name,
                            'email':user_data.email
                            }
        form = self.form_class(initial=initial_data)
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):

        id=request.user.id
        data = request.POST
        form = self.form_class(data)
        if form.is_valid():
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            UserInstanceResource()._update(id=id,first_name=first_name,last_name=last_name)
            return HttpResponseRedirect('/graphs/')
        return self.render_to_response({'form': form})




class SuperView(TemplateView,View):
    '''super admins dashboard page is returned'''
    
    template_name = 'access/superadmin_dashboard.html'

    @access_required_super()
    def get(self, request, *args, **kwargs):
        '''only superadmin can access this page by using decorator'''
        

        if self.request.user.is_authenticated():
            users=UserProfile.objects.all()
            entries=UserProfile.objects.extra({'published':"date(created_on)"}).values('published').annotate(count=Count('id'))
            
            entry_list=[]
            for entry in entries:
                entry['published']=entry.get('published').strftime("%Y-%m-%d")
                entry_list.append(entry)
                
            perday_count=[]
            pub_date=[]
            for new_entry in entries:
                pub_date.append(new_entry["published"])
                perday_count.append(new_entry["count"])  
            return self.render_to_response({'users': users,'perday_count':perday_count,'pub_date':json.dumps(pub_date),'entry_list':json.dumps(entry_list)})
        return HttpResponseRedirect(reverse('audit'))




'''user-delete view'''

class UserDeleteView(TemplateView,View):
    '''User is deleted by super admin'''
    template_name = 'access/user_delete.html'

    def delete_user(self,user_id):
        user =User.objects.get(pk=user_id)
        user.delete()

    @access_required_super()
    def get(self, request, *args, **kwargs):
        '''
        :param request:user id
        :param args:
        :param kwargs: users id
        :return: delete option pops up
        '''
        context = {}
        context['user_id']  = kwargs.get('user_id','')
        return self.render_to_response(context)

    def post(self,request, *args, **kwargs):
        '''
        :param request:
        :param args:
        :param kwargs:user_id
        :return:user is deleted and is back returned to home page

        '''
    
        data = request.POST.copy()
        self.delete_user(data.get('user_id',''))

        messages.success(request, 'User Deleted Successfully.',
                         extra_tags='alert-success')
        return HttpResponseRedirect("/access/super")

'''charts view'''
class ChartView(TemplateView,View):
    
    template_name = 'access/charts.html'

    def get(self, request, *args, **kwargs):
        users=UserProfile.objects.all()
        entries=UserProfile.objects.extra({'published':"date(created_on)"}).values('published').annotate(count=Count('id'))
        
        entry_list=[]
        for i in entries:
            i['published']=i.get('published').strftime("%Y-%m-%d")
            entry_list.append(i)

        perday_count=[]
        pub_date=[]
        for i in entries:
            pub_date.append(i["published"])
            perday_count.append(i["count"])  

        
        return self.render_to_response({'users': users,'perday_count':perday_count,'pub_date':json.dumps(pub_date),'entry_list':json.dumps(entry_list)})

    def post(self,request, *args, **kwargs):

        entries=UserProfile.objects.extra({'published':"date(created_on)"}).values('published').annotate(count=Count('id'))
        monthly=UserProfile.objects.extra({'published':"month(created_on)"}).values('published').annotate(count=Count('id'))
        entry_list=[]
        for i in entries:
            i['published']=i.get('published').strftime("%Y-%m-%d")
            entry_list.append(i)

        perday_count=[]
        pub_date=[]
        for i in entries:
            pub_date.append(i["published"])
            perday_count.append(i["count"])  
        return self.render_to_response({'users': users,'perday_count':perday_count,'pub_date':json.dumps(pub_date),'entry_list':json.dumps(entry_list)})
   
        
