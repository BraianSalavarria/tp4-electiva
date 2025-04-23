from datetime import datetime


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.anuncio.filters import CategoriaFilter, AnuncioFilter
from apps.anuncio.models import Categoria, Anuncio
from apps.anuncio.serializers import AnuncioReadSerializer, CategoriaSerializer, AnuncioSerializer
from apps.usuario.models import Usuario


class CategoriaListaAPIView(APIView):
    def get(self,request,format=None):
        categorias = Categoria.objects.all()
        categoriasSerializer = CategoriaSerializer(categorias, many=True)
        return Response(categoriasSerializer.data)

    def post(self,request,format=None):
        categoriaSerializer = CategoriaSerializer(data=request.data)
        if categoriaSerializer.is_valid():
            categoriaSerializer.save()
            return Response(categoriaSerializer.data,status=status.HTTP_201_CREATED)
        return Response(categoriaSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoriaDetalleAPIView(APIView):
    def get(self,request,pk,format=None):
        categoria = get_object_or_404(Categoria,pk=pk)
        categoriaSerializer = CategoriaSerializer(categoria)
        if categoria:
            return Response(categoriaSerializer.data, status=status.HTTP_200_OK)
        return Response(categoriaSerializer.errors, status=status.HTTP_404_NOT_FOUND)

    def put(self,request,pk, format=None):
        categoria = get_object_or_404(Categoria,pk=pk)
        categoriaSerializer = CategoriaSerializer(categoria,data=request.data)
        if categoriaSerializer.is_valid():
            categoriaSerializer.save()
            return Response(categoriaSerializer.data,status=status.HTTP_200_OK)
        return Response(categoriaSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk, format=None):
        categoria = get_object_or_404(Categoria, pk=pk)
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AnuncioListaAPIView(APIView):
    def get(self,request,format=None):
        anuncios = Anuncio.objects.all()
        anunciosSerializer = AnuncioReadSerializer(anuncios,many=True)
        return Response(anunciosSerializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
       anuncioSerializer = AnuncioSerializer(data=request.data)
       if anuncioSerializer.is_valid():
           anuncioSerializer.save()
           return Response(anuncioSerializer.data,status=status.HTTP_201_CREATED)
       return Response(anuncioSerializer.errors,status=status.HTTP_400_BAD_REQUEST)

class AnuncioDetalleAPIView(APIView):
    def get(self,request,pk, format=None):
        anuncio = get_object_or_404(Anuncio,pk=pk)
        anuncioSerializer = AnuncioSerializer(anuncio)
        return Response(anuncioSerializer.data,status = status.HTTP_200_OK)

    def put(self,request,pk,format=None):
        anuncio = get_object_or_404(Anuncio,pk=pk)
        anuncioSerializer=AnuncioSerializer(anuncio,data=request.data)
        if anuncioSerializer.is_valid():
            anuncioSerializer.save()
            return Response(anuncioSerializer.data, status=status.HTTP_200_OK)
        return Response(anuncioSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk, format=None):
        anuncio=get_object_or_404(Anuncio,pk=pk)
        anuncio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#-------------------------------   Vistas Concretas/Genericas --------------------------------------------------------#
class CategoriaListaGenericView(ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class CategoriaDetalleGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class AnuncioListaGenericView(ListCreateAPIView):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer

    def perform_create(self, serializer):
        usuario= Usuario.objects.get(id=1)
        serializer.save(publicado_por=usuario)


class AnuncioDetalleGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer

# ---------------------------------------------- Views Sets ------------------------------------------------
# class CategoriaViewSet(viewsets.ModelViewSet):
#     queryset = Categoria.objects.all()
#     serializer_class = CategoriaSerializer

# class AnuncioViewSet(viewsets.ModelViewSet):
#     queryset = Anuncio.objects.all()
#     serializer_class = AnuncioSerializer
#
#     def perform_create(self, serializer):
#         usuario= Usuario.objects.get(id=1)
#         serializer.save(publicado_por=usuario)
#
#     @action(detail=True, methods=['get'])
#     def tiempo_restante(self, request, pk=None):
#         anuncio = self.get_object()
#         ahora = datetime.now(anuncio.fecha_fin.tzinfo)
#         diferencia = anuncio.fecha_fin - ahora
#
#         dias = diferencia.days
#         horas = diferencia.seconds // 3600
#         minutos = (diferencia.seconds % 3600) // 60
#
#         return Response({
#             'dias':dias,
#             'horas':horas,
#             'minutos':minutos,
#         })

#--------------------------------------- Trabajo Practico 4 ---------------------------------------

#filtro usando parametro en la URL
# class CategoriaViewSet(viewsets.ModelViewSet):
#     serializer_class = CategoriaSerializer
#     def get_queryset(self):
#         queryset=Categoria.objects.all()
#         nombre=self.request.query_params.get('nombre', None)
#         if nombre is not None:
#             queryset = queryset.filter(nombre=nombre)
#         return queryset

#usando filterset_fields de la clase DjangoFilterBackends (usa parametros de la URL)
# class CategoriaViewSet(viewsets.ModelViewSet):
#     queryset = Categoria.objects.all()
#     serializer_class = CategoriaSerializer
#     filterset_fields = ['nombre', 'activa']

#usando una clase personalizada que hereda de FilterSet
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CategoriaFilter
    ordering_fields =['nombre','activa']
    ordering = ['nombre']


class AnuncioViewSet(viewsets.ModelViewSet):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = AnuncioFilter
    ordering_fields =['titulo','id']
    ordering = ['titulo'] #ordenamiento por defecto

    def perform_create(self, serializer):
        usuario= Usuario.objects.get(id=1)
        serializer.save(publicado_por=usuario)

    @action(detail=True, methods=['get'])
    def tiempo_restante(self, request, pk=None):
        anuncio = self.get_object()
        ahora = datetime.now(anuncio.fecha_fin.tzinfo)
        diferencia = anuncio.fecha_fin - ahora

        dias = diferencia.days
        horas = diferencia.seconds // 3600
        minutos = (diferencia.seconds % 3600) // 60

        return Response({
            'dias':dias,
            'horas':horas,
            'minutos':minutos,
        })
