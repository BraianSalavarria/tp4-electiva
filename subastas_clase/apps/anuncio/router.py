#inicializamos el router
from os.path import basename

from rest_framework import routers

from apps.anuncio.api import CategoriaViewSet, AnuncioViewSet

router_V1 = routers.DefaultRouter()

#registramos el view set
router_V1.register(prefix='categoria',viewset=CategoriaViewSet, basename='categoria')
router_V1.register(prefix='anuncio', viewset=AnuncioViewSet, basename='anuncio')
