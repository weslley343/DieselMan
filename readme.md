## SETUP
create a venv

``` python3 -m venv .venv ```

entra na venv

``` source .venv/bin/activate ```

instala dependencias

``` pip install -r requirements.txt ```

ativa banco de dados

``` docker compose -f compose/postgres/docker-compose.yml up -d ```

inicia a aplicacao

``` fast api dev main.py ```

para o banco de dados

``` docker compose -f compose/postgres/docker-compose.yml stop ```


## TESTS

``` PYTHONPATH=$(pwd) pytest ```