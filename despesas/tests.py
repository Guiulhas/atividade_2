from django.db import IntegrityError, transaction
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Categoria, Despesa


class ControleDespesasTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.categoria = Categoria.objects.create(nome="Transporte")
        cls.despesa = Despesa.objects.create(
            descricao="Ônibus", valor="5.00", data="2026-11-09",
            categoria=cls.categoria,
        )

    def test_cadastra_categoria(self):
        resposta = self.client.post(reverse("categoria-list"), {"nome": "Alimentação"})
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Categoria.objects.filter(nome="Alimentação").exists())

    def test_cadastra_despesa_com_categoria(self):
        resposta = self.client.post(reverse("despesa-list"), {
            "descricao": "Metrô", "valor": "4.50", "data": "2026-11-09",
            "categoria": self.categoria.pk,
        })
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        despesa = Despesa.objects.get(pk=resposta.data["id"])
        self.assertEqual(despesa.categoria, self.categoria)
        self.assertFalse(despesa.paga)

    def test_consulta_despesas(self):
        resposta = self.client.get(reverse("despesa-list"))
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual([item["id"] for item in resposta.data], [self.despesa.pk])
        self.assertEqual(resposta.data[0]["valor"], "5.00")

    def test_marca_despesa_como_paga(self):
        url = reverse("despesa-detail", args=[self.despesa.pk])
        resposta = self.client.patch(url, {"paga": True})
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.despesa.refresh_from_db()
        self.assertTrue(self.despesa.paga)

    def test_exclui_despesa(self):
        url = reverse("despesa-detail", args=[self.despesa.pk])
        resposta = self.client.delete(url)
        self.assertEqual(resposta.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Despesa.objects.filter(pk=self.despesa.pk).exists())

    def test_rejeita_valor_zero_ou_negativo(self):
        for valor in ("0.00", "-1.00"):
            with self.subTest(valor=valor):
                resposta = self.client.post(reverse("despesa-list"), {
                    "descricao": "Inválida", "valor": valor, "data": "2026-11-09",
                    "categoria": self.categoria.pk,
                })
                self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn("valor", resposta.data)
        self.assertEqual(Despesa.objects.count(), 1)

    def test_banco_rejeita_gravacao_direta_com_valor_invalido(self):
        for valor in ("0.00", "-1.00"):
            with self.subTest(valor=valor):
                with self.assertRaises(IntegrityError), transaction.atomic():
                    Despesa.objects.create(
                        descricao="Inválida",
                        valor=valor,
                        data="2026-11-09",
                        categoria=self.categoria,
                    )

    def test_preserva_categoria_com_despesa_vinculada(self):
        url = reverse("categoria-detail", args=[self.categoria.pk])
        resposta = self.client.delete(url)
        self.assertEqual(resposta.status_code, status.HTTP_409_CONFLICT)
        self.assertTrue(Categoria.objects.filter(pk=self.categoria.pk).exists())
        self.assertTrue(Despesa.objects.filter(pk=self.despesa.pk).exists())
