from django.shortcuts import render, redirect
from .models import Gasto, Recebimento, LogAcesso
from .forms import GastoForm, RecebimentoForm
from django.contrib.auth.decorators import login_required, user_passes_test

# Testes de permissão
def e_financeiro(user):
    return user.groups.filter(name='Financeiro').exists()

def e_auditoria(user):
    return user.groups.filter(name='Auditoria').exists()

# Usuário 1: Acesso apenas a Cadastros 
@login_required
@user_passes_test(e_financeiro)
def cadastrar_gasto(request):
    return render(request, 'core/form.html', {'form': form, 'titulo': 'Cadastro de Gastos'})

# Usuário 2: Acesso apenas a Logs de Auditoria 
@login_required
@user_passes_test(e_auditoria)
def listar_logs(request):
    logs = LogAcesso.objects.all().order_by('-data_hora')
    return render(request, 'core/logs.html', {'logs': logs})

# Função auxiliar para registrar logs de auditoria
@login_required
def registrar_log(request, acao, montante):
    LogAcesso.objects.create(
        usuario=request.user if request.user.is_authenticated else None,
        acao=acao,
        montante=montante,
        ip=request.META.get('REMOTE_ADDR')
    )


@login_required
def index(request):
    registrar_log(request, "Acesso à página inicial", 0)
    return render(request, 'core/index.html')

@login_required
def cadastrar_gasto(request):
    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            gasto = form.save()
            registrar_log(request, f"Cadastro de Gasto realizado: ID {gasto.id}",gasto.montante)
            return redirect('index')
    else:
        form = GastoForm()
    return render(request, 'core/form.html', {'form': form, 'titulo': 'Cadastro de Gastos'})

@login_required
def cadastrar_recebimento(request):
    if request.method == 'POST':
        form = RecebimentoForm(request.POST)
        if form.is_valid():
            recebimento = form.save()
            registrar_log(request, f"Cadastro de Recebimento realizado: ID {recebimento.id}", recebimento.montante)
            return redirect('index')
    else:
        form = RecebimentoForm()
    return render(request, 'core/form.html', {'form': form, 'titulo': 'Cadastro de Recebimentos'})

@login_required
def listar_logs(request):
    logs = LogAcesso.objects.all().order_by('-data_hora')
    return render(request, 'core/logs.html', {'logs': logs})
