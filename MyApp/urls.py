from django.urls import path, include

from MyApp import views

urlpatterns = [
    path('registrazione/', views.registrazione, name='registrazione'),
    path('', views.sign_in, name='login'),
    path('calcolauscita',views.calcolauscita, name='calcolauscita' ),
]