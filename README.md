# API de controle de despesas

Trabalho da Unidade 2 de Manutenção de Software. A API usa Django REST Framework e SQLite e parte do [Django Quick Project da UFERSA](https://github.com/lisa-ufersa/django-quickproject).

## Execução local

Use Python 3.10 ou 3.11. No PowerShell, dentro da pasta do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

A documentação interativa fica em [Swagger](http://127.0.0.1:8000/swagger/). Os endpoints de despesas e categorias são acessíveis sem login para uso local.

## Entidades e rotas

| Entidade | Campos | Coleção | Registro |
| --- | --- | --- | --- |
| Categoria | nome único, descrição opcional | /api/categorias/ | /api/categorias/{id}/ |
| Despesa | descrição, valor, data, paga, categoria | /api/despesas/ | /api/despesas/{id}/ |

Use GET e POST na coleção. Use GET, PUT, PATCH e DELETE no registro. Uma categoria pode ter várias despesas. O campo categoria recebe o ID de uma categoria existente.

Primeiro, envie um POST a /api/categorias/ com {"nome": "Transporte"}. Depois, use o ID retornado para cadastrar uma despesa. O exemplo abaixo usa o ID 1.

```json
{
  "descricao": "Ônibus",
  "valor": "5.00",
  "data": "2026-11-09",
  "paga": false,
  "categoria": 1
}
```

Valores menores que 0,01 são rejeitados com HTTP 400. A exclusão de categoria com despesas vinculadas retorna HTTP 409.

## Testes

```powershell
.\.venv\Scripts\python.exe manage.py test
```

A suíte verifica cadastro, consulta, atualização, exclusão e as regras de valor mínimo e de proteção da categoria. Os testes usam um banco SQLite temporário.
