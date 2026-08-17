# Aula 15 — API REST com Flask (somente JSON)

Atividade prática de CRUD via API REST. **Este projeto não tem frontend**: não há
`render_template`, pasta `views/` nem arquivos HTML. Toda resposta é JSON, gerada
com `jsonify()`, e os testes são feitos pelo PowerShell (`Invoke-RestMethod`),
Postman, Insomnia ou curl.

---

## 1. Estrutura do projeto

```
Aula15-API/
├── app.py                  # ponto de entrada: cria o app, o banco e o seed
├── requirements.txt        # flask e flask-sqlalchemy
├── atividade.md            # este arquivo
├── controllers/
│   ├── __init__.py         # exporta o Blueprint livros_api_bp
│   ├── livros_api.py       # rotas da API (GET, POST, PUT, DELETE)
│   └── api/                # pasta reservada (vazia por enquanto)
└── models/
    ├── __init__.py         # cria o objeto db e exporta os Models
    ├── base.py             # ModeloBase abstrato (id, data_criacao, data_atualizacao)
    └── livro.py            # Model Livro (tabela "livros")
```

O banco `biblioteca.db` (SQLite) é criado sozinho na primeira execução, junto com
o seed dos 3 livros iniciais definidos em `DADOS_INICIAIS`.

## 2. Como executar

```powershell
pip install -r requirements.txt
python app.py
```

O servidor sobe em `http://127.0.0.1:5000` com `debug=True`. Abrir a raiz `/`
devolve a documentação dos endpoints em JSON — não é uma home HTML.

## 3. Endpoints

| Método | Rota | Descrição | Status de sucesso |
|--------|------|-----------|-------------------|
| GET | `/api/livros` | Lista todos os livros (ordenados por título) | 200 |
| GET | `/api/livros/<id>` | Detalhe de um livro | 200 (ou 404) |
| POST | `/api/livros` | Cria um livro (JSON no body) | 201 Created |
| PUT | `/api/livros/<id>` | Atualiza os campos enviados | 200 (ou 404) |
| DELETE | `/api/livros/<id>` | Remove o livro | 204 No Content |

Erros de validação (falta de JSON, campo `ano` não inteiro, título/autor vazios)
retornam **400** com `{"erro": "..."}`.

> **Dica de acentuação no PowerShell 5.1:** ao enviar títulos com acento, o
> `-Body` como string pode chegar corrompido no servidor. Para garantir UTF-8:
> `-Body ([System.Text.Encoding]::UTF8.GetBytes('{"titulo":"Macunaíma", ...}'))`.

---

## 4. POST — inserindo 15 livros novos

Como o seed já gravou 3 livros (ids 1, 2 e 3), os 15 novos recebem os **ids 4 a 18**.

### Comandos

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/livros `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"titulo":"O Alienista","autor":"Machado de Assis","ano":1882}'

Invoke-RestMethod http://127.0.0.1:5000/api/livros `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"titulo":"Memórias Póstumas de Brás Cubas","autor":"Machado de Assis","ano":1881}'

Invoke-RestMethod http://127.0.0.1:5000/api/livros `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"titulo":"Quincas Borba","autor":"Machado de Assis","ano":1891}'

Invoke-RestMethod http://127.0.0.1:5000/api/livros `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"titulo":"Iracema","autor":"José de Alencar","ano":1865}'

Invoke-RestMethod http://127.0.0.1:5000/api/livros `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"titulo":"Senhora","autor":"José de Alencar","ano":1875}'

Invoke-RestMethod http://127.0.0.1:5000/api/livros `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"titulo":"O Guarani","autor":"José de Alencar","ano":1857}'

Invoke-RestMethod http://127.0.0.1:5000/api/livros `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"titulo":"Vidas Secas","autor":"Graciliano Ramos","ano":1938}'

Invoke-RestMethod http://127.0.0.1:5000/api/livros `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"titulo":"Grande Sertão: Veredas","autor":"João Guimarães Rosa","ano":1956}'

Invoke-RestMethod http://127.0.0.1:5000/api/livros `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"titulo":"Capitães da Areia","autor":"Jorge Amado","ano":1937}'

Invoke-RestMethod http://127.0.0.1:5000/api/livros `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"titulo":"A Hora da Estrela","autor":"Clarice Lispector","ano":1977}'

Invoke-RestMethod http://127.0.0.1:5000/api/livros `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"titulo":"Macunaíma","autor":"Mário de Andrade","ano":1928}'

Invoke-RestMethod http://127.0.0.1:5000/api/livros `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"titulo":"A Moreninha","autor":"Joaquim Manuel de Macedo","ano":1844}'

Invoke-RestMethod http://127.0.0.1:5000/api/livros `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"titulo":"Triste Fim de Policarpo Quaresma","autor":"Lima Barreto","ano":1915}'

Invoke-RestMethod http://127.0.0.1:5000/api/livros `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"titulo":"Os Sertões","autor":"Euclides da Cunha","ano":1902}'

Invoke-RestMethod http://127.0.0.1:5000/api/livros `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"titulo":"O Ateneu","autor":"Raul Pompeia","ano":1888}'
```

### Resultado

```
ano          : 1882
autor        : Machado de Assis
data_criacao : 2026-07-27 09:35:42.243532
id           : 4
titulo       : O Alienista

ano          : 1881
autor        : Machado de Assis
data_criacao : 2026-07-27 09:35:53.337745
id           : 5
titulo       : Memórias Póstumas de Brás Cubas

ano          : 1891
autor        : Machado de Assis
data_criacao : 2026-07-27 09:36:04.431958
id           : 6
titulo       : Quincas Borba

ano          : 1865
autor        : José de Alencar
data_criacao : 2026-07-27 09:36:15.526171
id           : 7
titulo       : Iracema

ano          : 1875
autor        : José de Alencar
data_criacao : 2026-07-27 09:36:26.620384
id           : 8
titulo       : Senhora

ano          : 1857
autor        : José de Alencar
data_criacao : 2026-07-27 09:36:37.714597
id           : 9
titulo       : O Guarani

ano          : 1938
autor        : Graciliano Ramos
data_criacao : 2026-07-27 09:36:48.808810
id           : 10
titulo       : Vidas Secas

ano          : 1956
autor        : João Guimarães Rosa
data_criacao : 2026-07-27 09:36:59.903023
id           : 11
titulo       : Grande Sertão: Veredas

ano          : 1937
autor        : Jorge Amado
data_criacao : 2026-07-27 09:37:10.997236
id           : 12
titulo       : Capitães da Areia

ano          : 1977
autor        : Clarice Lispector
data_criacao : 2026-07-27 09:37:22.091449
id           : 13
titulo       : A Hora da Estrela

ano          : 1928
autor        : Mário de Andrade
data_criacao : 2026-07-27 09:37:33.185662
id           : 14
titulo       : Macunaíma

ano          : 1844
autor        : Joaquim Manuel de Macedo
data_criacao : 2026-07-27 09:37:44.279875
id           : 15
titulo       : A Moreninha

ano          : 1915
autor        : Lima Barreto
data_criacao : 2026-07-27 09:37:55.374088
id           : 16
titulo       : Triste Fim de Policarpo Quaresma

ano          : 1902
autor        : Euclides da Cunha
data_criacao : 2026-07-27 09:38:06.468301
id           : 17
titulo       : Os Sertões

ano          : 1888
autor        : Raul Pompeia
data_criacao : 2026-07-27 09:38:17.562514
id           : 18
titulo       : O Ateneu
```

---

## 5. PUT — atualizando o livro de id 1

### Comando

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/livros/1 `
  -Method PUT `
  -ContentType "application/json" `
  -Body '{"titulo":"Cotemig","autor":"3A1","ano":2026}'
