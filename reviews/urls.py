from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('serie/<int:serie_id>/', views.detalle_serie, name='detalle_serie'),
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
