from django.shortcuts import render

def interactions_home(request):
    return render(request, 'interactions/home.html')
