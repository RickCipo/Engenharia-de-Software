from django import forms
from .models import Gasto, Recebimento

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['data', 'responsavel', 'setor', 'montante', 'justificativa']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }

class RecebimentoForm(forms.ModelForm):
    class Meta:
        model = Recebimento
        fields = ['data', 'responsavel', 'setor', 'montante', 'detalhes']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }
