from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from controllers import indexController, loginController, registerController
from home.decorators import user_is_not_logged_in

@user_is_not_logged_in
def login(req):
    if req.method == 'POST':
        context = loginController(req)
        if context['status']:
            return redirect('/')
        return redirect('/login/')
    return render(req, 'home/login.html')

@user_is_not_logged_in
def register(req):
    if req.method == 'POST':
        return registerController(req)
    return render(req, 'home/register.html')

@login_required
def index(req):
    context = indexController(req)
    return render(req, 'home/index.html', context)