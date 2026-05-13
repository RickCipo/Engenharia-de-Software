from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from .models import Movimentacao, Setor, Categoria, Auditoria
from .forms import MovimentacaoForm, MovimentacaoFiltroForm

ACAO_CRIAR = 1
ACAO_EDITAR = 2
ACAO_EXCLUIR = 3


def _log(usuario, acao, descricao):
    Auditoria.objects.create(usuario=usuario, acao=acao, descricao=descricao[:100])


@login_required
def dashboard(request):
    recebimentos = Movimentacao.objects.filter(tipo="Recebimento")
    gastos = Movimentacao.objects.filter(tipo="Gasto")
    total_recebido = recebimentos.aggregate(s=Sum("valor"))["s"] or 0
    total_gasto = gastos.aggregate(s=Sum("valor"))["s"] or 0
    ultimos = Movimentacao.objects.select_related("setor", "categoria", "usuario").order_by("-data_movimentacao")[:10]
    setores = Setor.objects.all()
    return render(request, "recebimentos/dashboard.html", {
        "total_recebido": total_recebido,
        "total_gasto": total_gasto,
        "saldo": total_recebido - total_gasto,
        "count_recebimentos": recebimentos.count(),
        "count_gastos": gastos.count(),
        "ultimos": ultimos,
        "setores": setores,
    })


@login_required
def listar(request):
    form = MovimentacaoFiltroForm(request.GET or None)
    qs = Movimentacao.objects.select_related("setor", "categoria", "usuario")

    if form.is_valid():
        if form.cleaned_data.get("setor"):
            qs = qs.filter(setor=form.cleaned_data["setor"])
        if form.cleaned_data.get("categoria"):
            qs = qs.filter(categoria=form.cleaned_data["categoria"])
        if form.cleaned_data.get("tipo"):
            qs = qs.filter(tipo=form.cleaned_data["tipo"])
        if form.cleaned_data.get("data_inicio"):
            qs = qs.filter(data_movimentacao__gte=form.cleaned_data["data_inicio"])
        if form.cleaned_data.get("data_fim"):
            qs = qs.filter(data_movimentacao__lte=form.cleaned_data["data_fim"])

    total = qs.aggregate(s=Sum("valor"))["s"] or 0
    return render(request, "recebimentos/listar.html", {"movimentacoes": qs, "form": form, "total": total})


@login_required
def criar(request):
    if request.method == "POST":
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            mov = form.save(commit=False)
            mov.usuario = request.user
            mov.save()
            _log(request.user, ACAO_CRIAR, f"{mov.tipo} de R$ {mov.valor} criado no setor {mov.setor}")
            messages.success(request, f"{mov.tipo} cadastrado com sucesso!")
            return redirect("recebimentos:detalhe", pk=mov.pk)
    else:
        form = MovimentacaoForm()
    return render(request, "recebimentos/form.html", {"form": form, "titulo": "Nova Movimentacao", "action": "Cadastrar"})


@login_required
def detalhe(request, pk):
    mov = get_object_or_404(Movimentacao.objects.select_related("setor", "categoria", "usuario"), pk=pk)
    return render(request, "recebimentos/detalhe.html", {"mov": mov})


@login_required
def editar(request, pk):
    mov = get_object_or_404(Movimentacao, pk=pk)
    if request.method == "POST":
        form = MovimentacaoForm(request.POST, instance=mov)
        if form.is_valid():
            mov = form.save()
            _log(request.user, ACAO_EDITAR, f"{mov.tipo} ID {mov.pk} editado")
            messages.success(request, "Movimentacao atualizada!")
            return redirect("recebimentos:detalhe", pk=mov.pk)
    else:
        form = MovimentacaoForm(instance=mov)
    return render(request, "recebimentos/form.html", {"form": form, "titulo": "Editar Movimentacao", "action": "Salvar", "mov": mov})


@login_required
def excluir(request, pk):
    mov = get_object_or_404(Movimentacao, pk=pk)
    if request.method == "POST":
        desc = f"{mov.tipo} ID {mov.pk} excluido"
        mov.delete()
        _log(request.user, ACAO_EXCLUIR, desc)
        messages.success(request, "Movimentacao excluida com sucesso.")
        return redirect("recebimentos:listar")
    return render(request, "recebimentos/confirmar_exclusao.html", {"mov": mov})
