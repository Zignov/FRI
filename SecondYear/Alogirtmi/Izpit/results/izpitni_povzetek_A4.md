# Izpitni povzetek A4

## Asimptotika

- `O`: zgornja meja, `Ω`: spodnja meja, `Θ`: tesna meja.
- Poln graf: `m=Θ(n^2)`.
- 1 GHz ≈ `10^9` operacij/s.
- `log n < n < n log n < n^2 < n^3 < 2^n < n!`

## Amortizirana analiza

- Metoda vsote: skupno delo `T(n)` -> amortizirano `T(n)/n`.
- Dvojiški števec: `n+n/2+n/4+...<2n` -> `O(1)` amortizirano.
- Dinamična tabela s podvajanjem -> `insert O(1)` amortizirano.
- Potencial: `a_i = c_i + Phi(D_i)-Phi(D_{i-1})`.

## Zgoščevanje

- Veriženje: pričakovano `O(1+α)`, `α=n/m`.
- Linearno: `h(k,i)=(h(k)+i) mod m`.
- Brisanje pri odprtem naslavljanju: `DELETED`, ne prazno.
- Bloom: “zagotovo NE” / “verjetno DA”; false positive da, false negative ne.

## Drevesa

- BST: `search/insert/delete = O(h)`.
- Minimum BST: skrajno levo; maksimum: skrajno desno.
- AVL: `|h_L-h_R|<=1`.
- Rotacije: LL desna, RR leva, LR leva+desna, RL desna+leva.
- RČ: koren črn, rdeč nima rdečega otroka, vse poti imajo isto črno višino.
- AVL bolj uravnotežen; RČ manj rotacij.

## Kopica

- Min-kopica: `min O(1)`, `insert O(log n)`, `deleteMin O(log n)`, `heapify O(n)`.
- Kopica ni BST.

## Disjunktne množice

- `makeSet`, `find`, `union`.
- Uporabi path compression + union by rank/size.
- Kruskal: DSU za preverjanje ciklov.

## DP

- Koraki: stanje -> prehod -> osnove -> vrstni red -> rekonstrukcija.
- Stopnice 1/2: `f(n)=f(n-1)+f(n-2)`, `f(0)=1`, `f(1)=1`.
- 0/1 nahrbtnik: `dp[i][w]=max(dp[i-1][w], dp[i-1][w-w_i]+v_i)`.
- Delni nahrbtnik: sort po `v_i/w_i`, jemlji pohlepno.
- Matrična veriga: `c(i,j)=min_k(c(i,k)+c(k+1,j)+d_{i-1}d_kd_j)`, čas `O(n^3)`.

## Grafi

- MST ima `n-1` povezav, brez cikla, poveže vsa vozlišča.
- Prim: širi drevo z najcenejšo povezavo navzven.
- Kruskal: sort povezav, dodaj brez cikla, DSU.
- Topološko: samo DAG; vhodne stopnje 0 -> odstranjuj.
- DAG shortest path: topološki vrstni red + sproščanje, `O(n+m)`.
- Dijkstra: samo nenegativne uteži.
- Bellman-Ford: negativne uteži OK; `n-1` relaksacij + 1 za negativen cikel.
- Welsh-Powell: uredi vozlišča po padajoči stopnji, barvaj nesosednja z isto barvo.
- Največji pretok: preskoči.

## P/NP

- P: rešljivo v polinomskem času.
- NP: rešitev preverljiva v polinomskem času.
- NP-poln: v NP + vsi NP problemi se reducirajo nanj.
- NP-težak: vsaj tako težak kot NP-polni, ni nujno v NP.
- Algoritem ≠ problem. Slab algoritem ne dokazuje, da problem ni v P.

## Mini pasti

- Negativna utež -> ne Dijkstra.
- Različne uteži v grafu -> MST enoličen.
- Slovar z istim ključem tipično posodobi vrednost.
- Pri matrix-chain rezultat dimenzije ni odvisen od oklepajev, cena pa je.
- Pri `O(n)` velja tudi `O(n^2)`, ampak to ni tesna meja.
