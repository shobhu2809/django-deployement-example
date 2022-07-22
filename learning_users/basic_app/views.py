
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from basic_app.forms import UserForm, UserProfileInfoForm


# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def special(request):
    return HttpResponse("You are logged in the app")


def registeration(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']
                
            profile.save()

            registered=True

        else:
            print(user_form.errors,profile_form.errors)
    
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    
    return render(request, 'basic_app/registeration.html',{'user_form':user_form, 'profile_form':profile_form, 'registered':registered})



def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password) #This line will authenticate the user from the database

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            print("Username : {} and password {}".format(username,password))
            return HttpResponse("Invalid login ")

    else:
        return render(request,'basic_app/login.html',{})
            
