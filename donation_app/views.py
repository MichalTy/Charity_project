from django.shortcuts import render


def LandingPage(request):
    return render(request, 'index.html')


def AddDonation(request):
    return render(request, 'form.html')


def Login(request):
    return render(request, 'login.html')


def Register(request):
    return render(request, 'register.html')
