from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    foto = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    cargo = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


class Setor(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    orcamento_planejado = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome


class MembroSetor(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE)
    papel = models.CharField(max_length=50)
    data_entrada = models.DateField(auto_now_add=True)


class Movimentacao(models.Model):
    TIPO_CHOICES = [
        ("Recebimento", "Recebimento"),
        ("Gasto", "Gasto"),
    ]
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=100, choices=TIPO_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_movimentacao = models.DateField()

    class Meta:
        ordering = ["-data_movimentacao"]

    def __str__(self):
        return f"{self.tipo} - R$ {self.valor} ({self.setor})"


class Auditoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    acao = models.IntegerField()
    descricao = models.CharField(max_length=100)
    data_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_hora"]

    def __str__(self):
        return f"[{self.acao}] {self.descricao} - {self.data_hora:%d/%m/%Y %H:%M}"
