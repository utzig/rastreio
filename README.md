# Rastreio

Este é um pequeno utilitário utilizado para capturar informações de rastreamento
de pacotes enviados para o Brasil (usando o site dos correios).

## Como usar

Gere um arquivo ~/.rastreio.conf com um código de rastreio por linha. Exemplo:

    RF12345678CN
    RF98765432SG

Rode o utilitário ./rastreio.

## Requisitos

* Python 2.6, 3.x
* requests

## TODO

- Suporte a verificação de mudanças (pode ser feito salvando o número atual de linhas)
