# FinCorp — MVP Cadastro de Recebimentos
**Responsável:** Carolina Lee | **Projeto:** Pedro Henrique Saraiva Arruda

## Como rodar

```bash
# 1. Instalar dependências
pip install django

# 2. Aplicar migrações
python manage.py migrate

# 3. Criar superusuário (ou usar o já criado)
python manage.py createsuperuser

# 4. Rodar servidor
python manage.py runserver

# Acesse: http://127.0.0.1:8000
# Admin: http://127.0.0.1:8000/admin
# Login padrão: carolina / fincorp123
```

## Funcionalidades implementadas

- Dashboard com totais por status (Pendente, Confirmado, Cancelado)
- Listagem com filtros por documento, centro, status e período
- Cadastro com validações de integridade:
  - Número de documento único
  - Contrato deve pertencer ao mesmo centro de planejamento (validação no form e no model)
  - Valor deve ser positivo
  - Unique constraint (numero_documento + centro_planejamento)
- AJAX: contratos filtrados dinamicamente pelo centro de planejamento selecionado
- Fluxo de status: Pendente → Confirmado / Cancelado
- Log de auditoria em cada recebimento (criação, edição, confirmação, cancelamento)
- Admin Django completo com inline de logs

## Modelos

| Modelo | Descrição |
|--------|-----------|
| CentroPlanejamento | Centros de custo/receita da empresa |
| Contrato | Contratos vinculados a centros |
| Recebimento | Registro principal do recebimento |
| LogRecebimento | Auditoria de todas as alterações |
