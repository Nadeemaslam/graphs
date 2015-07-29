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
        returns Index Page with Login Form for unauthenicated user
        where as  authenticated user are returned to maps
         '''
        if request.user.is_authenticated():
            if  request.user.userprofile.user_type=="S":
                print "hiiiiiiiii"
                return  HttpResponseRedirect('/access/super')
            else:
                return  HttpResponseRedirect('/graphs/')
        # if request.user.is_authenticated():
        #     return HttpResponseRedirect('/graphs/')

        context = {'form':self.form_class()}
        return self.render_to_response(context)

    
    def post(self, request, *args, **kwargs):
        '''
        authentication is done here after givings username and password
        if user is authenticated returned to maps page
        where as unauthenticated user or invalid email
        or passwords are turned back to index page with
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
                    print "kakaka"
                    login(request, user)
                  # Redirect to index page.
                    next = request.GET.get('next', None)
                    if next:
                        return HttpResponseRedirect(next)
                    if request.user.userprofile.user_type=="S":
                        print "hiiiiiiiii"
                        return  HttpResponseRedirect('/access/super')
                    else:
                        print "jajajaja"
                        return  HttpResponseRedirect('/graphs/')
                    
                else:
                  # Return a 'disabled account' error message
                    return HttpResponse("You're account is disabled.")
            else:
                print "lalala"
              # Return an 'invalid login' error message.
                context['form'] = form
                return self.render_to_response(context)
        else:  
            context['form']= form
            return self.render_to_response(context)


class SignupView(FormView):
    
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
            return HttpResponseRedirect('/graphs/')
        return self.render_to_response({'form': form})




class LogoutView(View):
    '''base class for logout'''

    def get(self, *args, **kwargs):
        '''authenticated users are returned back to index page'''
        if self.request.user.is_authenticated():
            logout(self.request)
        return HttpResponseRedirect(reverse('audit'))

class UserEditView(FormView):
    form_class = UserEditForm
    template_name = 'access/user_edit.html'

    def get(self, request, *args, **kwargs):
        u = User.objects.get(pk=1)
        if u:
            initial_data = {'firstname':u.first_name,
                            'lastname':u.last_name,
                            'email':u.email
                            }
            form = self.form_class(initial=initial_data)
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        
        data = request.POST
        form = self.form_class(data)
        u = User.objects.get(pk=1)
        print u
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name=request.POST['first_name']
            print first_name
            last_name=request.POST['last_name']
            print last_name
            UserInstanceResource()._update(email=email,id=1,first_name=first_name,last_name=last_name)
            return HttpResponseRedirect('/graphs/')
        return self.render_to_response({'form': form})

class SuperView(TemplateView,View):
    '''super admins home page is returned'''
    # form_class=UploadForm
    template_name = 'access/superadmin_dashboard.html'

    @access_required_super()
    def get(self, request, *args, **kwargs):
        '''only superadmin can access this page by using decorator'''
        # context = {}
        # if request.session.get('message',''):
        #     context['message'] = request.session['message']

        # context['user_properties'] = Properties.objects.all()
        # context['form']=self.form_class()
        # return self.render_to_response(context)
        print"hi nad"
        msg=[]
        if self.request.user.is_authenticated():
            print 'lala'
            users=UserProfile.objects.all()
            # first_date = datetime.date(2015,07,22)
            # last_date = datetime.date(2015,07,28)
            # query_set=UserProfile.objects.filter(created_on__range=(first_date, last_date)).count()
            # gg=UserProfile.objects.filter(created_on__gte=datetime.date.today()).count()
            # # print query_set,gg
            # for i in range(1, 8):
            #     n=UserProfile.objects.filter(created_on__week_day=i).count()

            # date_from = datetime.datetime.now() - datetime.timedelta(days=30)
            # created_documents = UserProfile.objects.filter(
            #             created_on__gte=date_from).count()
            entries=UserProfile.objects.extra({'published':"date(created_on)"}).values('published').annotate(count=Count('id'))
            print entries
            monthly=UserProfile.objects.extra({'published':"month(created_on)"}).values('published').annotate(count=Count('id'))
            
            
            # dic= dict(monthly)
            # data_1=[]
            # for s in monthly:
            #     for d,v in  s.items():
                
            #         # print d,v 
            #         data_1.append(s.get('count'))
            #     print (s.get("count")),"kk"
            
                    
                

            # dic=dict(data_1)

            
            per_day=[]
            pub_date=[]
            for x in entries:
                print x
                pub_date.append(x["published"].strftime("%Y-%m-%d"))
                per_day.append(x["count"])
            
            print per_day
            print pub_date  

            
            return self.render_to_response({'users': users,'per_day':per_day,'pub_date':json.dumps(pub_date)})
        return HttpResponseRedirect(reverse('audit'))
