"""Quicksort com pivô aleatório (partição em menores/iguais/maiores)
e versão híbrida que troca para inserção em pedaços pequenos."""
import random


def insercao(v):
    """Ordenação por inserção. Devolve uma nova lista ordenada."""
    a = list(v)
    for i in range(1, len(a)):
        chave = a[i]
        j = i - 1
        while j >= 0 and a[j] > chave:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = chave
    return a


def quicksort(v):
    """Tarefa 1: rápida pura, pivô aleatório, três partes."""
    if len(v) <= 1:
        return list(v)
    pivo = random.choice(v)
    menores = [x for x in v if x < pivo]
    iguais = [x for x in v if x == pivo]
    maiores = [x for x in v if x > pivo]
    return quicksort(menores) + iguais + quicksort(maiores)


def quicksort_hibrido(v, corte):
    """Tarefa 2: igual à rápida, mas usa inserção quando len(v) < corte."""
    if len(v) < corte:
        return insercao(v)
    if len(v) <= 1:
        return list(v)
    pivo = random.choice(v)
    menores = [x for x in v if x < pivo]
    iguais = [x for x in v if x == pivo]
    maiores = [x for x in v if x > pivo]
    return (quicksort_hibrido(menores, corte) + iguais
            + quicksort_hibrido(maiores, corte))
