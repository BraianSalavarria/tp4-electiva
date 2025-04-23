from django.urls import path

from apps.anuncio.api import CategoriaListaAPIView, CategoriaDetalleAPIView, AnuncioListaAPIView, AnuncioDetalleAPIView, \
    CategoriaListaGenericView, CategoriaDetalleGenericView, AnuncioListaGenericView, AnuncioDetalleGenericView

app_name='anuncio'

urlpatterns = [
    path('api-view/categorias/', CategoriaListaAPIView.as_view()),
    path('api-view/categorias/<int:pk>/',CategoriaDetalleAPIView.as_view()),
    path('api-view/anuncios/',AnuncioListaAPIView.as_view()),
    path('api-view/anuncios/<int:pk>/',AnuncioDetalleAPIView.as_view()),
    path('generic-view/categorias/',CategoriaListaGenericView.as_view()),
    path('generic-view/categorias/<int:pk>/',CategoriaDetalleGenericView.as_view()),
    path('generic-view/anuncios/',AnuncioListaGenericView.as_view()),
    path('generic-view/anuncios/<int:pk>/',AnuncioDetalleGenericView.as_view()),
]