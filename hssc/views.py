from django.shortcuts import render, redirect

def index(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/clinic/')
        else:
            return redirect('/core/index_customer/')
    else:
        return redirect('/accounts/login/')
