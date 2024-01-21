from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name= 'home'),
   path('download-timetable/', views.download_timetable, name='download_timetable'),
]
