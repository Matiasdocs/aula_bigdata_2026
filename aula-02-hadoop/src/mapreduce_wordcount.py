"""
Aula 02 - Hadoop & MapReduce
Lab: Contagem de palavras distribuída simulando um job Hadoop MapReduce.

Instruções gerais
------------------
Este job usa a biblioteca `mrjob`, que implementa o MESMO modelo de
programação MapReduce usado pelo Hadoop de verdade (map -> shuffle/sort
-> reduce). Em modo "inline"/"local" (o que os testes automáticos usam),
o mrjob simula um cluster Hadoop na sua própria máquina, sem precisar
instalar um cluster de verdade.

Como testar localmente antes de enviar a PR:
    pip install -r requirements.txt
    pytest -v
"""
from mrjob.job import MRJob
import re

# Palavras muito comuns em português que não agregam valor a uma análise
# de frequência de palavras (artigos, preposições, conjunções, etc.)
STOPWORDS = {
    "a", "o", "os", "as", "de", "da", "do", "das", "dos", "e", "que",
    "em", "um", "uma", "para", "com", "no", "na", "nos", "nas", "se",
    "por", "sua", "seu", "ao", "à", "às",
}

# Regex simples para extrair "palavras" (sequências de letras, incluindo
# acentos) de uma linha de texto.
WORD_RE = re.compile(r"[A-Za-zÀ-ÿ]+")


class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        """
        Chamada uma vez para cada linha do arquivo de entrada. Para cada
        palavra: converte para minúsculas, ignora se for stopword, e
        emite (palavra, 1).
        """
        for word in WORD_RE.findall(line.lower()):
            if word in STOPWORDS:
                continue
            yield word, 1

    def combiner(self, word, counts):
        """
        Roda localmente em cada máquina antes de enviar os dados pela
        rede para os reducers (otimização de tráfego de rede).
        """
        yield word, sum(counts)

    def reducer(self, word, counts):
        """
        Recebe todos os valores emitidos para uma mesma chave (palavra)
        e soma o total.
        """
        yield word, sum(counts)


if __name__ == "__main__":
    MRWordFrequencyCount.run()