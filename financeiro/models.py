from django.db import models
from django.contrib.auth.models import User

class Gasto(models.Model):
    data = models.DateField()
    responsavel = models.CharField(max_length=100)
    setor = models.CharField(max_length=100) 
    montante = models.DecimalField(max_digits=10, decimal_places=2)
    justificativa = models.TextField()        

    def __str__(self):
        return f"Gasto {self.id} - {self.setor}"

class Recebimento(models.Model):
    data = models.DateField()
    responsavel = models.CharField(max_length=100)
    setor = models.CharField(max_length=100)     
    montante = models.DecimalField(max_digits=10, decimal_places=2) 
    detalhes = models.TextField()          

    def __str__(self):
        return f"Recebimento {self.id} - {self.responsavel}"

class LogAcesso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data_hora = models.DateTimeField(auto_now_add=True)
    acao = models.CharField(max_length=255) # Ex: "Criou Gasto ID 15"
    montante = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ip = models.GenericIPAddressField(null=True)

    def __str__(self):
        return f"{self.data_hora} - {self.acao}"