```

### Resultado

```
ano          : 2026
autor        : 3A1
data_criacao : 2026-07-27 09:35:08.960893
id           : 1
titulo       : Cotemig
```

Repare que o `id` e o `data_criacao` **não mudam** — o PUT altera apenas os campos
enviados no JSON, conforme o método `atualizar_de_dict()` do Model. Quem muda
sozinho é o `data_atualizacao`, por causa do `onupdate=datetime.now` em `base.py`
(ele não aparece na saída porque `para_dict()` não o inclui).

### Lista completa após o PUT — 18 livros

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/livros
```

```
ano          : 1949
autor        : George Orwell
data_criacao : 2026-07-27 09:35:31.149319
id           : 3
titulo       : 1984

ano          : 1977
autor        : Clarice Lispector
data_criacao : 2026-07-27 09:37:22.091449
id           : 13
titulo       : A Hora da Estrela

ano          : 1844
autor        : Joaquim Manuel de Macedo
data_criacao : 2026-07-27 09:37:44.279875
id           : 15
titulo       : A Moreninha

ano          : 1937
autor        : Jorge Amado
data_criacao : 2026-07-27 09:37:10.997236
id           : 12
titulo       : Capitães da Areia

ano          : 2026
autor        : 3A1
data_criacao : 2026-07-27 09:35:08.960893
id           : 1
titulo       : Cotemig

ano          : 1956
autor        : João Guimarães Rosa
data_criacao : 2026-07-27 09:36:59.903023
id           : 11
titulo       : Grande Sertão: Veredas

ano          : 1865
autor        : José de Alencar
data_criacao : 2026-07-27 09:36:15.526171
id           : 7
titulo       : Iracema

ano          : 1928
autor        : Mário de Andrade
data_criacao : 2026-07-27 09:37:33.185662
id           : 14
titulo       : Macunaíma

ano          : 1881
autor        : Machado de Assis
data_criacao : 2026-07-27 09:35:53.337745
id           : 5
titulo       : Memórias Póstumas de Brás Cubas

ano          : 1882
autor        : Machado de Assis
data_criacao : 2026-07-27 09:35:42.243532
id           : 4
titulo       : O Alienista

ano          : 1888
autor        : Raul Pompeia
data_criacao : 2026-07-27 09:38:17.562514
id           : 18
titulo       : O Ateneu

ano          : 1890
autor        : Aluísio Azevedo
data_criacao : 2026-07-27 09:35:20.055106
id           : 2
titulo       : O Cortiço

ano          : 1857
autor        : José de Alencar
data_criacao : 2026-07-27 09:36:37.714597
id           : 9
titulo       : O Guarani

ano          : 1902
autor        : Euclides da Cunha
data_criacao : 2026-07-27 09:38:06.468301
id           : 17
titulo       : Os Sertões

ano          : 1891
autor        : Machado de Assis
data_criacao : 2026-07-27 09:36:04.431958
id           : 6
titulo       : Quincas Borba

ano          : 1875
autor        : José de Alencar
data_criacao : 2026-07-27 09:36:26.620384
id           : 8
titulo       : Senhora

ano          : 1915
autor        : Lima Barreto
data_criacao : 2026-07-27 09:37:55.374088
id           : 16
titulo       : Triste Fim de Policarpo Quaresma

ano          : 1938
autor        : Graciliano Ramos
data_criacao : 2026-07-27 09:36:48.808810
id           : 10
titulo       : Vidas Secas
```

A ordem não é a de inserção: `Livro.listar()` usa `order_by(cls.titulo)`, então a
saída vem em ordem alfabética de título. Por isso `1984` aparece primeiro (dígitos
vêm antes de letras) e `Cotemig`, que era o id 1, agora aparece no meio da lista.

---

## 6. DELETE — removendo os ids 5, 6 e 7

### Comandos

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/livros/5 -Method DELETE
Invoke-RestMethod http://127.0.0.1:5000/api/livros/6 -Method DELETE
Invoke-RestMethod http://127.0.0.1:5000/api/livros/7 -Method DELETE
```

Os três comandos **não imprimem nada**: a rota devolve `204 No Content`, ou seja,
sucesso sem corpo na resposta. Se rodar o mesmo comando duas vezes, o segundo
retorna erro 404 (`Livro não encontrado`).

Foram removidos:

| id | título | autor |
|----|--------|-------|
| 5 | Memórias Póstumas de Brás Cubas | Machado de Assis |
| 6 | Quincas Borba | Machado de Assis |
| 7 | Iracema | José de Alencar |

### Lista final — 15 livros

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/livros
```

