import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.http import JsonResponse
from .models import Recebimento, CentroPlanejamento, Contrato, LogRecebimento
from .forms import RecebimentoForm, RecebimentoFiltroForm


def _log(recebimento, usuario, acao, detalhes):
    LogRecebimento.objects.create(
        recebimento=recebimento, usuario=usuario, acao=acao, detalhes=detalhes
    )


@login_required
def dashboard(request):
    total_pendentes = Recebimento.objects.filter(status="pendente").aggregate(s=Sum("valor"))["s"] or 0
    total_confirmados = Recebimento.objects.filter(status="confirmado").aggregate(s=Sum("valor"))["s"] or 0
    ultimos = Recebimento.objects.select_related("centro_planejamento", "criado_por").order_by("-criado_em")[:10]
    return render(request, "recebimentos/dashboard.html", {
        "total_pendentes": total_pendentes,
        "total_confirmados": total_confirmados,
        "ultimos": ultimos,
        "count_pendentes": Recebimento.objects.filter(status="pendente").count(),
        "count_confirmados": Recebimento.objects.filter(status="confirmado").count(),
        "count_cancelados": Recebimento.objects.filter(status="cancelado").count(),
    })


@login_required
def listar(request):
    form = RecebimentoFiltroForm(request.GET or None)
    qs = Recebimento.objects.select_related("centro_planejamento", "contrato", "criado_por")

    if form.is_valid():
        if form.cleaned_data.get("numero_documento"):
            qs = qs.filter(numero_documento__icontains=form.cleaned_data["numero_documento"])
        if form.cleaned_data.get("centro_planejamento"):
            qs = qs.filter(centro_planejamento=form.cleaned_data["centro_planejamento"])
        if form.cleaned_data.get("status"):
            qs = qs.filter(status=form.cleaned_data["status"])
        if form.cleaned_data.get("data_inicio"):
            qs = qs.filter(data_recebimento__gte=form.cleaned_data["data_inicio"])
        if form.cleaned_data.get("data_fim"):
            qs = qs.filter(data_recebimento__lte=form.cleaned_data["data_fim"])

    total_filtrado = qs.aggregate(s=Sum("valor"))["s"] or 0
    return render(request, "recebimentos/listar.html", {
        "recebimentos": qs,
        "form": form,
        "total_filtrado": total_filtrado,
    })


@login_required
def criar(request):
    if request.method == "POST":
        form = RecebimentoForm(request.POST)
        if form.is_valid():
            rec = form.save(commit=False)
            rec.criado_por = request.user
            rec.full_clean()
            rec.save()
            _log(rec, request.user, "criacao", f"Recebimento {rec.numero_documento} criado com valor R$ {rec.valor}")
            messages.success(request, f"Recebimento {rec.numero_documento} cadastrado com sucesso!")
            return redirect("recebimentos:detalhe", pk=rec.pk)
    else:
        form = RecebimentoForm()
    return render(request, "recebimentos/form.html", {"form": form, "titulo": "Novo Recebimento", "action": "Cadastrar"})


@login_required
def detalhe(request, pk):
    rec = get_object_or_404(Recebimento.objects.select_related("centro_planejamento", "contrato", "criado_por"), pk=pk)
    logs = rec.logs.select_related("usuario").order_by("-data_hora")
    return render(request, "recebimentos/detalhe.html", {"rec": rec, "logs": logs})


@login_required
def editar(request, pk):
    rec = get_object_or_404(Recebimento, pk=pk)
    if rec.status == "cancelado":
        messages.error(request, "Recebimentos cancelados nao podem ser editados.")
        return redirect("recebimentos:detalhe", pk=pk)

    if request.method == "POST":
        form = RecebimentoForm(request.POST, instance=rec)
        if form.is_valid():
            changed = {f: (form.initial.get(f), form.cleaned_data[f]) for f in form.changed_data}
            rec = form.save(commit=False)
            rec.full_clean()
            rec.save()
            _log(rec, request.user, "edicao", f"Campos alterados: {changed}")
            messages.success(request, "Recebimento atualizado com sucesso!")
            return redirect("recebimentos:detalhe", pk=rec.pk)
    else:
        form = RecebimentoForm(instance=rec)
    return render(request, "recebimentos/form.html", {"form": form, "titulo": "Editar Recebimento", "action": "Salvar", "rec": rec})


@login_required
def confirmar(request, pk):
    rec = get_object_or_404(Recebimento, pk=pk)
    if rec.status != "pendente":
        messages.warning(request, "Apenas recebimentos pendentes podem ser confirmados.")
    else:
        rec.status = "confirmado"
        rec.save()
        _log(rec, request.user, "confirmacao", "Recebimento confirmado.")
        messages.success(request, "Recebimento confirmado!")
    return redirect("recebimentos:detalhe", pk=pk)


@login_required
def cancelar(request, pk):
    rec = get_object_or_404(Recebimento, pk=pk)
    if rec.status == "cancelado":
        messages.warning(request, "Recebimento ja esta cancelado.")
    else:
        rec.status = "cancelado"
        rec.save()
        _log(rec, request.user, "cancelamento", f"Recebimento cancelado pelo usuario {request.user}.")
        messages.success(request, "Recebimento cancelado.")
    return redirect("recebimentos:detalhe", pk=pk)


def contratos_por_centro(request):
    """AJAX: retorna contratos filhos do centro de planejamento selecionado."""
    centro_id = request.GET.get("centro_id")
    contratos = Contrato.objects.filter(centro_planejamento_id=centro_id, ativo=True).values("id", "numero", "descricao")
    return JsonResponse(list(contratos), safe=False)