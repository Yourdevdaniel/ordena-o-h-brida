"""Confirma que corte=1 se comporta como a rápida pura: com a mesma semente,
as duas fazem as mesmas escolhas de pivô e o mesmo número de chamadas, e a
inserção só é chamada em listas vazias (len < 1)."""
import random
import ordenacao as o

_g = random.Random(7)
v = [_g.randint(0, 10**6) for _ in range(20_000)]
cont = {"qs": 0, "hib": 0, "ins": 0, "ins_nao_vazia": 0}

orig_qs, orig_hib, orig_ins = o.quicksort, o.quicksort_hibrido, o.insercao
def qs(x): cont["qs"] += 1; return orig_qs(x)
def hib(x, c): cont["hib"] += 1; return orig_hib(x, c)
def ins(x):
    cont["ins"] += 1
    if x: cont["ins_nao_vazia"] += 1
    return orig_ins(x)
o.quicksort, o.quicksort_hibrido, o.insercao = qs, hib, ins

random.seed(123); a = o.quicksort(v)
random.seed(123); b = o.quicksort_hibrido(v, 1)
print("mesmo resultado:", a == b == sorted(v))
print("chamadas quicksort puro:", cont["qs"])
print("chamadas híbrido corte=1:", cont["hib"])
print("chamadas à inserção:", cont["ins"], "| com lista não vazia:", cont["ins_nao_vazia"])
