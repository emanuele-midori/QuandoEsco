from django.urls import path, include

from MyApp import views

urlpatterns = [
    path('',views.homepage, name='homepage' ),
]