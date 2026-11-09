from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome


class Despesa(models.Model):
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    data = models.DateField()
    paga = models.BooleanField(default=False)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="despesas",
    )

    def __str__(self):
        return self.descricao
