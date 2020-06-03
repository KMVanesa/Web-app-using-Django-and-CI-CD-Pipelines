from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# from first_app.models import Register
from . import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash


def index(request):
    # user = request.user
    # if user:
    #     print('abc')
    #     # my_data = {'user': user.first_name}
    # # users = Register.objects.order_by('first_name')

    return render(request, 'books/books.html', {})


@login_required
def user_logout(request):
    logout(request)
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
            reg_form.save()
            username = reg_form.cleaned_data.get('username')
            raw_password = reg_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            registered = True
            return HttpResponseRedirect(reverse('books'))

        else:
            print(reg_form.errors)
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
            login(request, user)
            return HttpResponseRedirect(reverse('books'))
        else:
            form = AuthenticationForm(request.POST)
            messages.info(request, "Invalid Credentials.")
            return render(request, 'first_app/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'first_app/login.html', {'form': form})


def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            update_form = forms.UserUpdateForm(request.POST, instance=request.user)
            if update_form.is_valid():
                update_form.save()
                messages.success(request, "Account has been updated")
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
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, "Your Password has been updated!")
                return HttpResponseRedirect(reverse('logout'))
            else:
                messages.info(request, "Passwords Don't Match.")
                return render(request, 'first_app/password.html', {'form': form})
        else:
            form = PasswordChangeForm(user=request.user)
            return render(request, 'first_app/password.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse('login'))
