from django.db.models.deletion import ProtectedError
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Categoria, Despesa
from .serializers import CategoriaSerializer, DespesaSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.order_by("nome")
    serializer_class = CategoriaSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"detail": "A categoria possui despesas vinculadas."},
                status=status.HTTP_409_CONFLICT,
            )


class DespesaViewSet(viewsets.ModelViewSet):
    queryset = Despesa.objects.order_by("-data", "-pk")
    serializer_class = DespesaSerializer
