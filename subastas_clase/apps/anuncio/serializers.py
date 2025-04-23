from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.anuncio.models import Categoria, Anuncio
from apps.usuario.models import Usuario
from django.utils.timezone import now
from datetime import timedelta


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            'id',
            'nombre',
            'activa',
        ]

class AnuncioSerializer(serializers.ModelSerializer):
    categorias = serializers.PrimaryKeyRelatedField(many=True, queryset=Categoria.objects.all())
    publicado_por = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())

    class Meta:
        model = Anuncio
        fields = [
            'id',
            'titulo',
            'descripcion',
            'precio_inicial',
            'imagen',
            'fecha_inicio',
            'fecha_fin',
            'activo',
            'categorias',
            'publicado_por',
            'oferta_ganadora'
        ]

    def validate_fecha_inicio(self,value):
        fecha_actual = now()
        if value <= fecha_actual:
            raise ValidationError("La fecha de inicio de un anuncio debe ser posterior a la fecha actual")
        return value

    def validate(self,data):
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        if fecha_fin is not None and fecha_inicio is not None:
            if fecha_fin <= fecha_inicio:
                raise ValidationError('La fecha de final de un anuncio no debe ser antes que su fecha de inicio')
        return data

    def validate_titulo(self,value):
        # Buscamos todos los anuncios con ese título
        anuncios = Anuncio.objects.filter(titulo=value)

        # Si estamos editando, excluimos el anuncio actual
        if self.instance:
            anuncios = anuncios.exclude(id=self.instance.id)

        # Si queda alguno, es porque otro anuncio tiene ese mismo título
        if anuncios.exists():
            raise ValidationError('Ya existe un anuncio con ese título.')
        return value

    def validate(self, data):
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            diferencia = fecha_fin - fecha_inicio

            if diferencia > timedelta(days=365):  # Aproximadamente 12 meses
                raise ValidationError({'fecha_fin':'La fecha de fin no puede ser más de 12 meses posterior a la fecha de inicio.'})

            if fecha_fin <= fecha_inicio:
                raise ValidationError({'fecha_fin':'La fecha de fin debe ser posterior a la fecha de inicio.'})

        return data


class AnuncioReadSerializer(serializers.ModelSerializer):

    categorias = serializers.StringRelatedField(many=True)
    publicado_por = serializers.StringRelatedField()

    class Meta:
        model = Anuncio
        fields = [
            'id',
            'titulo',
            'descripcion',
            'precio_inicial',
            'imagen',
            'fecha_inicio',
            'fecha_fin',
            'activo',
            'categorias',
            'publicado_por',
            'oferta_ganadora'
        ]
        