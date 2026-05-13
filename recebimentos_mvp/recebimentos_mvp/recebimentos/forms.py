from django import forms
from .models import Movimentacao, Setor, Categoria


class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        exclude = ["usuario"]
        widgets = {
            "setor": forms.Select(attrs={"class": "form-select"}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "valor": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.01"}),
            "data_movimentacao": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

    def clean_valor(self):
        valor = self.cleaned_data.get("valor")
        if valor is not None and valor <= 0:
            raise forms.ValidationError("O valor deve ser maior que zero.")
        return valor


class MovimentacaoFiltroForm(forms.Form):
    setor = forms.ModelChoiceField(
        queryset=Setor.objects.all(), required=False,
        empty_label="Todos os setores",
        widget=forms.Select(attrs={"class": "form-select"}))
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(), required=False,
        empty_label="Todas as categorias",
        widget=forms.Select(attrs={"class": "form-select"}))
    tipo = forms.ChoiceField(
        choices=[("", "Todos os tipos"), ("Recebimento", "Recebimento"), ("Gasto", "Gasto")],
        required=False, widget=forms.Select(attrs={"class": "form-select"}))
    data_inicio = forms.DateField(required=False, widget=forms.DateInput(
        attrs={"type": "date", "class": "form-control"}))
    data_fim = forms.DateField(required=False, widget=forms.DateInput(
        attrs={"type": "date", "class": "form-control"}))
