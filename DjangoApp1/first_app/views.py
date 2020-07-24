from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# from first_app.models import Register
from . import forms
import boto3
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from statsd import StatsClient
from django.contrib.auth import get_user_model
Users = get_user_model()
from django.contrib.auth.models import User
stats = StatsClient()
import logging
import uuid
logger = logging.getLogger(__name__)


# from statsd.defaults.django import statsd

def index(request):
    # user = request.user
    # if user:
    #     print('abc')
    #     # my_data = {'user': user.first_name}
    # # users = Register.objects.order_by('first_name')
    logger.info('User is here')
    return render(request, 'books/books.html', {})


@login_required
def user_logout(request):
    timer = stats.timer('user-logged-out')
    timer.start()
    logger.info('User logged out')
    logout(request)
    timer.stop()
    return HttpResponseRedirect(reverse('login'))


# def form_view(request):
#     form = forms.FormName()
#     if request.method == 'POST':
#         form = forms.FormName(request.POST)
#         if form.is_valid():
#             print('Validated')
#             print("fName: " + form.cleaned_data['first_name'])
#             print("lName: " + form.cleaned_data['last_name'])
#             print("email: " + form.cleaned_data['email'])
#             form.save(commit=True)
#             return index(request)
#         else:
#             print('Error')
#
#     return render(request, 'first_app/form.html', {'form': form})


def register_form(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    registered = False
    reg_form = forms.UserForm()
    if request.method == 'POST':
        reg_form = forms.UserForm(data=request.POST)
        if reg_form.is_valid():
            # user = reg_form.save()
            # user.set_password(user.password)
            # user.save()
            timer = stats.timer('user-registered')
            timer.start()
            reg_form.save()
            username = reg_form.cleaned_data.get('username')
            raw_password = reg_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            logger.info('User Registered in')
            registered = True
            timer.stop()
            return HttpResponseRedirect(reverse('books'))

        else:
            print(reg_form.errors)
            logger.warning(reg_form.errors)
    else:
        reg_form = forms.UserForm()
    return render(request, 'first_app/registration.html', {'registered': registered, 'reg_form': reg_form})


# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = authenticate(username=username, password=password)
#         print(user)
#         print("-------")
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 print('AAAAAAAAA')
#                 return HttpResponseRedirect(reverse('index'))
#             else:
#                 print('BBBBBBBBB')
#                 return HttpResponse("Error")
#         else:
#             print('KKKKKKKKKK')
#             print('id:{} and pass:{}'.format(username, password))
#             return HttpResponse("Invalid Login Details")
#     else:
#         print('Oooooooooooo')
#         return render(request, 'first_app/login.html', {})

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('books'))
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            timer = stats.timer('user-logged-in')
            timer.start()
            login(request, user)
            logger.info('User Logged in')
            timer.stop()
            return HttpResponseRedirect(reverse('books'))
        else:
            form = AuthenticationForm(request.POST)
            messages.info(request, "Invalid Credentials.")
            logger.warning('User entered invalid credentials')
            return render(request, 'first_app/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'first_app/login.html', {'form': form})


def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            update_form = forms.UserUpdateForm(request.POST, instance=request.user)
            if update_form.is_valid():
                timer = stats.timer('user-profile-updated')
                timer.start()
                update_form.save()
                messages.success(request, "Account has been updated")
                timer.stop()
                return HttpResponseRedirect(reverse('update'))
        else:
            update_form = forms.UserUpdateForm(instance=request.user)
        context = {
            'update_form': update_form,
        }
        return render(request, 'first_app/form.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))


def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(data=request.POST, user=request.user)
            if form.is_valid():
                timer = stats.timer('user-change-passwd')
                timer.start()
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, "Your Password has been updated!")
                timer.stop()
                return HttpResponseRedirect(reverse('logout'))
            else:
                messages.info(request, "Passwords Don't Match.")
                return render(request, 'first_app/password.html', {'form': form})
        else:
            form = PasswordChangeForm(user=request.user)
            return render(request, 'first_app/password.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse('login'))


def reset_password(request):
    if request.method == 'POST':
        form = forms.PasswordResetForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            if User.objects.filter(username=username).exists():
                user1= User.objects.filter(username=username)
                token = uuid.uuid1()
                messages.success(request, "Your Password Reset Link in sent!")
                client = boto3.client('sns',region_name='us-east-1')
                msg={"username": username,"token":str(token)}
                response = client.publish(
                    TargetArn='arn:aws:sns:us-east-1:708581696554:user-updates-pwd',
                    Message=json.dumps(msg),
                    MessageAttributes={
                    'username': {
                        'DataType': 'String',
                        'StringValue': username
                    },
                    'token': {
                        'DataType': 'String',
                        'StringValue': str(token)
                    }
                })
            else:
                messages.success(request, "You are not registered as a user!")
                return HttpResponseRedirect(reverse('login'))
            return HttpResponseRedirect(reverse('login'))
    else:
        form = forms.PasswordResetForm()
        return render(request, 'first_app/reset_password.html', {'form': form})

