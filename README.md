# Meeting

[![Build Status](https://travis-ci.org/lucaspolo/meeting.svg?branch=master)](https://travis-ci.org/lucaspolo/meeting)
[![codecov](https://codecov.io/gh/lucaspolo/meeting/branch/master/graph/badge.svg)](https://codecov.io/gh/lucaspolo/meeting)

Sistema de reserva de salas para reuniões contando com as seguintes funcionalidades:

- API de Salas
- API de Reuniões (Agendamentos das Salas)

## Instalação do Projeto

Para instalar o projeto faça um clone do mesmo em sua área, com o comando:

```bash
git clone git@github.com:lucaspolo/meeting.git
```

Depois crie um virtualenv dentro da sua área, o ative e instale as dependências:

```bash
cd meeting
python3.6 -m venv .venv
./venvbin/activate

pip install -r requirements-dev.txt
```

Com isto o projeto estará instalado e pronto para ser executado e alterado.

## Execução

Para executar a aplicação e os testes é necessário primeiro configurar estas duas variáveis de ambiente:

```bash
FLASK_APP=meeting/app.py
FLASK_ENV=development
```

### Testes

Como primeira etapa, executaremos os testes do projeto, que serão executados da seguinte forma:

```bash
pytest meeting/tests --cov=meeting
```

Os testes serão executados e também será gerado um relatório de cobertura.

### Aplicação

Para executar a aplicação, basta executar o comando:

```bash
flask run
```

Com isto a aplicação estará executando localmente e já poderá receber requisições.

## Salas

Para acessar os serviços de salas basta enviarmos requisições para `localhost:5000/api/sala/`, através do método HTTP adequado:

#### Recuperando as salas

Para recuperar todas as salas cadastradas basta enviar uma requisição GET:

```bash
$ http --form GET localhost:5000/api/sala/

```
Retornará um JSON contendo uma lista de todas as salas:

```json
{
    "salas": [
        {
            "_id": "be9b0ae8e07e11e8b7ca1c394760687f",
            "ativa": false,
            "capacidade": "40",
            "nome": "Turing"
        },
        {
            "_id": "be9b0ae9e07e11e8b7ca1c394760687f",
            "ativa": true,
            "capacidade": 15,
            "nome": "Ramalho"
        },
        {
            "_id": "be9b0aece07e11e8b7ca1c394760687f",
            "ativa": true,
            "capacidade": "10",
            "nome": "Currie"
        }
    ]
}
```

### Criando e editando salas

Para criar uma sala basta enviar um método POST com um json contendo o `nome` da sala e sua `capacidade`:

```bash
# http --json --form POST localhost:5000/api/sala/ nome="Knuth" capacidade=10 
```

Irá retornar uma confirmação com o ID da nova sala:

```json
{
    "sala criada": "3192ba04e08011e8b7ca1c394760687f"
}
```

Para alterar a sala, basta enviar para `api/sala/ID` um PUT contendo as informações da sala:

```bash
http --json --form PUT localhost:5000/api/sala/3192ba04e08011e8b7ca1c394760687f nome="Knuth" capacidade=30
```

JSON:
```json
{
    "sala atualizada": "3192ba04e08011e8b7ca1c394760687f"
}
```

Para excluir, basta enviar DELETE para `api/sala/ID`:

```bash
http --json --form DELETE localhost:5000/api/sala/3192ba04e08011e8b7ca1c394760687f
```

JSON:
```json
{
    "sala excluida": "3192ba04e08011e8b7ca1c394760687f"
}
```

Obs: A exclusão de salas ocorre de maneira lógica para que não ocorram agendamentos sem sala.