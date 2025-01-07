from django.urls import path, include

from MyApp import views

urlpatterns = [
    path('login/', views.sign_in, name='login'),
    path('registrazione/', views.registrazione, name='registrazione'),
    path('logout/', views.sign_out, name='logout'),
    path('', views.homepage, name='homepage'),
    path('calcolauscita/', views.calcola_uscita, name='calcola_uscita'),
    path('salvagiornata/', views.salva_giornata, name='salva_giornata'),
    path('registro/', views.registro, name='registro'),
    path('modificagiornata/<int:id>/', views.modifica_giornata, name='modifica_giornata'),
    path('eliminagiornata/<int:id>/', views.elimina_giornata, name='elimina_giornata'),

]