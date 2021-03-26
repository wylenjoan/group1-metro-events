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
        events = Event.objects.filter(status='approved', is_deleted=False).exclude(participants=regular_user)
        joined_events = Event.objects.filter(participants=regular_user)

        context = {
            'events': events,
            'regular_user': regular_user,
            'joined_events': joined_events
        }
        return render(request, 'user.html', context)

    def post(self, request):
        user = request.user
        regular_user = RegularUser.objects.get(user_id=user)
        if request.method == 'POST':
            # Join Event
            if 'btnJoinEvent' in request.POST:
                event_id = request.POST.get('event_id')
                event = Event.objects.get(id=event_id)
                request_ = Request.objects.create(request_type = 'join_event', user_id = regular_user, event_id=event, status='pending')
                return redirect('app:user-dashboard')

            # Apply as Organizer
            elif 'btnApplyOrganizer' in request.POST:
                request_ = Request.objects.create(request_type = 'upgrade', user_id = regular_user, user_type = 'organizer', status='pending')
                return redirect('app:user-dashboard')

            # Apply as Administrator
            elif 'btnApplyAdmin' in request.POST:
                request_ = Request.objects.create(request_type = 'upgrade', user_id = regular_user, user_type = 'admin', status='pending')
                return redirect('app:user-dashboard')

            else:
                print('else')


class OrganizerDashboardView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'login.html')    
        user = request.user
        regular_user = RegularUser.objects.get(user_id=user)
        organizer_user = OrganizerUser.objects.get(regular_user_id=regular_user)

        events = Event.objects.filter(is_deleted=False, organizer_id = organizer_user)
        join_requests = Request.objects.filter(status='pending', request_type='join_event')

        context = {
            'regular_user': regular_user,
            'organizer_user': organizer_user,
            'events': events,
            'join_requests': join_requests
        }
        return render(request, 'organizer.html', context)

    def post(self, request):
        user = request.user
        regular_user = RegularUser.objects.get(user_id=user)
        organizer_user = OrganizerUser.objects.get(regular_user_id=regular_user)

        if request.method == 'POST':
            if 'btnUpdateEvent' in request.POST:
                event_id = request.POST.get('event_id')
                event = Event.objects.get(id = event_id)

                event.title = request.POST.get('update_event_title')
                event.description = request.POST.get('update_event_description')
                event.event_type = request.POST.get('update_event_eventType')
                event.street = request.POST.get('update_event_street')
                event.city = request.POST.get('update_event_city')
                event.province = request.POST.get('update_event_province')
                event.save()

                return redirect('app:organizer-dashboard')

            elif 'btnDeleteEvent' in request.POST:
                event_id = request.POST.get('event_id')
                event = Event.objects.get(id = event_id)
                event.is_deleted = True
                event.save()
                return redirect('app:organizer-dashboard')
            
            elif 'btnCreateEvent' in request.POST:
                title = request.POST.get('create_event_title')
                description = request.POST.get('create_event_description')
                event_type = request.POST.get('create_event_eventType')
                status = 'pending'
                street = request.POST.get('create_event_street')
                city = request.POST.get('create_event_city')
                province = request.POST.get('create_event_province')
                organizer_id = organizer_user

                event = Event.objects.create(title=title, description=description, event_type=event_type, status=status, street=street, city=city, province=province, organizer_id=organizer_id)

                request_ = Request.objects.create(request_type='create_event', event_id=event, status='pending', user_id=regular_user)

                return redirect('app:organizer-dashboard')
            
            elif 'btnAcceptRequest' in request.POST:
                join_request_id = request.POST.get('join_request_id')
                join_request = Request.objects.get(id=join_request_id)
                join_request.status = 'approved'
                join_request.save()

                print(join_request.user_id)

                event = join_request.event_id
                print(event)

                event.participants.add(join_request.user_id)
                event.save()

                return redirect('app:organizer-dashboard')

            elif 'btnDeclineRequest' in request.POST:
                join_request_id = request.POST.get('join_request_id')
                join_request = Request.objects.get(id=join_request_id)
                join_request.status = 'declined'
                join_request.save()

                return redirect('app:organizer-dashboard')


            
class AdminDashboardView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'login.html')
        user = request.user
        regular_user = RegularUser.objects.get(user_id=user)
        admin_user = AdministratorUser.objects.get(regular_user_id=regular_user)

        events = Event.objects.filter(is_deleted=False)
        event_requests = Request.objects.filter(status='pending', request_type='create_event')
        upgrade_requests = Request.objects.filter(status='pending', request_type='upgrade')
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

    def post(self, request):
        user = request.user
        regular_user = RegularUser.objects.get(user_id=user)

        if request.method == 'POST':
            # Accept Upgrade Requests (btnAcceptUpgrade)
            if 'btnAcceptUpgrade' in request.POST:
                upgrade_request_id = request.POST.get('upgrade_request_id')
                upgrade_request = Request.objects.get(id=upgrade_request_id)
                upgrade_request.status = 'approved'
                upgrade_request.save()

                if upgrade_request.user_type == 'organizer':
                    request_user = upgrade_request.user_id
                    request_user.is_organizer = True
                    request_user.save()
                    organizer = OrganizerUser.objects.create(regular_user_id = request_user)
                
                else:
                    request_user = upgrade_request.user_id
                    request_user.is_admin = True
                    request_user.save()
                    admin = AdministratorUser.objects.create(regular_user_id = request_user)
                
                return redirect('app:admin-dashboard')
            
            # Decline Upgrade Requests (btnAcceptUpgrade)
            elif 'btnDeclineUpgrade' in request.POST:
                upgrade_request_id = request.POST.get('upgrade_request_id')
                upgrade_request = Request.objects.get(id=upgrade_request_id)
                upgrade_request.status = 'declined'
                upgrade_request.save()
                return redirect('app:admin-dashboard')
            
            # Accept Create Event Requests (btnAcceptCreateEvent)
            elif 'btnAcceptCreateEvent' in request.POST:
                event_request_id = request.POST.get('event_request_id')
                event_request = Request.objects.get(id=event_request_id)
                event_request.status = 'approved'
                event_request.save()

                event = event_request.event_id
                event.status = 'approved'
                event.save()

                return redirect('app:admin-dashboard')

            # Decline Create Event Requests (btnAcceptCreateEvent)
            elif 'btnDeclineCreateEvent' in request.POST:
                event_request_id = request.POST.get('event_request_id')
                event_request = Request.objects.get(id=event_request_id)
                event_request.status = 'declined'
                event_request.save()

                event = event_request.event_id
                event.status = 'declined'
                event.save()

                return redirect('app:admin-dashboard')

            # Remove User
            elif 'btnRemoveUser' in request.POST:
                list_user_id = request.POST.get('list_user_id')
                list_user = RegularUser.objects.get(id=list_user_id)
                list_user.is_deleted = True
                list_user.save()

                return redirect('app:admin-dashboard')

            # Remove Event
            elif 'btnRemoveEvent' in request.POST:
                list_event_id = request.POST.get('list_event_id')
                list_event = Event.objects.get(id=list_event_id)
                list_event.is_deleted = True
                list_event.save()

                return redirect('app:admin-dashboard')
            
            else:
                print('else')