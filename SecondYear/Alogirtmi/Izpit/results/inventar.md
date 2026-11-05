# Inventar gradiva za izpit APS2

Delovna mapa: `D:\Šola\FRI\SecondYear\Alogirtmi\Izpit`

## Struktura

- `Predavanja/` - 8 PDF datotek s prosojnicami.
- `Vaje/` - 13 PDF datotek z nalogami iz vaj.
- `Primeri/` - 13 slik primerov testov oziroma izpitnih pol.
- `results/` - mapa za pripravljene rešitve in učne povzetke.

## Predavanja

| Datoteka | Strani | Prepoznana tema |
|---|---:|---|
| `eaa263f7-76f0-4079-ad23-58eeea71b9a7.pdf` | 8 | Uvod v algoritme in podatkovne strukture, časovna zahtevnost |
| `c9a3298c-761d-49b8-8af4-7cbe31c6282c.pdf` | 34 | ADT, tabele, slovarji, seznami, preskočni seznami |
| `b8a0228c-5230-4ccc-be50-eee727f2bc1c.pdf` | 17 | Amortizirana analiza |
| `9789321c-64c3-45f0-a279-56d205df82ce.pdf` | 53 | Drevesa: dvojiška, iskalna, AVL, večsmerna, B/B+, TTF, rdeče-črna |
| `41e289b2-60c5-48f4-b5f7-1599164cb827.pdf` | 34 | Vrsta s prednostjo, zgoščene tabele, Bloomov filter, disjunktne množice |
| `4d7fa5ce-45de-4397-833e-bfead45e6b22.pdf` | 30 | Dinamično programiranje, verižno množenje matrik, nahrbtnik |
| `f9097b46-0b19-48a1-a360-83f8ae291bd8.pdf` | 14 | Razredi kompleksnosti, P/NP, redukcije |
| `2a7980df-6c3e-4fe2-aad2-fe12d98d310f.pdf` | 42 | Grafi: MST, barvanje, najkrajše poti, pretoki |

Opomba za grafe: po navodilu obdelam samo Prim, Kruskal, topološko urejanje, Bellman-Ford, Dijkstra in Welsh-Powell. Največji pretok preskočim.

## Vaje

| Datoteka | Strani | Prepoznana vsebina |
|---|---:|---|
| `b53d52a2-70e1-44c6-8a18-9a7b62821c3f.pdf` | 2 | Asimptotika, dokazovanje Θ/O, kopice |
| `0ffa67ac-647d-4550-bb25-a680dc598532.pdf` | 1 | Največje podzaporedje, osnovni algoritmi |
| `9770dd55-2718-4f70-ac34-2d59ff7bae55.pdf` | 1 | Amortizirana analiza sklada |
| `45d204a3-f745-457d-8df5-c302eb96e01d.pdf` | 1 | Java `List`, implementacije ADT |
| `c8049133-4b00-4352-81aa-4cdfd0330146.pdf` | 2 | Povezani seznami, obračanje seznama, preskočni seznami |
| `5689f7ec-5e26-42ba-99a0-793ba9ec6b15.pdf` | 2 | BST, min-kopica, izpisi, implementacija dreves |
| `b2990eb4-f36c-4dc1-8700-3972034d955d.pdf` | 1 | AVL vstavljanja/brisanja in rotacije |
| `4d82ebc6-7d38-43f5-ab39-0f85ed9d115f.pdf` | 1 | Zgoščene tabele, trki, naslavljanje |
| `7f6c1956-6ae3-4b18-a72d-f8618f87cf3c.pdf` | 1 | 0/1 nahrbtnik, dinamično programiranje |
| `89257b34-30a5-4be6-b8c3-6c640ee4bc11.pdf` | 1 | Vertex cover, kompleksnost |
| `8c28068f-2372-41bc-80be-cf5a94e52bcc.pdf` | 1 | Verižno množenje matrik |
| `f9310514-5098-4f50-b2ed-dc43d8277a0c.pdf` | 1 | Grafi: MST/najkrajše poti na uteženem neusmerjenem grafu |
| `f4daa6ad-596e-4de1-a2a5-75b4196ab4a0.pdf` | 2 | Grafi: najkrajše poti, topološko urejanje, štetje poti |

## Primeri

Slike v `Primeri/`:

- `20240610_100725.jpg`
- `20240620_100452.jpg`
- `20240620_100530.jpg`
- `20240620_100533.jpg`
- `20240620_100553.jpg`
- `image0.jpg`
- `IMG_5392.jpg`
- `IMG_5395.jpg`
- `IMG_5396.jpg`
- `PXL_20230619_080959115.jpg`
- `PXL_20230619_081001816.jpg`
- `PXL_20230619_081016189.jpg`
- `PXL_20230619_081022358.jpg`

## Tehnična opomba

- Originalnih PDF-jev ne spreminjam.
- Na PATH-u ni bilo najdenega `pdftotext`, `pdftoppm` ali `tesseract`.
- Uporabljen je priložen Codex Python runtime z `pypdf`, `PIL` in `reportlab`.
- Ker varno neposredno dopolnjevanje PDF-jev ni zagotovljeno, bodo rešitve praznih delov iz predavanj pripravljene kot spremljevalna datoteka v `results/`.
