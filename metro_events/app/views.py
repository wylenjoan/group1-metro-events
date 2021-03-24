# Date Started: March 20, 2021
# Author/s: Wylen Joan Lee

# References:
#    https://www.youtube.com/watch?v=dBctY3-Z5hY&ab_channel=PrettyPrinted

from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import UserRegistrationForm
from django.http import HttpResponse
from django.contrib.auth.models import Group, User, auth
from .models import RegularUser, OrganizerUser, AdministratorUser, Event, Request

class UserLoginView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'login.html')
        else:
            return redirect('app:user-dashboard')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('app:user-dashboard')
        else:
            return redirect('app:login')

class UserLogoutView(View):
    def get(self,request):
        auth.logout(request)
        return  redirect('app:login')

    def post(self,request):
         auth.logout(request)
         return  redirect('app:login')

class UserRegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        context = {'form' : form}
        return render(request, 'register.html', context)
    
    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        username = str(first_name).lower().replace(' ', '') + '.' + str(last_name).lower().replace(' ', '')
        password = request.POST.get('password')
        is_organizer = False
        is_admin = False
       
        user = User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            regular_user = form.save(commit=False)
            regular_user.user_id = user
            regular_user.save()
            return redirect('app:login')
        else:
            return HttpResponse(form.errors)

class UserDashboardView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'login.html')
        user = request.user
        regular_user = RegularUser.objects.get(user_id=user)
        events = Event.objects.filter(is_approved=True)

        context = {
            'events': events,
            'regular_user': regular_user
        }
        return render(request, 'user.html', context)
        #btnJoinEvent
        #btnApplyOrganizer
        #btnApplyAdmin
        #btnUpdateUser
    def post(self, request):
        user = request.user
        regular_user = RegularUser.objects.get(user_id=user)
        if request.method == 'POST':
            if 'btnJoinEvent' in request.POST:
                event_id = request.POST.get('event_id')
                request = Request.objects.create(request_type = 'join_event', user_id = regular_user, event_id=event_id, is_approved = False,)
                return redirect('app:user-dashboard')

            elif 'btnApplyOrganizer' in request.POST:
                request = Request.objects.create(request_type = 'upgrade', user_id = regular_user, user_type = 'organizer', is_approved = False,)
                
                return redirect('app:user-dashboard')

            elif 'btnApplyAdmin' in request.POST:
                request = Request.objects.create(request_type = 'upgrade', user_id = regular_user, user_type = 'admin', is_approved = False,)
                
                return redirect('app:user-dashboard')

            # elif 'btnUpdateUser' in request.POST:
            #     # first_name = request.POST.get('first_name')
            #     # last_name = request.POST.get('last_name')
            #     # gender = request.POST.get('gender')
            #     # email = request.POST.get('email')
            #     # username = request.POST.get('username')
            #     # password = request.POST.get('password')
            #     form = UserRegistrationForm(request.POST, instance=regular_user)

            #     if form.is_valid():
            #         regular_user = form.save(commit=False)
            #         gender = request.POST.get('gender')
            #         regular_user.save()
            #         return redirect('app:user-dashboard')

            else:
                print('else')


    
class OrganizerDashboardView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'login.html')
        user = request.user
        regular_user = RegularUser.objects.get(user_id=user)
        organizer_user = OrganizerUser.objects.get(regular_user_id=regular_user)

        context = {
            'regular_user': regular_user,
            'organizer_user': organizer_user,
        }

        return render(request, 'organizer.html', context)

class AdminDashboardView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'login.html')
        user = request.user
        regular_user = RegularUser.objects.get(user_id=user)
        admin_user = AdministratorUser.objects.get(regular_user_id=regular_user)

        events = Event.objects.filter(is_deleted=False)
        event_requests = Request.objects.filter(is_approved=False, request_type='create_event')
        upgrade_requests = Request.objects.filter(is_approved=False, request_type='upgrade')
        users = RegularUser.objects.filter(is_deleted=False)

        context = {
            'events': events,
            'regular_user': regular_user,
            'admin_user': admin_user,
            'event_requests': event_requests,
            'upgrade_requests': upgrade_requests,
            'users': users,
        }
        return render(request, 'administrator.html', context)