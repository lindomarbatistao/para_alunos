from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    class TipoUsuario(models.TextChoices):
        PROPRIETARIO = "PROPRIETARIO", "Proprietário"
        MORADOR = "MORADOR", 'Morador'
        # NOME_DA_CONSTANTE = "VALOR_NO_BANCO", "TEXTO_EXIBIDO"
    
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    tipo = models.CharField(
        max_length=20,
        choices=TipoUsuario.choices,
        default=TipoUsuario.MORADOR
    )
    
    def __str__(self):
        return self.get_full_name() or self.username

    
class Imovel(models.Model):
    class TipoImovel(models.TextChoices):
        CASA = "CASA", "Casa"
        APARTAMENTO = "APTO", "Apartamento"
        KITNET = "KIT", "Kitnet"
        SOBRADO = "SOBR", "Sobrado"
        CHACARA = "CHAC", "Chácara"
        SITIO = "SITIO", "Sítio"
        FAZENDA = "FAZENDA", "Fazenda"
        TERRENO = "TERRENO", "Terreno"
        SALA_COMERCIAL = "SALA_COM", "Sala comercial"
        LOJA = "LOJA", "Loja"
        GALPAO = "GALPAO", "Galpão"
        ESCRITORIO = "ESCR", "Escritório"
    
    titulo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100, choices=TipoImovel, default=TipoImovel.APARTAMENTO)
    valor_aluguel = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)
    logradouro = models.CharField(max_length=200)
    cep = models.CharField(max_length=12)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)

    proprietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="imoveis")

    def __str__(self):
        return self.titulo


class Contrato(models.Model):
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    imovel = models.ForeignKey(Imovel, on_delete=models.PROTECT, related_name='contrato')
    proprietario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='proprietario')
    morador = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='morador')

    def __str__(self):
        return f"Contrato {self.id}"

class Pagamento(models.Model):
    data_pagamento = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=False)
    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT, related_name='pagamentos')

    def __str__(self):
        return f"Pagamento {self.id}"