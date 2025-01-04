from django.shortcuts import render

def Home(request):
    return render(request, 'app/index.html')

def About(request):
    return render(request, 'app/about.html')
