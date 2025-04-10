from django.urls import path
from . import views

app_name = 'theater_cms'  # Change this from 'cms' to 'theater_cms'

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.events, name='events'),
    path('about/', views.about, name='about'),
    path('today/', views.today, name='today'),
    path('qa/', views.qa, name='qa'),
    path('sponsors/', views.sponsors, name='sponsors'),
]