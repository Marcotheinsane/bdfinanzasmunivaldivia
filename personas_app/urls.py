from django.urls import path
from personas import views



# Enrutamiento simple para poder dar a basto a 4 simples vistas
urlpatterns = [
    path('', views.lista_personas, name='lista_personas'),
    path('agregar/', views.agregar_persona, name='agregar_persona'),
    path('editar/<int:id>/', views.editar_persona, name='editar_persona'),
    path('eliminar/<int:id>/', views.eliminar_persona, name='eliminar_persona'),
    path('importar-csv/', views.importar_csv, name='importar_csv'),
]
