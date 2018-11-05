# Meeting

[![Build Status](https://travis-ci.org/lucaspolo/meeting.svg?branch=master)](https://travis-ci.org/lucaspolo/meeting)
[![codecov](https://codecov.io/gh/lucaspolo/meeting/branch/master/graph/badge.svg)](https://codecov.io/gh/lucaspolo/meeting)

Sistema de reserva de salas para reuniões contando com as seguintes funcionalidades:

- API de Salas
- API de Reuniões (Agendamentos das Salas)

## Instalação do Projeto

Para instalar o projeto faça um clone do mesmo em sua área, com o comando:

```bash
$ git clone git@github.com:lucaspolo/meeting.git
```

Depois crie um virtualenv dentro da sua área, o ative e instale as dependências:

```bash
$ cd meeting
$ python3.6 -m venv .venv
$ ./venvbin/activate

$ pip install -r requirements-dev.txt
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
$ pytest meeting/tests --cov=meeting
```

Os testes serão executados e também será gerado um relatório de cobertura.

### Aplicação

Para executar a aplicação, basta executar o comando:

```bash
$ flask run
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

#### Criando e editando salas

Para criar uma sala basta enviar um método POST com um json contendo o `nome` da sala e sua `capacidade`:

```bash
$ http --json --form POST localhost:5000/api/sala/ nome="Knuth" capacidade=10 
```

Irá retornar uma confirmação com o ID da nova sala:

```json
{
    "sala criada": "3192ba04e08011e8b7ca1c394760687f"
}
```

Para alterar a sala, basta enviar para `api/sala/ID` um PUT contendo as informações da sala:

```bash
$ http --json --form PUT localhost:5000/api/sala/3192ba04e08011e8b7ca1c394760687f nome="Knuth" capacidade=30
```

JSON:
```json
{
    "sala atualizada": "3192ba04e08011e8b7ca1c394760687f"
}
```

Para excluir, basta enviar DELETE para `api/sala/ID`:

```bash
$ http --json --form DELETE localhost:5000/api/sala/3192ba04e08011e8b7ca1c394760687f
```

JSON:
```json
{
    "sala excluida": "3192ba04e08011e8b7ca1c394760687f"
}
```

**Obs: A exclusão de salas ocorre de maneira lógica para que não ocorram agendamentos sem sala.**

## Agendamentos

Para acessar o recurso de agendamentos é necessário `localhost:5000/api/agendamento/`.

#### Recuperando agendamentos

Para recuperar os agendamentos é necessário enviar um get para o recurso:

```bash
$ http --form GET localhost:5000/api/agendamento/
```

JSON:
```json
{
    "agendamentos": [
        {
            "_id": "46a1e0e3e11711e8b7ca1c394760687f",
            "fim": "2018-12-02T08:10:00",
            "inicio": "2018-12-02T08:00:00",
            "sala_id": "46a1e0e1e11711e8b7ca1c394760687f",
            "titulo": "Fechamento mensal"
        },
        {
            "_id": "46a1e0e4e11711e8b7ca1c394760687f",
            "fim": "2018-12-02T08:10:00",
            "inicio": "2018-12-02T08:00:00",
            "sala_id": "46a1e0e0e11711e8b7ca1c394760687f",
            "titulo": "Weekly meeting"
        }
    ]
}
```

Para recuperar informações de um agendamento específico, basta solicitar pelo seu ID:

```bash
$ http --form GET localhost:5000/api/agendamento/46a1e0e3e11711e8b7ca1c394760687f
```

JSON:
```json
{
    "_id": "46a1e0e3e11711e8b7ca1c394760687f",
    "fim": "2018-12-02T08:10:00",
    "inicio": "2018-12-02T08:00:00",
    "sala_id": "46a1e0e1e11711e8b7ca1c394760687f",
    "titulo": "Fechamento mensal"
}
```

#### Criando e editando agendamento

Para criar um agendamento basta submeter um POST para o recurso, com as informações de `titulo`, `inicio`, `fim` e o `sala_id`. Lembrando que inicio e fim deve seguir o seguinte formato `%Y-%m-%dT%H:%M:%S`:

```bash
$ http --json --form POST localhost:5000/api/agendamento/ titulo="Festa de Fim de Ano" inicio="2018-12-20T18:00:00" fim="2018-12-20T22:00:00" sala_id="46a1e0e1e11711e8b7ca1c394760687f"
```

Retornará o ID da reunião criada:

```json
{
    "agendamento criado": "7eabf5d2e11911e8b7ca1c394760687f"
}
```

Caso tente incluir um agendamento na mesma sala e horário, será apresentado um erro:

```bash
$ http --json --form POST localhost:5000/api/agendamento/ titulo="Limpeza de carpete" inicio="2018-12-20T20:00:00" fim="2018-12-20T22:00:00" sala_id="46a1e0e1e11711e8b7ca1c394760687f"
```
Retorno:

```json
{
    "Agendamento inválido": "Ja existe reuniao para esta sala neste horario"
}
```

Para atualizar, basta enviar as alterações via PUT para o recurso desejado:

```bash
$ http --json --form PUT localhost:5000/api/agendamento/7eabf5d2e11911e8b7ca1c394760687f titulo="Limpeza de carpete" inicio="2018-12-20T18:00:00" fim="2018-12-20T22:00:00" sala_id="46a1e0e1e11711e8b7ca1c394760687f"
```

Retornando a confirmação:

```json
{
    "agendamento atualizado": "7eabf5d2e11911e8b7ca1c394760687f"
}
```

Para remover, basta enviar o delete para o recurso:

```bash
$ http --form DELETE localhost:5000/api/agendamento/7eabf5d2e11911e8b7ca1c394760687f
```

Retornando a confirmação:

```json
{
    "agendamento excluido": "7eabf5d2e11911e8b7ca1c394760687f"
}
```

O agendamento será excluído definitivamente.