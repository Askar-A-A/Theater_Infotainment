from django.shortcuts import render

# Home page view
def home(request):
    return render(request, 'home.html')

# Events listing page view
def events(request):
    return render(request, 'events.html')

# About page view
def about(request):
    return render(request, 'about.html')

# Today's performance page view
def today(request):
    return render(request, 'today.html')

# Q&A/FAQ page view
def qa(request):
    return render(request, 'q&a.html')

# Sponsors page view
def sponsors(request):
    return render(request, 'sponsors.html')
