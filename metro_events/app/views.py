# Date Started: March 20, 2021
# Author/s: Wylen Joan Lee

# References:
#    https://www.youtube.com/watch?v=dBctY3-Z5hY&ab_channel=PrettyPrinted

from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import UserRegistrationForm
from django.http import HttpResponse
from django.contrib.auth.models import Group, User, auth


class UserLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('app:user-dashboard')
        else:
            return render(request, 'login.html')
    
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
        username = str(first_name) + '.' + str(last_name)
        password = request.POST.get('password')
       
        user = User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            regular_user = form.save(commit=False)
            regular_user.user_id = user
            regular_user.save()
            return redirect('app_user:login_view')
        else:
            return HttpResponse(form.errors)

class UserDashboardView(View):
    def get(self, request):
        return render(request, 'user/user-dashboard.html')

    
