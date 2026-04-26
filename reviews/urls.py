from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('serie/<int:serie_id>/', views.detalle_serie, name='detalle_serie'),
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('buscar/', views.buscar_serie_view, name='buscar_serie'),
    path('agregar/<int:tmdb_id>/', views.agregar_desde_tmdb, name='agregar_desde_tmdb'),
    path('agregar-catalogo/<int:tmdb_id>/', views.agregar_catalogo_personal, name='agregar_catalogo_personal'),
    path('perfil/', views.perfil_usuario_view, name='perfil'),
    path('populares/<str:media_type>/', views.populares_view, name='populares'),
    path('estrenos/<str:media_type>/', views.estrenos_view, name='estrenos'),
    path('prximamente/<str:media_type>/', views.prontas_estrenar_view, name='prontas_estrenar'),
]
