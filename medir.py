"""Tarefas 3, 4 e 5: mede o tempo variando o corte, compara com a rápida
pura e gera o gráfico tempo x corte.

Para reduzir ruído: as variantes são intercaladas (cada entrada é ordenada
por todas, em ordem embaralhada), o coletor de lixo fica desligado durante
a cronometragem e reportamos a mediana de várias repetições."""
import gc
import random
import statistics
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ordenacao import quicksort, quicksort_hibrido

N = 20_000
CORTES = [1, 5, 10, 16, 20, 32, 50, 100, 200]
REPETICOES = 41
AQUECIMENTO = 3


def main():
    random.seed(42)
    variantes = {"pura": quicksort}
    for c in CORTES:
        variantes[c] = (lambda v, c=c: quicksort_hibrido(v, c))
    tempos = {k: [] for k in variantes}

    for rep in range(AQUECIMENTO + REPETICOES):
        v = [random.randint(0, 1_000_000) for _ in range(N)]
        esperado = sorted(v)
        ordem = list(variantes)
        random.shuffle(ordem)
        for k in ordem:
            gc.collect()
            gc.disable()
            t0 = time.perf_counter()
            r = variantes[k](v)
            dt = time.perf_counter() - t0
            gc.enable()
            assert r == esperado, f"{k}: resultado não ordenado!"
            if rep >= AQUECIMENTO:
                tempos[k].append(dt * 1000)

    med = {k: statistics.median(t) for k, t in tempos.items()}
    iqr = {k: statistics.quantiles(t, n=4) for k, t in tempos.items()}
    pura = med["pura"]

    print(f"N={N}, {REPETICOES} repetições (mediana, ms)")
    print("| variante | mediana (ms) | Q1–Q3 (ms) | ganho sobre a pura |")
    print("|---|---:|---:|---:|")
    q = iqr["pura"]
    print(f"| rápida pura | {pura:.2f} | {q[0]:.2f}–{q[2]:.2f} | — |")
    for c in CORTES:
        q = iqr[c]
        print(f"| corte = {c} | {med[c]:.2f} | {q[0]:.2f}–{q[2]:.2f} | "
              f"{(pura - med[c]) / pura * 100:+.1f}% |")

    melhor = min(CORTES, key=lambda c: med[c])
    print(f"\nMelhor corte: {melhor} ({med[melhor]:.2f} ms, "
          f"{(pura - med[melhor]) / pura * 100:.1f}% mais rápido que a pura)")

    plt.figure(figsize=(8, 5))
    y = [med[c] for c in CORTES]
    lo = [med[c] - iqr[c][0] for c in CORTES]
    hi = [iqr[c][2] - med[c] for c in CORTES]
    plt.errorbar(CORTES, y, yerr=[lo, hi], fmt="o-", capsize=4,
                 label="Híbrida (rápida + inserção)")
    plt.axhline(pura, color="red", linestyle="--",
                label=f"Rápida pura ({pura:.1f} ms)")
    plt.scatter([melhor], [med[melhor]], s=180, facecolors="none",
                edgecolors="green", linewidths=2, zorder=5,
                label=f"Melhor corte = {melhor}")
    plt.xscale("log")
    plt.xticks(CORTES, [str(c) for c in CORTES])
    plt.minorticks_off()
    plt.xlabel("corte (escala log)")
    plt.ylabel("tempo (ms) — mediana, barras = Q1–Q3")
    plt.title(f"Tempo x corte — {N} elementos aleatórios, {REPETICOES} repetições")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("grafico_corte.png", dpi=120)


if __name__ == "__main__":
    main()
