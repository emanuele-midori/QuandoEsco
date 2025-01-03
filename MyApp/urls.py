from django.urls import path, include

from MyApp import views

urlpatterns = [
    path('login/', views.sign_in, name='login'),
    path('registrazione/', views.registrazione, name='registrazione'),
    path('logout/', views.sign_out, name='logout'),
    path('', views.homepage, name='homepage'),
    path('calcolauscita/', views.calcola_uscita, name='calcola_uscita'),
    path('salvagiornata/', views.salva_giornata, name='salva_giornata'),
]