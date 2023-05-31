from django.urls import path
from . import views

urlpatterns=[
    path('', views.inicio, name='inicio'),

    #Para el CRUD
    path('estudiantes/crear', views.crear, name='crear'),
    path('estudiantes/editar', views.editar, name='editar'),
    path('eliminar/<int:id>', views.eliminar, name='eliminar'),
    path('estudiantes/editar/<int:id>', views.editar, name='editar'),

    #Para el login
    path('signup/',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('home/',views.HomePage,name='home'),
    path('logout/',views.LogoutPage,name='logout'),

    #path('estudiantes', views.estudiantes, name='estudiantes'),
]