from django.contrib import messages
from django.shortcuts import redirect

def userIsAdmin(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, "No tiene permiso!", extra_tags='error-message')
            return redirect('inicio')
    return wrap