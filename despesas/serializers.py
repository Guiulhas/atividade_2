from rest_framework import serializers

from .models import Categoria, Despesa


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ("id", "nome", "descricao")


class DespesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Despesa
        fields = ("id", "descricao", "valor", "data", "paga", "categoria")
