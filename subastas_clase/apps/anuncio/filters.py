from django_filters import rest_framework as filters
from apps.anuncio.models import Categoria, Anuncio


class CategoriaFilter(filters.FilterSet):
    nombre = filters.CharFilter(field_name='nombre', lookup_expr='icontains')
    nombre_con =filters.CharFilter(field_name='nombre',lookup_expr='istartswith')

    class Meta:
        model=Categoria
        fields=['nombre','activa']

class AnuncioFilter(filters.FilterSet):
    titulo = filters.CharFilter(field_name='titulo', lookup_expr='icontains') #coincidencia parcial - es dificil que elñ usuario ponga el nombre exacto.
    precio_desde = filters.NumberFilter(field_name='precio_inicial', lookup_expr='gte')
    categorias= filters.BaseInFilter(field_name='categorias__id',lookup_expr='in')

    class Meta:
        model=Anuncio
        fields=['activo','titulo','precio_inicial']
