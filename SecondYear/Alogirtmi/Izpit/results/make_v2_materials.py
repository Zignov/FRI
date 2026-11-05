from pathlib import Path
import re
import tempfile

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4 as PAGE_A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import generate_pdf_artifacts as base


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v2"
PDF = OUT / "pdf"
LECTURE_OUT = PDF / "predavanja_reseno_ob_straneh"
PDF.mkdir(parents=True, exist_ok=True)
LECTURE_OUT.mkdir(parents=True, exist_ok=True)

pdfmetrics.registerFont(TTFont("Study", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("Study-Bold", r"C:\Windows\Fonts\arialbd.ttf"))


def write_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


SUPER = r"""
# Super učni vodič APS2 - popravljena cram-ready verzija

Ta verzija je napisana tako, da lahko iz nje dejansko ponavljaš snov, ne samo bereš odgovore. Za vsak sklop glej: kaj je ideja, kdaj jo uporabiš, postopek, mini primer, tipične napake in preverjanje.

## 0. Kako se učiti iz tega vodiča

Najprej preleti A4 povzetek, potem ta vodič. Pri vsaki metodi naredi vsaj en ročni primer. APS2 naloge skoraj vedno ocenjujejo postopek: če napišeš samo rezultat, izgubiš točke tudi, ko je rezultat pravilen.

Red učenja:

1. Asimptotika + amortizacija.
2. Osnovne podatkovne strukture: tabele, slovarji, seznami, kopice.
3. Drevesa: BST, AVL, rdeče-črna, B/B+.
4. Zgoščevanje, Bloom, disjunktne množice.
5. DP: stopnice/Fibonacci, nahrbtnik, verižno množenje.
6. Grafi: samo Prim, Kruskal, topološko, Dijkstra, Bellman-Ford, Welsh-Powell.
7. P/NP in redukcije.

## 1. Asimptotična zahtevnost

### Kaj moraš znati

Znati moraš prepoznati red rasti algoritma in ga povezati z realno velikostjo podatkov. Na izpitu se pogosto pojavi vprašanje tipa: "Koliko časa traja algoritem, če je n = ... in procesor naredi ... operacij/s?"

### Definicije

- `O(f(n))`: algoritem ne raste hitreje kot `f(n)` do konstante. Zgornja meja.
- `Ω(f(n))`: algoritem raste vsaj tako hitro kot `f(n)`. Spodnja meja.
- `Θ(f(n))`: oboje hkrati. Tesna meja.

Primer: `3n^2 + 10n + 5 = Θ(n^2)`.

### Kako oceniš zanke

```text
for i = 1..n:
    for j = 1..n:
        O(1)
```

`n*n` ponovitev -> `Θ(n^2)`.

```text
for i = 1..n:
    for j = 1..i:
        O(1)
```

`1+2+...+n = n(n+1)/2 = Θ(n^2)`.

```text
i = 1
while i < n:
    i = 2*i
```

Število ponovitev je `log2 n`, zato `Θ(log n)`.

### Rekurzije

Tipične oblike:

- `T(n)=T(n/2)+O(1)` -> `O(log n)` (binarno iskanje).
- `T(n)=2T(n/2)+O(n)` -> `O(n log n)` (merge sort).
- `T(n)=T(n-1)+O(1)` -> `O(n)`.
- `T(n)=T(n-1)+T(n-2)+O(1)` -> eksponentno, če ne shranjuješ rezultatov.

### Ocena realnega časa

Postopek:

1. Dobi `f(n)`.
2. Če je dana konstanta `C`, računaj `C*f(n)`.
3. Deli s številom operacij/s.

Mini primer: `n=10^7`, `O(n^2)`, `C=1`, 1 GHz.

`n^2 = 10^14`; `10^14 / 10^9 = 10^5 s ≈ 27.8 h`.

### Tipične napake

- Pri polnem grafu pozabiš, da ima `Θ(n^2)` povezav.
- Zamenjaš `log n` in `n log n`.
- Iz tega, da poznaš počasen algoritem, sklepaš, da je problem težak. To ne drži.

## 2. ADT in osnovne podatkovne strukture

### ADT vs podatkovna struktura

ADT pove, katere operacije obstajajo in kaj pomenijo. Podatkovna struktura pove, kako je to implementirano.

Primer: ADT slovar ima `insert`, `find`, `delete`. Implementacija je lahko seznam, BST, zgoščena tabela, B-drevo ...

### Tabela

Tabela je dobra, ko poznaš indeks.

- `get(i)`: `O(1)`
- `put(i,x)`: `O(1)`
- vstavljanje na poljubno mesto: lahko `O(n)`, ker premikaš elemente

### Dinamična tabela

Problem: navadna tabela ima fiksno kapaciteto. Rešitev: ko je polna, naredimo večjo in prekopiramo elemente.

Najbolj smiselno: podvajanje velikosti.

Zakaj?

- povečanje za `+1`: kopiranje `1+2+...+n = Θ(n^2)`;
- podvajanje: skupno kopiranje manj kot `2n`, zato `insert` amortizirano `O(1)`.

Mini primer: kapacitete `1,2,4,8,16`. Do 16 elementov skupno prekopiraš `1+2+4+8=15` elementov.

### Tabela tabel

Struktura hrani elemente v urejenih tabelah `A_0, A_1, ...`, kjer je velikost `A_i = 2^i`.

Ideja: zasedene tabele ustrezajo bitom v binarnem zapisu števila elementov.

Primer: `n=13 = 8+4+1 = 1101_2`, zato so zasedene `A_3, A_2, A_0`.

Iskanje:

1. Pregledaš vse zasedene tabele.
2. V vsaki narediš binarno iskanje.
3. Tabel je `O(log n)`, iskanje v posamezni je `O(log n)`.
4. Skupaj `O(log^2 n)`.

Vstavljanje:

1. Narediš tabelo velikosti 1 z novim elementom.
2. Če je `A_0` prazna, jo postaviš tja.
3. Če je polna, zlij tabeli in prenos nesi v `A_1`.
4. Ponavljaš kot binarni števec.

Tipična napaka: pri vprašanju “koliko tabel potrebujemo” loči med številom zasedenih tabel in številom vseh nivojev do največjega.

## 3. Seznami in preskočni seznami

### Navaden povezan seznam

Iskanje je `O(n)`, tudi če je seznam urejen, ker ne moreš skočiti na sredino kot pri tabeli.

Vstavljanje na začetek je `O(1)`, vstavljanje na pravo urejeno mesto pa zahteva iskanje mesta.

### Popolnoma dopolnjen seznam

Dodamo kazalce `+1, +2, +4, +8, ...`.

Iskanje je podobno binarnemu zapisu: z največjim skokom določiš polovico, z naslednjim četrtino ...

Iskanje: `O(log n)`.

Problem: vstavljanje in brisanje lahko zahtevata popravljanje ogromno kazalcev -> `O(n)`.

### Preskočni seznam

Preskočni seznam reši problem s slučajno višino elementov.

Pri vstavljanju:

1. Element je vedno na nivoju 0.
2. Mečeš kovanec.
3. Dokler pada "uspeh", element dobi še en nivo.
4. Pri verjetnosti `1/2` ima malo elementov veliko višino.

Iskanje:

1. Začneš zgoraj levo.
2. Premikaš se desno, dokler naslednji element ni prevelik.
3. Potem greš dol.
4. Na dnu najdeš element ali mesto, kjer bi moral biti.

Pričakovano:

- iskanje `O(log n)`;
- vstavljanje `O(log n)`;
- prostor `O(n)`.

Mini primer z višinami:

```text
nivo 2: 7 -------- 8
nivo 1: 6 -- 7 -- 8 -- 9
nivo 0: 3 -- 5 -- 6 -- 7 -- 8 -- 9 -- 10
```

Pazi: `O(log n)` je tudi `O(n)`, ampak ni `Ω(n^2)`.

## 4. Slovarji, zgoščene tabele in Bloomov filter

### Slovar

Slovar hrani pare `(ključ, vrednost)`.

Če vstaviš isti ključ dvakrat, se v običajni definiciji vrednost posodobi. Če naloga eksplicitno obravnava duplikate kot elemente, potem jih hraniš po dogovoru naloge.

### Zgoščena tabela

Ideja: ključ `k` preslikamo v indeks `h(k)`.

Če je `m` velikost tabele:

- metoda deljenja: `h(k)=k mod m`;
- metoda množenja: `h(k)=(k*p) mod m`.

Dobro je, da je `m` ali `p` izbran tako, da razbije vzorce v ključih.

### Sovpadanje

Sovpadanje pomeni, da dva ključa padeta v isto celico.

#### Veriženje

V vsaki celici je koš: seznam, BST ali druga struktura.

Operacije:

1. Izračunaj `h(k)`.
2. Pojdi v koš.
3. Tam išči/vstavi/briši.

Pričakovani čas: `O(1+α)`, kjer je `α=n/m`.

#### Odprto naslavljanje

Vse je v isti tabeli. Če je celica polna, poskusiš naslednjo.

Linearno:

`h(k,i) = (h(k)+i) mod m`.

Postopek vstavljanja:

1. `i=0`.
2. Poglej `h(k,i)`.
3. Če je prosto, vstavi.
4. Sicer povečaj `i`.

Pazi:

- brisanje zahteva oznako `DELETED`;
- pri visoki zasedenosti število poskusov močno naraste;
- linearno naslavljanje povzroča gruče.

### Bloomov filter

Bloomov filter ima bitno tabelo in `k` zgoščevalnih funkcij.

Vstavljanje:

1. Za element izračunaš `h_1(x),...,h_k(x)`.
2. Ustrezne bite nastaviš na 1.

Preverjanje:

1. Izračunaš iste bite.
2. Če je vsaj eden 0 -> zagotovo NE.
3. Če so vsi 1 -> verjetno DA.

False positive je možen, false negative ne, dokler ne brišeš.

Brisanje:

- navaden Bloomov filter ne zna varno brisati;
- counting Bloom filter namesto bitov hrani števce.

## 5. Kopice in prioritetne vrste

### Prioritetna vrsta

ADT z operacijami:

- `min` ali `max`;
- `insert`;
- `deleteMin` ali `deleteMax`.

### Min-kopica

Lastnost: vsak starš je manjši ali enak otrokom.

Ni BST. Levo/desno poddrevo nista urejeni po BST pravilu.

Operacije:

- `min`: `O(1)`, koren;
- `insert`: dodaš na konec in popravljaš navzgor, `O(log n)`;
- `deleteMin`: koren zamenjaš z zadnjim, pobrišeš zadnjega, popravljaš navzdol, `O(log n)`;
- `heapify` celotne tabele: `O(n)`.

Pasti:

- največji element v min-kopici je nekje med listi, ne nujno na skrajnem desnem mestu;
- urejen izpis vseh elementov z zaporednim `deleteMin` traja `O(n log n)`.

## 6. Drevesa

### Dvojiško iskalno drevo (BST)

Pravilo:

- levo poddrevo ima manjše ključe;
- desno poddrevo ima večje ključe.

Iskanje, vstavljanje, brisanje: `O(h)`.

Minimum: pojdi čim bolj levo. Maksimum: čim bolj desno.

Če je drevo uravnoteženo, `h=O(log n)`. Če vstaviš že urejene elemente v navaden BST, lahko dobiš seznam in `h=O(n)`.

### AVL drevo

AVL je BST z dodatnim pogojem:

`|height(left)-height(right)| <= 1` za vsako vozlišče.

Po vstavljanju:

1. Vstavi kot v BST.
2. Hodi nazaj proti korenu.
3. Najdi prvo neuravnoteženo vozlišče.
4. Popravi z rotacijo.

Rotacije:

- LL: desna rotacija.
- RR: leva rotacija.
- LR: leva rotacija pri levem otroku, nato desna.
- RL: desna rotacija pri desnem otroku, nato leva.

Čas: vse osnovne operacije `O(log n)`.

### Rdeče-črno drevo

Je BST z barvami.

Pravila:

1. Vozlišče je rdeče ali črno.
2. Koren je črn.
3. Prazni listi NIL so črni.
4. Rdeče vozlišče nima rdečega otroka.
5. Vsaka pot od vozlišča do NIL lista ima enako število črnih vozlišč.

Vstavljanje:

1. Vstavi kot BST.
2. Novo vozlišče pobarvaj rdeče.
3. Če je starš črn, konec.
4. Če je starš rdeč, glej strica.
5. Rdeč stric -> prebarvanje.
6. Črn stric -> rotacija + prebarvanje.

AVL vs RČ:

- AVL je bolj uravnotežen -> hitrejše iskanje.
- RČ ima manj popravljanja -> dobro za veliko vstavljanj/brisanj.

### B-drevo in B+ drevo

Uporaba: baze in diski. Cilj je malo dostopov do diska, zato ima vozlišče več ključev.

B-drevo:

- ključi so v notranjih vozliščih in listih;
- vsi listi so na isti globini;
- ob prepolnem vozlišču se razcepi.

B+ drevo:

- podatki so v listih;
- notranja vozlišča so indeks;
- listi so pogosto povezani za hitro zaporedno branje.

## 7. Disjunktne množice

### Cilj

Vzdržujemo razbitje elementov na disjunktne množice.

Operacije:

- `makeSet(x)`: naredi množico `{x}`;
- `find(x)`: vrne predstavnika množice;
- `union(x,y)`: združi množici.

### Učinkovita izvedba

Gozd dreves, kjer vsak otrok kaže na starša, koren pa je predstavnik.

Optimizaciji:

- union by rank/size: manjše drevo pripni pod večje;
- path compression: pri `find` vse elemente na poti pripni direktno na koren.

Amortizirano skoraj konstantno: `O(α(n))`.

### Kdaj uporabiš

Kruskalov algoritem: preveriš, ali sta krajišči povezave že v isti komponenti.

## 8. Amortizirana analiza

### Ideja

Worst-case ene operacije je lahko drag, ampak to se ne zgodi pogosto. Amortizirana analiza ocenjuje povprečno ceno v najslabšem zaporedju operacij.

### Metoda vsote

Sešteješ realne cene vseh operacij in deliš s številom operacij.

Primer sklad z `multipop(k)`:

- vsak element je enkrat potisnjen;
- vsak element je največ enkrat odstranjen;
- skupno delo pri odstranjevanju je največ število vstavljanj;
- zato je amortizirano `O(1)`.

### Bankirska metoda

Poceni operacije plačajo malo več in pustijo kredit.

Primer sklad:

- `push` plača 2: 1 za takojšnje vstavljanje, 1 kredit na elementu;
- ko ga kasneje `pop` odstrani, porabi kredit.

### Potencialna metoda

Formula:

`a_i = c_i + Phi(D_i) - Phi(D_{i-1})`

Izbereš potencial, ki meri “shranjeno energijo” strukture.

Primer sklad: `Phi(D)=število elementov na skladu`.

## 9. Dinamično programiranje

### Kako ga prepoznaš

Naloga ima optimalno rešitev ali število možnosti in se da razbiti na podobne manjše naloge.

Ključni znaki:

- "največja/najmanjša vrednost";
- "na koliko načinov";
- "optimalna postavitev";
- "uporabi postopek iz predavanj".

### Standardni postopek

1. Definiraj stanje.
2. Zapiši rekurenco.
3. Zapiši začetne vrednosti.
4. Določi vrstni red računanja.
5. Če naloga zahteva predmete/pot/oklepaje, rekonstruiraj rešitev.

### Fibonacci in stopnice

Stopnice s koraki 1 ali 2:

`f(n)=f(n-1)+f(n-2)`.

Zakaj? Zadnji korak je dolg 1 ali 2.

Osnove:

- `f(0)=1`: en način, da ne narediš nič;
- `f(1)=1`.

### 0/1 nahrbtnik

Stanje:

`dp[i][w]` = najboljša vrednost s prvimi `i` predmeti in kapaciteto `w`.

Prehod:

Če predmeta ne vzamem:

`dp[i-1][w]`.

Če ga vzamem:

`dp[i-1][w-w_i] + v_i`.

Zato:

`dp[i][w]=max(dp[i-1][w], dp[i-1][w-w_i]+v_i)`.

Če `w_i>w`, predmeta ne moreš vzeti.

Preverjanje: končni odgovor je `dp[n][W]`, predmete najdeš z vračanjem nazaj po tabeli.

### Delni nahrbtnik

Če smeš predmete rezati, uporabi greedy:

1. Izračunaj `v_i/w_i`.
2. Uredi padajoče.
3. Jemlji cele predmete, zadnjega po potrebi odreži.

Pazi: isti greedy ne velja za 0/1 nahrbtnik.

### Verižno množenje matrik

Matrika `M_i` ima dimenzijo `d_{i-1} x d_i`.

Cena množenja `(a x b)*(b x c)` je `a*b*c`.

Stanje:

`c(i,j)` = najmanjša cena produkta `M_i...M_j`.

Rekurenca:

`c(i,j)=min_{i<=k<j}(c(i,k)+c(k+1,j)+d_{i-1}*d_k*d_j)`.

Osnova:

`c(i,i)=0`.

Računaš po diagonalah: najprej dolžina 1, potem 2, 3 ...

Pazi:

- rezultat produkta je isti ne glede na oklepaje;
- cena je lahko zelo različna;
- vrstni red matrik se ne sme poljubno menjati, razen če naloga eksplicitno sprašuje po veljavnem vrstnem redu iz danih matrik.

## 10. Grafi - samo zahtevane teme

Največji pretok preskoči.

### Predstavitev grafa

Matrika:

- prostor `O(n^2)`;
- hitro preverjanje, ali obstaja povezava `O(1)`;
- naštevanje sosedov je `O(n)`.

Seznam sosedov:

- prostor `O(n+m)`;
- naštevanje sosedov je učinkovito;
- preverjanje posamezne povezave je počasnejše, razen če uporabljaš slovarje.

### Minimalno vpeto drevo

MST obstaja za povezan neusmerjen utežen graf.

Lastnosti:

- ima `n-1` povezav;
- poveže vsa vozlišča;
- nima cikla;
- če so vse uteži različne, je MST enoličen.

### Prim

Uporaba: MST.

Postopek:

1. Začni v izbranem vozlišču.
2. Množica `T` vsebuje že izbrana vozlišča.
3. Med povezavami iz `T` v `V\T` izberi najcenejšo.
4. Dodaj novo vozlišče in povezavo.
5. Ponavljaj do `n-1` povezav.

Čas:

- matrika + linearno iskanje: `O(n^2)`;
- seznam sosedov + min-kopica: `O((n+m)log n)`.

### Kruskal

Postopek:

1. Uredi vse povezave po teži.
2. Začni s praznim gozdom.
3. Povezavo dodaj, če krajišči nista že v isti komponenti.
4. Komponente vodi z disjunktnimi množicami.
5. Ustavi se pri `n-1` povezavah.

Čas: `O(m log m)`.

### Topološko urejanje

Samo za DAG.

Kahnov algoritem:

1. Izračunaj vhodne stopnje.
2. V vrsto dodaj vozlišča z vhodno stopnjo 0.
3. Odstrani vozlišče, izpiši ga, zmanjšaj vhodne stopnje naslednikov.
4. Če ne izpišeš vseh vozlišč, graf ima cikel.

### Najkrajše poti v DAG

1. Topološko uredi graf.
2. `d[s]=0`, ostalo `∞`.
3. V topološkem vrstnem redu sproščaj izhodne povezave.

Čas: `O(n+m)`.

### Dijkstra

Uporaba: najkrajše poti, vse uteži nenegativne.

Postopek:

1. `d[s]=0`, ostalo `∞`.
2. Vsi so neobiskani.
3. Izberi neobiskano vozlišče z najmanjšim `d`.
4. Označi kot obiskano.
5. Sprosti vse izhodne povezave.

Sprostitev:

Če `d[u]+w(u,v)<d[v]`, potem `d[v]=d[u]+w(u,v)` in `pred[v]=u`.

Pazi: negativna povezava pomeni, da Dijkstra ni veljaven.

### Bellman-Ford

Uporaba:

- negativne uteži;
- preverjanje negativnega cikla.

Postopek:

1. `d[s]=0`, ostalo `∞`.
2. `n-1` krat sprosti vse povezave.
3. Še enkrat sprosti vse povezave.
4. Če se kaj izboljša, obstaja dosegljiv negativen cikel.

Čas: `O(nm)`.

### Welsh-Powell

Uporaba: hitro barvanje grafa.

Postopek:

1. Vozlišča uredi padajoče po stopnji.
2. Prvemu nepobarvanemu dodeli novo barvo.
3. Z isto barvo pobarvaj vsa naslednja vozlišča, ki niso sosednja nobenemu že pobarvanemu s to barvo.
4. Ponavljaj.

Pazi: rezultat ni nujno optimalen.

## 11. Kompleksnost P/NP

### Odločitveni in optimizacijski problemi

Odločitveni problem ima odgovor DA/NE.

Optimizacijski problem išče najboljšo rešitev po neki kriterijski funkciji.

Pogosto lahko optimizacijski problem rešuješ z več odločitvenimi vprašanji.

### P

Odločitveni problemi, ki jih znamo rešiti v polinomskem času.

### NP

Odločitveni problemi, kjer znamo pravilnost dane rešitve preveriti v polinomskem času.

Velja `P ⊆ NP`.

### Redukcije

Če problem `A` polinomsko prevedemo na problem `B`, potem je `B` vsaj tako težak kot `A`.

Trik za smer: lažji problem lahko rešujemo s težjim. Če znaš rešiti težjega, znaš rešiti tudi lažjega po prevedbi.

### NP-poln

Problem je NP-poln, če:

1. je v NP;
2. vsak problem iz NP se nanj polinomsko reducira.

Če najdeš polinomski algoritem za en NP-poln problem, potem `P=NP`.

### NP-težak

Vsaj tako težak kot NP-polni problemi. Ni nujno odločitveni in ni nujno v NP.

### Praktični pristopi

Za NP-težke/NP-polne probleme pogosto uporabljamo:

- hevristike;
- aproksimacijske algoritme;
- lokalno optimizacijo;
- backtracking;
- eksponentne algoritme za majhne vhode.

## 12. Kako pisati rešitve na izpitu

### DA/NE

Oblika:

```text
NE. Razlog: ...
Protiprimer: ...
```

Če je trditev formalno ohlapno resnična, zapiši tudi tesnejšo mejo. Primer: `O(log n)` je tudi `O(n^2)`, ampak prava tesna meja je `Θ(log n)`.

### Graf

Vedno pokaži tabelo:

- trenutna množica;
- kandidati;
- izbrana povezava/vozlišče;
- posodobljene razdalje/barve.

### DP

Če ni stanja in rekurence, rešitev ni dovolj dokumentirana.

Minimalno napiši:

1. `dp[...]` pomeni ...
2. Prehod ...
3. Osnova ...
4. Končni odgovor ...

### Drevesa

Po vsakem vstavljanju:

1. vstavi kot BST;
2. popravi najnižji neuravnotežen del;
3. nariši stanje.
"""


A4 = r"""
# Izpitni povzetek A4 - zgoščena popravljena verzija

## Asimptotika

`O` zgornja, `Ω` spodnja, `Θ` tesna. Ignoriraj konstante/nižje člene. `1+...+n=Θ(n^2)`. Poln graf: `m=Θ(n^2)`. 1 GHz ≈ `10^9` op/s. `log n < n < n log n < n^2 < n^3 < 2^n < n!`.

Rekurzije: `T(n)=T(n/2)+1 -> log n`; `2T(n/2)+n -> n log n`; `T(n-1)+1 -> n`; Fibonacci brez memo -> eksponentno.

## Tabele/ADT

ADT = operacije + pomen; PS = implementacija. Tabela `get/put O(1)`. Dinamična tabela s podvajanjem: `insert O(1)` amortizirano, ker kopiranja `1+2+4+...<2n`.

Tabela tabel: `A_i` velikosti `2^i`; zasedene tabele = biti v binarnem zapisu `n`; iskanje `O(log^2 n)`; vstavljanje kot binarni števec z zlivanjem.

## Seznami

Povezan seznam: iskanje `O(n)`. Urejenost sama ne pomaga pri kazalčnem seznamu. Preskočni seznam: nivo z meti kovanca; search/insert pričakovano `O(log n)`, prostor `O(n)`.

## Zgoščevanje

`h(k)=k mod m` ali `(k*p) mod m`. Faktor zasedenosti `α=n/m`. Veriženje: `O(1+α)`. Linearno: `h(k,i)=(h(k)+i) mod m`; brisanje z `DELETED`; pazi na gruče in polno tabelo. Slovar: isti ključ navadno posodobi vrednost.

Bloom: vstavi = prižgi `k` bitov; query: vsaj en 0 -> zagotovo NE, vsi 1 -> verjetno DA. False positive da, false negative ne. Brisanje: counting BF.

## Kopice / PQ

Min-kopica: starš <= otroci. `min O(1)`, `insert O(log n)`, `deleteMin O(log n)`, `heapify O(n)`. Kopica ni BST; max v min-kopici je med listi.

## Drevesa

BST: levo manjše, desno večje. `search/insert/delete O(h)`. Min = skrajno levo, max = skrajno desno.

AVL: `|hL-hR|<=1`; LL desna, RR leva, LR leva+desna, RL desna+leva. Vse `O(log n)`.

RČ: koren črn; rdeč nima rdečega otroka; vse poti imajo isto črno višino; novo vozlišče rdeče; rdeč stric -> prebarvanje, črn stric -> rotacija. AVL bolj iskalno strog, RČ manj rotacij.

B/B+: več ključev v vozlišču, vsi listi ista globina. B+ ima podatke v listih, notranja vozlišča indeks.

## Disjunktne množice

`makeSet/find/union`; gozd s parent kazalci; path compression + union by rank/size -> skoraj `O(1)`. Kruskal za cikle.

## Amortizacija

Vsota: skupno delo / št. operacij. Dvojiški števec: `n+n/2+...<2n -> O(1)`. Sklad/multipop: element enkrat noter, enkrat ven -> `O(1)`. Potencial: `a_i=c_i+Phi(D_i)-Phi(D_{i-1})`.

## DP

Vedno: stanje, prehod, osnove, vrstni red, rekonstrukcija.

Stopnice 1/2: `f(n)=f(n-1)+f(n-2)`, `f(0)=1`, `f(1)=1`.

0/1 nahrbtnik: `dp[i][w]=max(dp[i-1][w], dp[i-1][w-w_i]+v_i)` če `w_i<=w`; drugače `dp[i-1][w]`. Čas `O(nW)`.

Delni nahrbtnik: sort po `v/w`, jemlji greedy.

Matrix-chain: `M_i=d_{i-1} x d_i`; `c(i,j)=min_k(c(i,k)+c(k+1,j)+d_{i-1}d_kd_j)`, `c(i,i)=0`, po diagonalah, čas `O(n^3)`.

## Grafi

Matrika: prostor `O(n^2)`, edge check `O(1)`, sosedi `O(n)`. Seznam: prostor `O(n+m)`, sosedi hitro.

MST: `n-1` povezav, brez cikla, povezan. Različne uteži -> enoličen MST.

Prim: širi drevo z najcenejšo povezavo iz `T` v `V-T`; `O(n^2)` matrika, `O((n+m)log n)` heap.

Kruskal: sort edge po teži, dodaj če DSU-find različna; `O(m log m)`.

Topološko: samo DAG; indegree 0 v vrsto; odstranjuj; če ostane cikel. DAG shortest path: topo + relax `O(n+m)`.

Dijkstra: nenegativne uteži; vedno izberi neobiskano min `d`; relax. Negativna utež -> NE.

Bellman-Ford: negativne uteži OK; `n-1` krat relax vse edge; dodatni prehod zazna negativen cikel; `O(nm)`.

Welsh-Powell: vozlišča padajoče po stopnji; nova barva za prvo nepobarvano; z isto barvo barvaj nesosednja. Ni nujno optimalno.

Največji pretok: preskoči.

## P/NP

P: rešljivo polinomsko. NP: rešitev preverljiva polinomsko. `P⊆NP`. Redukcija `A <=p B` pomeni B vsaj tako težak kot A. NP-poln = v NP + vsi NP nanj. NP-težak = vsaj tako težak, ni nujno v NP. Algoritem ≠ problem.
"""


LECTURE_SOLUTIONS = {
    "eaa263f7-76f0-4079-ad23-58eeea71b9a7.pdf": {
        3: "Rešitve: čas nas zanima zato, da primerjamo algoritme neodvisno od računalnika. Razlika 1 ms/2 ms postane bistvena pri velikem številu ponovitev ali velikem n. V teoriji merimo število osnovnih korakov kot funkcijo velikosti vhoda, ne sekund.",
        6: "Primer O(n^2), n=10^7: približno 10^14 operacij. Če procesor naredi 10^9 op/s, je to 10^5 s ≈ 27.8 h. Eksponentna zahtevnost je problematična, ker se pri povečanju n za 1 delo pomnoži, ne samo prišteje.",
    },
    "c9a3298c-761d-49b8-8af4-7cbe31c6282c.pdf": {
        4: "Skladovna tabela: insert na konec je O(1), iskanje po vrednosti O(n). Urejena tabela: iskanje z bisekcijo O(log n), vstavljanje O(n), ker premikamo elemente. Boljša izbira je odvisna od tega, ali več iščemo ali več vstavljamo.",
        5: "Dinamično tabelo povečuj za faktor, tipično 2x. Če bi povečevali za +1, bi pri n vstavljanjih kopirali 1+2+...+n=Θ(n^2). Pri podvajanju je vseh kopiranj manj kot 2n, zato je insert amortizirano O(1).",
        8: "Za n elementov zasedene tabele ustrezajo enicam v binarnem zapisu n. Največ tabel/nivojev je O(log n). Iskanje: pregledamo O(log n) urejenih tabel, v vsaki bisekcija O(log n), skupaj O(log^2 n). Vstavljanje je kot binarni števec z zlivanjem tabel.",
        13: "Če dvakrat vstavimo isti ključ, slovar praviloma posodobi vrednost. Lahko imamo slovar samo s ključi; takrat je to množica. Slovar = preslikava ključ -> vrednost.",
        16: "Dva elementa z istim ključem: pri slovarju navadno drugi prepiše prvega; pri multiseznamski strukturi pa dovolimo duplikate. Vedno preveri, kaj naloga definira kot element.",
        18: "Urejenost kazalčnega seznama ne omogoči bisekcije, ker ne znamo skočiti na sredino. Še vedno se premikamo po kazalcih, zato iskanje ostane O(n), le v povprečju se lahko prej ustavimo.",
        21: "Rešitev za počasno iskanje: dodamo preskočne kazalce. Ideja je, da se po višjih nivojih premikamo z velikimi skoki, nato se spuščamo navzdol.",
        22: "S kazalci +2 prepolovimo število korakov: namesto približno n premikov potrebujemo približno n/2. Če dodamo še +4, +8, ... pridemo do logaritmičnega iskanja.",
        24: "Ustavimo se pri približno lg(n)-1, ker skok 2^i večji od dolžine seznama nima smisla. Število dodatnih povezav je n+n/2+n/4+...<2n, zato prostor ostane O(n).",
        25: "PDS ima search O(log n), insert/delete pa O(n), ker lahko nov element spremeni veliko preskočnih kazalcev. Preskočni seznam to reši z naključno izbiro nivoja elementa.",
        30: "Nivo elementa določimo z generatorjem/metom kovanca: nivo 0 ima vsak element; dokler pada uspeh, element promoviramo za en nivo. Pri p=1/2 je pričakovana višina O(log n).",
        31: "Vstavljanje: najprej poiščemo predhodnike na vseh nivojih, kjer bo novi element. Nato popravimo kazalce od nivoja 0 do izbrane višine elementa.",
        33: "k-ti element v preskočnem seznamu najdemo učinkovito, če povezave hranijo tudi dolžine/preskoke. Potem pri iskanju odštevamo velikosti preskokov podobno kot pri indeksiranju.",
    },
    "b8a0228c-5230-4ccc-be50-eee727f2bc1c.pdf": {
        9: "Razširjen sklad, metoda vsote: vsak element je enkrat potisnjen in največ enkrat odstranjen. Skupno delo v n operacijah je O(n), zato so push/pop/multipop amortizirano O(1).",
        10: "Dvojiški števec: bit 0 se spremeni n-krat, bit 1 n/2-krat, bit 2 n/4-krat ... Skupno < 2n sprememb, zato je povecaj() amortizirano O(1).",
        12: "Bankirsko za sklad: push plača 2 enoti; 1 za vstavljanje, 1 kredit ostane na elementu. Ko ga pop/multipop odstrani, odstranitev plača njegov kredit.",
        13: "Bankirsko za števec: ko bit nastavimo na 1, mu damo kredit za kasnejši preklop nazaj na 0. Drage operacije porabijo prej naložene kredite.",
        16: "Potencial za sklad: Phi(D)=število elementov. Push: realno 1, potencial +1 -> amortizirano 2. Pop: realno 1, potencial -1 -> amortizirano 0. Multipop skupno ostane O(1) amortizirano na operacijo zaporedja.",
        17: "Potencial za števec: Phi(D)=število enic. Pri povečanju se t enic spremeni v 0, ena ničla v 1. Realna cena t+1, sprememba potenciala 1-t, amortizirano 2.",
    },
    "41e289b2-60c5-48f4-b5f7-1599164cb827.pdf": {
        7: "Implementacija zgoščene tabele: tabela velikosti m + funkcija h(k). Idealno h enakomerno razprši ključe. Pri sovpadanju uporabimo veriženje ali odprto naslavljanje.",
        10: "Idealna zgoščevalna funkcija za poljubne prihodnje ključe ne obstaja. Cilj je enakomerna razpršitev za pričakovane podatke; zato izbiramo dobra m/p in včasih naključna semena.",
        11: "Veriženje: čas je O(1+dolžina koša). Pri enakomerni razpršitvi je pričakovana dolžina koša alfa=n/m, zato operacije pričakovano O(1+alfa).",
        12: "Odprto naslavljanje: vse hranimo v tabeli. Linearno h(k,i)=(h(k)+i) mod m. Potrebujemo zaporedje, ki lahko pregleda vsa mesta. Brisanje rešimo z oznako DELETED.",
        16: "Pri odprtem naslavljanju je pričakovano število poskusov odvisno od zasedenosti alfa. Ko je alfa blizu 1, se število poskusov močno poveča; zato tabelo povečamo prej.",
        22: "Bloom insert: za x izračunamo k indeksov in bite nastavimo na 1. Query: če je kateri od teh bitov 0 -> zagotovo NE; če so vsi 1 -> verjetno DA.",
        23: "Verjetnost napačnega DA raste z več elementi in manjšo tabelo. Približno: (1-e^{-kn/m})^k. Izberemo m in k glede na dovoljeno stopnjo false positive.",
        25: "Navaden Bloom ne zna varno brisati, ker bi z ugašanjem bitov pokvarili druge elemente. Rešitev: counting Bloom filter ali dodatna struktura za izbrisane.",
        26: "Counting Bloom filter: namesto bitov hrani števce. Insert poveča k števcev, delete jih zmanjša. Query s pragom: vsi relevantni števci >= phi -> verjetno DA.",
        31: "DSU s kazalcem na predstavnika: makeSet O(1), find O(1), union je lahko O(n), ker moramo prevezati vse elemente ene množice.",
        32: "DSU z gozdom: makeSet O(1), union pripne koren pod koren, find sledi staršem do korena. Brez optimizacij je find lahko O(n).",
        33: "Popravilo počasnega find: path compression + union by rank/size. Pri find vse elemente na poti pripnemo na koren; pri union manjše drevo pod večje.",
    },
    "4d7fa5ce-45de-4397-833e-bfead45e6b22.pdf": {
        5: "Navadni rekurzivni Fibonacci ima T(n)=T(n-1)+T(n-2)+O(1), zato eksponentno mnogo klicev. Razlog: iste vrednosti računamo večkrat.",
        11: "Množenje A(a x b) in B(b x c) potrebuje a*b*c skalarnih množenj. Produkt verige je možen, če se sosednje dimenzije ujemajo: M_i je d_{i-1} x d_i.",
        12: "Cena verige je odvisna od oklepajev. Rezultat ima isto dimenzijo, število množenj pa se lahko močno spremeni.",
        13: "Optimalni razcep Mi..Mj: izberemo k. Cena = c(i,k)+c(k+1,j)+d_{i-1}*d_k*d_j. Vzamemo minimum po vseh k.",
        14: "Naivna rekurzija preizkuša ogromno oklepajevanj, zato je eksponentna. Popravimo z memoizacijo ali tabulacijo.",
        15: "Memoizacija: tabela c(i,j) ima O(n^2) stanj, za vsako stanje preizkusimo O(n) delitev k. Čas O(n^3), prostor O(n^2).",
        16: "Bottom-up: c(i,i)=0. Računamo po dolžini intervala: najprej pari, nato trojice ... ker c(i,j) potrebuje krajše intervale.",
        23: "0/1 nahrbtnik: dp[i][w] = najboljša vrednost s prvimi i predmeti in kapaciteto w. Prehod: ne vzamem ali vzamem predmet i.",
        24: "Če w_i<=w: dp[i][w]=max(dp[i-1][w], dp[i-1][w-w_i]+v_i). Če ne, dp[i][w]=dp[i-1][w]. Čas O(nW).",
    },
    "9789321c-64c3-45f0-a279-56d205df82ce.pdf": {
        8: "BST operacije so O(h). Če je drevo uravnoteženo, h=O(log n); če je degenerirano v seznam, h=O(n). Minimum je skrajno levo, maksimum skrajno desno.",
        16: "AVL pogoj: za vsako vozlišče razlika višin poddreves največ 1. Po vstavljanju popravljamo prvo neuravnoteženo vozlišče z rotacijo.",
        17: "Rotacije: LL -> desna, RR -> leva, LR -> leva pri levem otroku nato desna, RL -> desna pri desnem otroku nato leva.",
        24: "B-drevo zmanjša višino tako, da ima vozlišče več ključev in več otrok. Uporabno za diske/baze, ker en dostop prebere blok z več ključi.",
        31: "B+ drevo: vsi podatki so v listih, notranja vozlišča so indeks. Dobro za razponska iskanja, ker so listi pogosto povezani.",
        39: "2-3-4/TTF drevo: vozlišče ima lahko 1,2,3 ključe in 2,3,4 otroke. Vsa listna vozlišča so na isti globini.",
        50: "RČ vstavljanje: novo vozlišče je rdeče. Če je starš črn, konec. Če sta starš in stric rdeča, prebarvaj. Če je stric črn, rotacija + prebarvanje.",
        51: "RČ brisanje je zahtevnejše, ker brisanje črnega vozlišča lahko poruši črno višino. Popravljamo s sorojencem, prebarvanji in rotacijami.",
        52: "AVL je bolj uravnotežen in boljši za veliko iskanj. RČ ima manj popravljanja pri spremembah in je pogost v knjižnicah Map/Set.",
    },
    "f9097b46-0b19-48a1-a360-83f8ae291bd8.pdf": {
        5: "Zahtevnost problema določamo po najboljšem znanem/obstoječem algoritmu za vse naloge problema, ne po enem izbranem algoritmu.",
        7: "NP: rešitev znamo preveriti v polinomskem času. Hamiltonov cikel: težko ga je najti, ampak dano zaporedje hitro preverimo.",
        8: "Redukcija A <=p B pomeni: če znamo rešiti B, znamo rešiti A. Zato je B vsaj tako težak kot A.",
        9: "NP-poln: problem je v NP in vsak NP problem se nanj polinomsko reducira. Polinomska rešitev enega NP-polnega problema bi dala P=NP.",
        10: "P=NP je odprto vprašanje. Splošno prepričanje je P != NP, ni pa dokazano.",
        11: "NP-polne rešujemo z eksponentnimi algoritmi za majhne n, hevristikami, aproksimacijami, lokalno optimizacijo ali backtrackingom.",
        13: "Zahtevnost algoritma ni zahtevnost problema. Eksponenten algoritem daje zgornjo mejo, ne dokaza, da problem ni v P.",
        14: "Največje podzaporedje: ker poznamo linearni algoritem, je problem v P. Ne smemo pa brez dokaza trditi, da boljši algoritem ne obstaja.",
    },
    "2a7980df-6c3e-4fe2-aad2-fe12d98d310f.pdf": {
        3: "Matrika: prostor O(n^2), preverjanje povezave O(1), naštevanje sosedov O(n). Seznam sosedov: prostor O(n+m), naštevanje sosedov hitro, preverjanje povezave počasnejše.",
        8: "Prim: z matriko in linearnim iskanjem minimuma O(n^2). S seznamom sosedov in min-kopico O((n+m)log n). Na vsakem koraku dodamo eno vozlišče in sprostimo njegove povezave.",
        9: "Kruskal: povezave hranimo v seznamu in jih uredimo po teži. Gozd komponent hranimo z disjunktnimi množicami, da hitro preverimo, ali povezava naredi cikel.",
        10: "Kruskal čas: urejanje povezav O(m log m), DSU operacije skoraj O(1) amortizirano. Skupaj O(m log m).",
        14: "Požrešno barvanje je odvisno od vrstnega reda. Welsh-Powell uporabi vrstni red padajočih stopenj in ni nujno optimalen, je pa hiter.",
        21: "Najkrajše poti v DAG: topološki vrstni red zagotovi, da je d[u] dokončen, ko obdelujemo u. Vsako povezavo sprostimo enkrat, čas O(n+m).",
        24: "Dijkstra velja samo za nenegativne uteži. Izbiramo neobiskano vozlišče z najmanjšo trenutno razdaljo; ta razdalja je potem dokončna.",
        28: "Bellman-Ford: n-1 krat sprostimo vse povezave. Po n-1 prehodih so najkrajše poti brez ciklov izračunane. Dodaten prehod zazna negativen cikel.",
        30: "Posplošeni Bellman-Ford lahko sprošča povezave, dokler se razdalje spreminjajo. Če se po n-1 iteracijah še spreminjajo, preveri negativen cikel.",
    },
}


def make_pdf(md_path: Path, title: str):
    base.make_pdf_from_markdown(md_path, PDF / (md_path.stem + ".pdf"), title)


def split_lines(text, max_chars=90):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        if len(current) + len(word) + 1 > max_chars:
            lines.append(current)
            current = word
        else:
            current = (current + " " + word).strip()
    if current:
        lines.append(current)
    return lines


def overlay_pdf(page_width, page_height, page_no, text, path):
    c = canvas.Canvas(str(path), pagesize=(page_width, page_height))
    box_h = min(145, max(82, 28 + 10 * len(split_lines(text, 92))))
    x = 28
    y = 28
    w = page_width - 56
    c.setFillColor(colors.Color(1, 1, 0.92, alpha=0.96))
    c.rect(x, y, w, box_h, stroke=0, fill=1)
    c.setStrokeColor(colors.darkorange)
    c.setLineWidth(1)
    c.rect(x, y, w, box_h, stroke=1, fill=0)
    c.setFillColor(colors.black)
    c.setFont("Study-Bold", 9)
    c.drawString(x + 8, y + box_h - 14, f"Rešitev / dopolnitev za stran {page_no}:")
    c.setFont("Study", 8)
    yy = y + box_h - 28
    for line in split_lines(text, 100):
        c.drawString(x + 8, yy, line)
        yy -= 9.5
        if yy < y + 8:
            break
    c.save()


def solution_page_pdf(page_no, text, path):
    doc = SimpleDocTemplate(str(path), pagesize=PAGE_A4, rightMargin=1.4*cm, leftMargin=1.4*cm, topMargin=1.2*cm, bottomMargin=1.2*cm)
    flow = [Paragraph(f"Podrobna rešitev za stran {page_no}", base.STYLES["h1"])]
    flow.extend(base.markdown_to_flowables("### Postopek\n\n" + text + "\n\n**Kako preverim:** rezultat primerjaj z definicijo na isti prosojnici; pri zahtevnosti preveri, kaj štejemo kot osnovni korak."))
    doc.build(flow)


def make_lecture_pdfs():
    for filename, page_map in LECTURE_SOLUTIONS.items():
        src = ROOT / "Predavanja" / filename
        if not src.exists():
            continue
        reader = PdfReader(str(src))
        writer = PdfWriter()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            for idx, page in enumerate(reader.pages, start=1):
                if idx in page_map:
                    w = float(page.mediabox.width)
                    h = float(page.mediabox.height)
                    ov = td / f"overlay_{idx}.pdf"
                    overlay_pdf(w, h, idx, page_map[idx], ov)
                    page.merge_page(PdfReader(str(ov)).pages[0])
                writer.add_page(page)
                if idx in page_map and len(page_map[idx]) > 220:
                    sp = td / f"solution_{idx}.pdf"
                    solution_page_pdf(idx, page_map[idx], sp)
                    for sol_page in PdfReader(str(sp)).pages:
                        writer.add_page(sol_page)
            out = LECTURE_OUT / f"v2_reseno_ob_strani_{filename}"
            with out.open("wb") as f:
                writer.write(f)


def make_dense_a4_pdf(md_path: Path):
    doc = SimpleDocTemplate(str(PDF / "izpitni_povzetek_A4_v2_gosto.pdf"), pagesize=PAGE_A4, rightMargin=0.75*cm, leftMargin=0.75*cm, topMargin=0.65*cm, bottomMargin=0.65*cm)
    flow = []
    lines = md_path.read_text(encoding="utf-8")
    # Reuse markdown conversion; small margins already make it denser.
    flow.extend(base.markdown_to_flowables(lines, title="Izpitni povzetek A4 v2"))
    doc.build(flow)


def make_one_page_a4_pdf():
    sections = [
        ("Asimptotika", [
            "O(g): obstajata c,n0, da f(n)<=c*g(n) za n>=n0. Omega je spodnja, Theta oboje.",
            "Polinomi: vzame se najvisja potenca. Logaritmi so pocasnejsi od n^eps, eksponenti hitrejsi od polinomov.",
            "Vsota zank: zaporedno sestejemo, gnezdeno pomnozimo, pri deljenju problema nastane log n nivojev.",
            "Master: aT(n/b)+f(n). Primerjaj f(n) z n^log_b(a).",
        ]),
        ("ADT in tabele", [
            "ADT opise operacije in obnasanje, implementacija pove strukturo in cene.",
            "Tabela: dostop O(1), iskanje neurejeno O(n), urejeno O(log n), vrivanje v sredino O(n).",
            "Dinamicna tabela z razsirjanjem x2 ima amortizirano vrivanje O(1). Potencial meri placano prihodnje kopiranje.",
            "Pri nalogi vedno povej, kateri indeks se premakne in koliko elementov se kopira.",
        ]),
        ("Seznami in skip list", [
            "Povezani seznam: vrivanje po znanem kazalcu O(1), iskanje O(n), slab cache locality.",
            "Dvojno povezan seznam omogoca brisanje znanega vozlisca brez iskanja predhodnika.",
            "Skip list: nivo vozlisca je nakljucen. Pricakovano iskanje, vstavljanje, brisanje O(log n).",
            "Postopek iskanja: desno dokler ne presezes kljuca, nato dol.",
        ]),
        ("Slovarji in hash", [
            "Dobra zgosc. funkcija enakomerno razprsi kljuce. Load factor alpha=n/m.",
            "Verizenje: pricakovano O(1+alpha). Odprto naslavljanje: sondiranje, brisanje potrebuje tombstone.",
            "Linearno sondiranje povzroca primary clustering; kvadratno/dvojno zmanjsata kopicenje.",
            "Bloom: vstavljanje nastavi k bitov, iskanje preveri vseh k bitov. Ni laznih negativnih, so lazni pozitivni.",
        ]),
        ("Kopice", [
            "Min/max heap je skoraj polno binarno drevo v tabeli. Stars (i-1)//2, otroka 2i+1,2i+2.",
            "insert: dodaj na konec in sift-up O(log n). delete-min/max: zamenjaj s koncem in sift-down O(log n).",
            "build-heap od spodaj je O(n), ker je veliko vozlisc blizu listov.",
            "Heapsort: build O(n), n izbrisov O(n log n), in-place, obicajno nestabilen.",
        ]),
        ("Drevesa", [
            "BST inorder izpise urejene kljuce. Cena je O(h); uravnotezeno h=O(log n), degenerirano h=O(n).",
            "AVL: visinska razlika najvec 1. Rotacije LL, RR, LR, RL popravijo lokalno neravnovesje.",
            "B-drevo: vec kljucev v vozliscu, vsi listi enako globoki, primerno za diske/bloke.",
            "Pri rotaciji napisi nov koren poddrevesa in prestavi srednje poddrevo na pravo stran.",
        ]),
        ("DSU", [
            "make-set, find, union. Union by rank/size + path compression da skoraj konstantno amortizirano ceno.",
            "Kruskal: sortiraj povezave po tezi, dodaj povezavo, ce find(u)!=find(v), nato union.",
            "Cikla ne dodamo, ker sta krajisci ze v isti komponenti.",
        ]),
        ("Dinamicno programiranje", [
            "Stanja morajo zajeti tocno dovolj zgodovine. Prehod gradi optimalno resitev iz manjsih podproblemov.",
            "Rod cutting: dp[i]=max(cena[j]+dp[i-j]). Hrani izbiro j za rekonstrukcijo.",
            "Nahrbtnik 0/1: dp[i][w]=max(dp[i-1][w], vred[i]+dp[i-1][w-teza[i]]).",
            "LCS: enaka znaka -> 1+dp[i-1][j-1], sicer max(dp[i-1][j],dp[i][j-1]).",
            "Pri izpitu zapisi stanje, zacetne pogoje, prehod, vrstni red racunanja in rekonstrukcijo.",
        ]),
        ("Grafi", [
            "BFS: nivoji, najkrajse poti v neutezenem grafu, O(V+E). Vrsta.",
            "DFS: casi vstop/izstop, topolosko urejanje, komponente, cikli. Sklad/rekurzija.",
            "Dijkstra: nenegativne utezi, prioritetna vrsta, O((V+E)logV). Bellman-Ford dopusca negativne utezi.",
            "Topoloski sort obstaja samo za DAG. Kahn: vozlisca z vhodno stopnjo 0.",
            "MST: Kruskal sortira povezave, Prim raste iz vozlisca. Oba uporabljata lastnost reza.",
        ]),
        ("P/NP in redukcije", [
            "P: resljivo polinomsko. NP: resitev preverimo polinomsko. NP-tezko: nanj reduciramo NP probleme.",
            "NP-polno: v NP in NP-tezko. Redukcija A <=p B pomeni: ce znam B, znam tudi A.",
            "Dokaz NP-polnosti: clan v NP, znan NP-poln problem, preslikava, dokaz ekvivalence.",
        ]),
        ("Pasti", [
            "Ne mesaj najkrajse poti in MST: MST ne daje najkrajsih poti med pari.",
            "Dijkstra odpove pri negativnih povezavah. DFS ne daje najkrajsih poti v splosnem grafu.",
            "Pri hashanju vedno navedi nacin resevanja trkov. Pri DP ne pozabi zacetnih pogojev.",
            "Rezultat brez postopka je nevaren: pri vsaki nalogi napisi invariant ali razlog pravilnosti.",
        ]),
    ]
    path = PDF / "izpitni_povzetek_A4_v2_ena_stran.pdf"
    width, height = PAGE_A4
    c = canvas.Canvas(str(path), pagesize=PAGE_A4)
    c.setTitle("Izpitni povzetek A4 v2 - ena stran")
    margin = 0.55 * cm
    gap = 0.32 * cm
    col_w = (width - 2 * margin - 2 * gap) / 3
    x_positions = [margin, margin + col_w + gap, margin + 2 * (col_w + gap)]
    col = 0
    y = height - margin
    c.setFont("Study-Bold", 10)
    c.drawString(margin, y, "APS2 izpitni povzetek v2 - ena A4 stran")
    y -= 12

    def new_col():
        nonlocal col, y
        col += 1
        y = height - margin
        if col > 2:
            c.showPage()
            col = 0
            y = height - margin

    for heading, bullets in sections:
        needed = 10 + 8 * sum(max(1, len(split_lines(b, 48))) for b in bullets)
        if y - needed < margin:
            new_col()
        x = x_positions[col]
        c.setFont("Study-Bold", 7.4)
        c.drawString(x, y, heading)
        y -= 8
        c.setFont("Study", 5.9)
        for bullet in bullets:
            for i, line in enumerate(split_lines(bullet, 48)):
                prefix = "- " if i == 0 else "  "
                c.drawString(x, y, prefix + line)
                y -= 6.4
                if y < margin:
                    new_col()
                    x = x_positions[col]
                    c.setFont("Study", 5.9)
        y -= 2.5
    c.save()


def make_status():
    status = """
# Status v2 popravka

Stare datoteke v `results/` in `results/pdf/` niso bile brisane.

Nova popravljena verzija je v `results_v2/`.

## Kaj je drugače

- Predavanja: ustvarjeni so novi PDF-ji, kjer je na relevantnih straneh dodan rumen okvir z rešitvijo/dopolnitvijo. Če je razlaga daljša, je takoj za isto stranjo dodana dodatna stran s postopkom. Rešitve niso več zbrane samo na koncu dokumenta.
- Super učni vodič: razširjen je iz kratkega seznama v dejanski učni dokument, ki pokrije ADT, tabele, seznam/preskočni seznam, slovarje, zgoščevanje, Bloom, kopice, drevesa, DSU, amortizacijo, DP, grafe in P/NP.
- A4 povzetek: dodanih je več formul, postopkov, pasti in pogojev uporabe algoritmov.

## Pomembna omejitev

Brez ročnega urejevalnika PDF strani in brez renderiranega preverjanja vsake prosojnice ne morem zanesljivo tipkati v točno isti prazen pravokotnik na vsaki prosojnici. Zato je v2 narejen varno: rešitev je na isti strani v vidnem okvirju ali takoj za njo, brez spremembe izvornega besedila naloge.
"""
    write_text(OUT / "status_v2.md", status)
    make_pdf(OUT / "status_v2.md", "Status v2 popravka")


def main():
    write_text(OUT / "super_ucni_vodic_v2.md", SUPER)
    write_text(OUT / "izpitni_povzetek_A4_v2.md", A4)
    make_pdf(OUT / "super_ucni_vodic_v2.md", "Super učni vodič APS2 v2")
    make_pdf(OUT / "izpitni_povzetek_A4_v2.md", "Izpitni povzetek A4 v2")
    make_dense_a4_pdf(OUT / "izpitni_povzetek_A4_v2.md")
    make_one_page_a4_pdf()
    make_lecture_pdfs()
    make_status()


if __name__ == "__main__":
    main()