```
ano          : 1949
autor        : George Orwell
data_criacao : 2026-07-27 09:35:31.149319
id           : 3
titulo       : 1984

ano          : 1977
autor        : Clarice Lispector
data_criacao : 2026-07-27 09:37:22.091449
id           : 13
titulo       : A Hora da Estrela

ano          : 1844
autor        : Joaquim Manuel de Macedo
data_criacao : 2026-07-27 09:37:44.279875
id           : 15
titulo       : A Moreninha

ano          : 1937
autor        : Jorge Amado
data_criacao : 2026-07-27 09:37:10.997236
id           : 12
titulo       : Capitães da Areia

ano          : 2026
autor        : 3A1
data_criacao : 2026-07-27 09:35:08.960893
id           : 1
titulo       : Cotemig

ano          : 1956
autor        : João Guimarães Rosa
data_criacao : 2026-07-27 09:36:59.903023
id           : 11
titulo       : Grande Sertão: Veredas

ano          : 1928
autor        : Mário de Andrade
data_criacao : 2026-07-27 09:37:33.185662
id           : 14
titulo       : Macunaíma

ano          : 1882
autor        : Machado de Assis
data_criacao : 2026-07-27 09:35:42.243532
id           : 4
titulo       : O Alienista

ano          : 1888
autor        : Raul Pompeia
data_criacao : 2026-07-27 09:38:17.562514
id           : 18
titulo       : O Ateneu

ano          : 1890
autor        : Aluísio Azevedo
data_criacao : 2026-07-27 09:35:20.055106
id           : 2
titulo       : O Cortiço

ano          : 1857
autor        : José de Alencar
data_criacao : 2026-07-27 09:36:37.714597
id           : 9
titulo       : O Guarani

ano          : 1902
autor        : Euclides da Cunha
data_criacao : 2026-07-27 09:38:06.468301
id           : 17
titulo       : Os Sertões

ano          : 1875
autor        : José de Alencar
data_criacao : 2026-07-27 09:36:26.620384
id           : 8
titulo       : Senhora

ano          : 1915
autor        : Lima Barreto
data_criacao : 2026-07-27 09:37:55.374088
id           : 16
titulo       : Triste Fim de Policarpo Quaresma

ano          : 1938
autor        : Graciliano Ramos
data_criacao : 2026-07-27 09:36:48.808810
id           : 10
titulo       : Vidas Secas
```

---

## 7. Conferência final

| Etapa | Total no banco |
|-------|----------------|
| Seed inicial | 3 |
| Após os 15 POST | 18 |
| Após o PUT (id 1) | 18 (o PUT não cria registro) |
| Após os 3 DELETE | **15** |

Os ids 5, 6 e 7 não são reaproveitados: o SQLite continua a contagem do último id
usado, então o próximo livro criado receberá o id 19.

## 8. O que ficou claro nesta aula

- **API REST não devolve página**: o mesmo Model das aulas anteriores é usado, mas
  o Controller troca `render_template` por `jsonify` e não há redirect nem flash.
- **O verbo HTTP define a intenção**: GET lê, POST cria, PUT atualiza, DELETE remove
  — todos na mesma rota `/api/livros`.
- **O status code faz parte da resposta**: 201 para criação, 204 para exclusão,
  400 para erro do cliente, 404 para recurso inexistente.
- **`jsonify` só aceita tipos JSON**: por isso `para_dict()` converte o `datetime`
  de `data_criacao` em string com `str(...)`.
- **`__abstract__ = True`** em `ModeloBase` evita criar uma tabela para a superclasse;
  `id`, `data_criacao` e `data_atualizacao` são herdados pelo `Livro`.

> Os horários em `data_criacao` correspondem à execução de referência registrada
> aqui; ao rodar o projeto novamente os valores de data/hora serão diferentes.
