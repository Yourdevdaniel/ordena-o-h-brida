# Ordenação híbrida: rápida + inserção — onde fica o ponto de troca?

## O que foi feito

- **`ordenacao.py`**
  - `quicksort(v)`: ordenação rápida com **pivô aleatório**, separando em três listas — **menores**, **iguais** e **maiores** que o pivô — e ordenando recursivamente só as pontas.
  - `quicksort_hibrido(v, corte)`: mesmo algoritmo, mas quando o pedaço tem **menos que `corte` elementos** (`len(v) < corte`) chama `insercao(v)` em vez de continuar recursando.
  - `insercao(v)`: ordenação por inserção clássica.
- **`medir.py`**: mede o tempo com **20 000 inteiros aleatórios** (0 a 1 000 000) para a rápida pura e para os cortes 1, 5, 10, 16, 20, 32, 50, 100 e 200, e gera o gráfico.
- **`verifica_corte1.py`**: confirma que corte = 1 equivale à rápida pura.

### Metodologia de medição

Uma primeira rodada simples (todas as entradas da variante A, depois todas da B…) deu números ruidosos e incoerentes (ex.: corte = 1 15% mais lento que a pura, corte = 16 pior que 10 e 20). Para medir de forma justa:

- 41 entradas aleatórias diferentes (+3 de aquecimento descartadas);
- **cada entrada é ordenada por todas as variantes**, em ordem embaralhada — assim oscilações da máquina afetam todas igualmente;
- coletor de lixo (`gc`) desligado durante a cronometragem;
- reportada a **mediana** e o intervalo interquartil (Q1–Q3);
- cada resultado é conferido contra `sorted(v)`.

Ambiente: Python 3, CPython, Linux. Os valores absolutos dependem da máquina; o que importa é a forma da curva.

## Resultados

| variante | mediana (ms) | Q1–Q3 (ms) | ganho sobre a pura |
|---|---:|---:|---:|
| rápida pura | 44,77 | 42,53–50,96 | — |
| corte = 1 | 45,92 | 44,54–52,26 | −2,6% |
| corte = 5 | 39,92 | 38,98–44,02 | +10,8% |
| corte = 10 | 36,88 | 35,71–40,03 | +17,6% |
| corte = 16 | 36,43 | 34,43–38,98 | +18,6% |
| **corte = 20** | **34,86** | 33,36–39,67 | **+22,1%** |
| corte = 32 | 36,09 | 34,95–39,52 | +19,4% |
| corte = 50 | 38,00 | 36,73–40,34 | +15,1% |
| corte = 100 | 48,78 | 46,35–52,28 | −9,0% |
| corte = 200 | 68,77 | 67,30–77,58 | −53,6% |

![Tempo em função do corte](grafico_corte.png)

## Qual corte deu o melhor tempo

O **melhor corte foi 20**: 34,86 ms contra 44,77 ms da rápida pura — **cerca de 22% mais rápido** (≈ 9,9 ms a menos).

O fundo da curva é largo: de **10 a 50** todos os cortes ficam entre 15% e 22% melhores que a pura, e as faixas Q1–Q3 de 10, 16, 20 e 32 se sobrepõem. Ou seja, o ponto exato (20 vs. 16 vs. 32) pode trocar de lugar de uma rodada para outra; o que é robusto é a **região de 10 a ~50**. Isso bate com o que bibliotecas reais usam (cortes na casa de 10 a 32).

**Por que ganha?** Perto das folhas da recursão, a rápida gasta muito com pedaços minúsculos: cada chamada cria três listas novas, sorteia um pivô e concatena resultados. Para poucos elementos, esse custo fixo é maior que o trabalho útil. A inserção, embora seja O(n²), tem custo por operação muito baixo (só comparações e deslocamentos no lugar) e, para n pequeno, n² é pequeno. Trocar nas folhas elimina milhares de chamadas recursivas.

## O que acontece com cortes grandes demais

A partir de algum ponto o termo quadrático da inserção domina:

- **corte = 100** já é **9% mais lento** que a rápida pura;
- **corte = 200** é **54% mais lento** (68,8 ms).

Com um corte grande, a inserção recebe pedaços de até ~corte elementos, e o custo dela cresce como corte² por pedaço. Somando sobre os ~n/corte pedaços, o trabalho extra fica proporcional a **n · corte** — cresce linearmente com o corte, enquanto o que se economiza em recursão é limitado. Por isso a curva sobe rapidamente depois de ~50. No limite (corte > n) o algoritmo vira inserção pura, O(n²).

## Confirmação: corte = 1 se comporta como a rápida pura

Com `corte = 1`, a condição `len(v) < 1` só é verdadeira para **listas vazias** — que a rápida pura já devolveria de imediato. Então o algoritmo nunca troca de verdade.

1. **Pelo tempo:** 45,92 ms contra 44,77 ms — diferença de 2,6%, dentro do ruído (as faixas Q1–Q3 42,5–51,0 e 44,5–52,3 se sobrepõem). A pequena diferença vem só do `if` extra e da chamada a `insercao([])`.
2. **Pela estrutura** (`verifica_corte1.py`): fixando a mesma semente aleatória, as duas versões escolhem os mesmos pivôs e fazem **exatamente 26 539 chamadas recursivas** cada, com o mesmo resultado. A inserção foi chamada 6 731 vezes — **todas com lista vazia, nenhuma com elementos**.

Logo, corte = 1 é, na prática, a rápida pura.

## Conclusão

Combinar os métodos vale a pena: com corte em torno de **20** (faixa boa: 10–50) ganhamos ~**22%** sobre a rápida pura. Cortes pequenos demais não aproveitam a troca (corte = 1 é idêntico à pura), e cortes grandes demais (≥ 100) pioram o tempo porque a inserção quadrática passa a trabalhar em pedaços grandes.
