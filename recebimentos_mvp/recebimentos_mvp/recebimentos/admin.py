from django.contrib import admin
from .models import Profile, Categoria, Setor, MembroSetor, Movimentacao, Auditoria


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "cargo", "telefone"]


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ["nome", "descricao"]
    search_fields = ["nome"]


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ["nome", "orcamento_planejado"]
    search_fields = ["nome"]


@admin.register(MembroSetor)
class MembroSetorAdmin(admin.ModelAdmin):
    list_display = ["usuario", "setor", "papel", "data_entrada"]
    list_filter = ["setor", "papel"]


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ["tipo", "setor", "categoria", "valor", "data_movimentacao", "usuario"]
    list_filter = ["tipo", "setor", "categoria"]
    search_fields = ["setor__nome", "categoria__nome"]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ["acao", "descricao", "usuario", "data_hora"]
    readonly_fields = ["usuario", "acao", "descricao", "data_hora"]
