def user_is_not_logged_in(function):
    from django.shortcuts import redirect
    def wrap(request, *args, **kwargs):
        if request.user.is_anonymous:
            return function(request, *args, **kwargs)
        return redirect('/')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def is_user_profile(function):
    from django.shortcuts import redirect
    from utils import profileCompleted
    def wrap(request, *args, **kwargs):
        if request.user.userprofile.id == kwargs['profileId'] or request.user.companyprofile.id == kwargs['profileId']:
            return function(request, *args, **kwargs)
        return redirect("/")
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_profile_completed(function):
    from django.shortcuts import redirect
    from utils import profileCompleted
    def wrap(request, *args, **kwargs):
        if profileCompleted(request):
            return function(request, *args, **kwargs)
        return redirect("/profileEdit/" + str(request.user.id))
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
