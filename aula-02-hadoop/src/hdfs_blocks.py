"""
Aula 02 - HDFS (Hadoop Distributed File System)
Lab: Simule, em Python, como o HDFS divide arquivos em blocos e os
distribui entre os nós (DataNodes) de um cluster.

Isso NÃO substitui o HDFS real -- é um modelo simplificado para você
praticar, na prática, os cálculos que o NameNode faz por trás dos panos
sempre que um arquivo é gravado no HDFS.

Como testar localmente antes de enviar a PR:
    pip install -r requirements.txt
    pytest -v
"""
import math


def calculate_num_blocks(file_size_mb: float, block_size_mb: int = 128) -> int:
    """
    Calcula quantos blocos HDFS são necessários para armazenar um arquivo
    de `file_size_mb` megabytes, usando blocos de `block_size_mb` MB cada.
    """
    return math.ceil(file_size_mb / block_size_mb)


def calculate_total_storage_with_replication(file_size_mb: float, replication_factor: int = 3) -> float:
    """
    Calcula o espaço TOTAL em disco (em MB) realmente ocupado no cluster
    para armazenar um arquivo de `file_size_mb` MB, considerando o fator
    de replicação.
    """
    return file_size_mb * replication_factor


def simulate_block_distribution(num_blocks: int, num_datanodes: int) -> dict:
    """
    Simula a distribuição round-robin de `num_blocks` blocos entre
    `num_datanodes` DataNodes, nomeados "datanode-1", "datanode-2", etc.
    """
    distribution = {f"datanode-{i + 1}": [] for i in range(num_datanodes)}
    for block_id in range(1, num_blocks + 1):
        node_index = (block_id - 1) % num_datanodes
        distribution[f"datanode-{node_index + 1}"].append(block_id)
    return distribution