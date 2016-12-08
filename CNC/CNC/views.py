from django.http import *
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(main)
    return render_to_response('login.html', (request))

@login_required(login_url='/login/') # moet even kijken hoe ik dit fix krijg nu dat de pagina nie gevonde kan worde
def main(request):
	return render_to_response('main.html', (request))
