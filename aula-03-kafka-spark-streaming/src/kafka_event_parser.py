"""
Aula 03 - Apache Kafka e Spark Streaming
Lab (parte 1/2): Parsing e validacao de mensagens vindas de um topico
Kafka.

Contexto
--------
Em um pipeline real, um Kafka Consumer recebe mensagens em formato de
texto/bytes (o "value" da mensagem) e precisa:
  1. Decodificar/parsear o conteudo (geralmente JSON)
  2. Validar se a mensagem tem os campos esperados antes de processa-la
Este arquivo foca exatamente nessa logica -- a MESMA logica que voce
colocaria dentro de um Kafka Consumer real ou de um mapper de Spark
Streaming, so que aqui testada de forma isolada (sem precisar de um
broker Kafka rodando).

Como testar localmente antes de enviar a PR:
    pip install -r requirements.txt
    pytest -v
"""
import json

# Campos que toda mensagem de evento precisa ter para ser considerada
# valida neste pipeline.
REQUIRED_FIELDS = {"event_id", "event_time", "category", "amount"}


def parse_kafka_message(raw_value):
    """
    Recebe `raw_value` (uma string, o "value" de uma mensagem Kafka),
    faz o parse como JSON, valida se e um objeto e se tem os campos
    obrigatorios, e retorna o dicionario parseado.
    """
    try:
        parsed = json.loads(raw_value)
    except (json.JSONDecodeError, TypeError):
        raise ValueError("Mensagem nao e um JSON valido")

    if not isinstance(parsed, dict):
        raise ValueError("Mensagem JSON deve representar um objeto")

    faltantes = REQUIRED_FIELDS - parsed.keys()
    if faltantes:
        raise ValueError(f"Campos obrigatorios ausentes: {sorted(faltantes)}")

    return parsed


def is_valid_event(event):
    """
    Retorna True se, e somente se: todos os campos de REQUIRED_FIELDS
    estao presentes, "amount" e um numero, e "amount" e maior ou igual
    a zero.
    """
    if not REQUIRED_FIELDS.issubset(event.keys()):
        return False

    amount = event["amount"]
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        return False

    return amount >= 0


def filter_valid_events(events):
    """
    Recebe uma lista de dicionarios `events` e retorna apenas os que
    passam em `is_valid_event`.
    """
    return [event for event in events if is_valid_event(event)]