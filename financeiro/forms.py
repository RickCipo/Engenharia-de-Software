from django import forms
from .models import Recebimento, CentroPlanejamento, Contrato


class RecebimentoForm(forms.ModelForm):
    class Meta:
        model = Recebimento
        exclude = ["criado_por", "criado_em", "atualizado_em"]
        widgets = {
            "data_recebimento": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "data_competencia": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "numero_documento": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex: REC-2024-0001"}),
            "descricao": forms.TextInput(attrs={"class": "form-control"}),
            "valor": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.01"}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "centro_planejamento": forms.Select(attrs={"class": "form-select", "id": "id_centro_planejamento"}),
            "contrato": forms.Select(attrs={"class": "form-select", "id": "id_contrato"}),
            "observacoes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["centro_planejamento"].queryset = CentroPlanejamento.objects.filter(ativo=True)
        self.fields["contrato"].queryset = Contrato.objects.filter(ativo=True)
        self.fields["contrato"].required = False

    def clean(self):
        cleaned_data = super().clean()
        contrato = cleaned_data.get("contrato")
        centro = cleaned_data.get("centro_planejamento")
        if contrato and centro and contrato.centro_planejamento != centro:
            self.add_error("contrato", "Este contrato nao pertence ao centro de planejamento selecionado.")
        return cleaned_data


class RecebimentoFiltroForm(forms.Form):
    numero_documento = forms.CharField(required=False, widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Buscar documento..."}))
    centro_planejamento = forms.ModelChoiceField(
        queryset=CentroPlanejamento.objects.filter(ativo=True),
        required=False, empty_label="Todos os centros",
        widget=forms.Select(attrs={"class": "form-select"}))
    status = forms.ChoiceField(
        choices=[("", "Todos os status")] + Recebimento.STATUS_CHOICES,
        required=False, widget=forms.Select(attrs={"class": "form-select"}))
    data_inicio = forms.DateField(required=False, widget=forms.DateInput(
        attrs={"type": "date", "class": "form-control"}))
    data_fim = forms.DateField(required=False, widget=forms.DateInput(
        attrs={"type": "date", "class": "form-control"}))