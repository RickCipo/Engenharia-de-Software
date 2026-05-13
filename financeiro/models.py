from django.db import models
from django.contrib.auth.models import User

# Extensão do Usuário (Sua tabela PROFILES)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    foto = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    cargo = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username

# Tabela CATEGORIAS
class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

# Tabela SETORES
class Setor(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    orcamento_planejado = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome

# Tabela MEMBROS_SETOR (Relação Many-to-Many com dados extras)
class MembroSetor(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE)
    papel = models.CharField(max_length=50) # Ex: Gerente, Analista
    data_entrada = models.DateField(auto_now_add=True)

# Tabela MOVIMENTACOES (Onde entram os recebimentos)
class Movimentacao(models.Model):
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=100) # Ex: "Recebimento" ou "Gasto"
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_movimentacao = models.DateField()

# Tabela AUDITORIA
class Auditoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    acao = models.IntegerField() # Pode ser um código de status ou tipo de ação
    descricao = models.CharField(max_length=100)
    data_hora = models.DateTimeField(auto_now_add=True)