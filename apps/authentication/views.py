from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm


#### Loggers ####
import logging
logger=logging.getLogger('dashboardLogs')


#### Error Code ####
from ..inneye.APIStatus import *


#### Login Section Start ####
def login_view(request):
    
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":
        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:

                logger.debug(authenticationSuccess.get('message')+username)
                login(request, user)
                return redirect("/")

            else:

                logger.debug(authenticationError.get('message')+username)
                msg = 'Invalid credentials'

        else:

            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})
#### Login Section End ####

#### Logout Section Start ####
def logout_view(request):

    logger.debug(authenticationLogout.get('message')+str(request.user))
    logout(request)
    return redirect(login_view)
#### Login Section End ####




