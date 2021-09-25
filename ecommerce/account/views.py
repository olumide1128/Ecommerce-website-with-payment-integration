from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from store.models import *

# Create your views here.

def login_view(request):

    error_msg = ""

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if(username != "" and password != ""):
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user) #login
                print("Details correct..")
                print(request.user, "is logged in!")
                return redirect("/")
            else:
                error_msg = "Incorrect Username and Password!!"
        else:
            error_msg = "Enter username and password!!"



    context = {"error":error_msg}
    
    return render(request, 'account/login.html', context)


def register_view(request):
    error_msg = ""

    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        if(fullname != "" and email != "" and username != "" and password != ""):
            user = User.objects.create_user(username, email, password, is_staff=False, is_superuser=False)
            user.save()

            customer = Customer.objects.create(user=user, name=fullname, email=email)
            customer.save()

            login(request, user) #login user

            print("User account created and user logged in as ", request.user)

            return redirect("/")


        else:
            error_msg = "Must fill all fields!!"

    
    context = {"error":error_msg}

    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect("/")
