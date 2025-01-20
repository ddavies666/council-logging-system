from django.shortcuts import render

from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1>Welcome to My Django Web App!</h1>")
    return render(request, 'templates/myapp/home.html')
