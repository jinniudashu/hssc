from django.shortcuts import render
from django.http import HttpResponse

def htmx_test(request):
    print('From htmx_test:', request)
    return HttpResponse('From: htmx_test')
