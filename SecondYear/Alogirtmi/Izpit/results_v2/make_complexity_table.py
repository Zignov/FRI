# -*- coding: utf-8 -*-
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v2"
PDF = OUT / "pdf"
PDF.mkdir(parents=True, exist_ok=True)

FONT = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
for name, file in [("Study", r"C:\Windows\Fonts\arial.ttf"), ("Study-Bold", r"C:\Windows\Fonts\arialbd.ttf")]:
    p = Path(file)
    if p.exists():
        pdfmetrics.registerFont(TTFont(name, str(p)))
        if name == "Study":
            FONT = name
        else:
            FONT_BOLD = name


SOURCE_MAP = {
    "P0": "Predavanja/eaa263f7-...: uvod v casovno zahtevnost, strani 4-7",
    "P1": "Predavanja/c9a3298c-...: ADT, tabele, seznami, preskocni seznam, strani 5-34",
    "P2": "Predavanja/b8a0228c-...: amortizirana analiza, strani 8-17",
    "P3": "Predavanja/41e289b2-...: kopice, slovarji, zgoscevanje, Bloom, DSU, strani 4-33",
    "P4": "Predavanja/9789321c-...: BST, AVL, B/B+, TTF, rdece-crna drevesa, strani 7-52",
    "P5": "Predavanja/4d7fa5ce-...: dinamicno programiranje, matrike, nahrbtnik, strani 5-30",
    "P6": "Predavanja/2a7980df-...: grafi, MST, barvanje, najkrajse poti, pretoki, strani 3-42",
    "P7": "Predavanja/f9097b46-...: P/NP in primeri algoritmov, strani 5-14",
    "V": "Vaje/*.pdf: naloge, kjer je zahtevnost eksplicitno zahtevana",
}


ROWS = [
    # Splošno
    ("Splošne oblike", "Konstanten postopek", "ena neposredna operacija", "O(1)", "neodvisno od n", "P0"),
    ("Splošne oblike", "Logaritemski postopek", "razpolavljanje / sprehod po uravnotezeni visini", "O(log n)", "osnova logaritma pri O ni pomembna", "P0"),
    ("Splošne oblike", "Linearen postopek", "en pregled vseh elementov", "O(n)", "tipicno ena zanka po vhodu", "P0"),
    ("Splošne oblike", "Linearno-logaritemski postopek", "deli-in-vladaj ali sortiranje s primerjavami", "O(n log n)", "npr. mergesort/quicksort povprecno, max podzaporedje D&V", "P7,V"),
    ("Splošne oblike", "Kvadraticen postopek", "dve gnezdeni zanki", "O(n^2)", "npr. izboljsana groba sila, mehurcki", "P0,P7,V"),
    ("Splošne oblike", "Kubičen postopek", "tri gnezdene zanke", "O(n^3)", "npr. mnozenje matrik, Floyd-Warshall, groba sila max podzaporedja", "P0,P5,P6,P7,V"),
    ("Splošne oblike", "Eksponenten postopek", "pregled kombinacij / backtracking", "O(2^n), O(k^n)", "uporabno samo za majhne n", "P7,P6,P5"),
    ("Splošne oblike", "Faktorialen postopek", "pregled permutacij", "O(n!)", "se slabse od eksponentnega za velike n", "P0"),
    ("Splošne oblike", "Polinomski cas", "razred P", "n^c za konst. c", "problem je 'lahek' v smislu teorije kompleksnosti", "P7"),
    ("Splošne oblike", "Psevdopolinomski cas", "odvisnost od numericne kapacitete", "O(nV)", "pri 0/1 nahrbtniku V ni nujno velikost zapisa", "P5"),

    # Tabele
    ("Tabele", "Navadna tabela", "get(i), put(i,x), length", "O(1)", "indeks neposredno pove naslov", "P1,V"),
    ("Tabele", "Navadna tabela", "init(n)", "O(n)", "ce inicializiramo vseh n mest", "P1"),
    ("Tabele", "Neurejena tabela", "find(x)", "O(n)", "v najslabsem primeru pregledamo vse", "P1,V"),
    ("Tabele", "Neurejena tabela", "insert na konec, ce je prostor", "O(1)", "brez preverjanja podvajanja", "P1,V"),
    ("Tabele", "Neurejena tabela", "delete(x)", "O(n)", "najprej iskanje; premik ali zamenjava je najvec linearen del", "P1,V"),
    ("Tabele", "Urejena tabela", "find(x)", "O(log n)", "binarno iskanje", "P1"),
    ("Tabele", "Urejena tabela", "insert(x)", "O(n)", "najdemo mesto in premaknemo elemente", "P1"),
    ("Tabele", "Urejena tabela", "delete(x)", "O(n)", "po brisanju premikamo elemente", "P1"),
    ("Tabele", "Dinamicna tabela / ArrayList", "append/add na konec", "amort. O(1), najslabse O(n)", "razsiritev kopira elemente", "P1,P2,V"),
    ("Tabele", "Dinamicna tabela / ArrayList", "get(i)", "O(1)", "neposreden indeks", "V"),
    ("Tabele", "Dinamicna tabela / ArrayList", "addFirst ali insert v sredino", "O(n)", "premik elementov", "V"),
    ("Tabele", "Dinamicna tabela / ArrayList", "remove(i)", "O(n)", "premik elementov za zapolnitev luknje", "V"),
    ("Tabele", "Tabela tabel / cascading arrays", "find(x)", "O(log^2 n)", "pregled do log n urejenih tabel, v vsaki binarno iskanje", "P1,V"),
    ("Tabele", "Tabela tabel / cascading arrays", "insert(x)", "amort. O(log n), najslabse O(n)", "zlivanje tabel deluje kot binarni stevec", "P1,V"),
    ("Tabele", "Tabela tabel / cascading arrays", "delete(x), enostavna rekonstrukcija", "O(n)", "po odstranitvi lahko strukturo zgradimo nazaj", "V"),
    ("Tabele", "Tabela tabel / cascading arrays", "najdi minimum", "O(log n)", "preverimo minimum vsake neprazne urejene tabele", "V"),

    # Seznami
    ("Seznami", "Povezan seznam / LinkedList", "insert na zacetek, addFirst", "O(1)", "spremenimo nekaj kazalcev", "P1,V"),
    ("Seznami", "Povezan seznam / LinkedList", "get(i), find(x)", "O(n)", "zaporedni sprehod", "P1,V"),
    ("Seznami", "Povezan seznam / LinkedList", "delete po kljucu", "O(n)", "najprej moramo najti element/predhodnika", "P1,V"),
    ("Seznami", "Povezan seznam / LinkedList", "delete znanega vozlisca v dvojno povezanem seznamu", "O(1)", "ce ze imamo referenco na vozlisce", "P1,V"),
    ("Seznami", "Urejen povezan seznam", "find/insert/delete", "O(n)", "urejenost ne odpravi zaporednega sprehoda", "P1"),
    ("Seznami", "Popolnoma dopolnjen seznam (PDS)", "find", "O(log n)", "dodatne povezave omogocajo skoke", "P1"),
    ("Seznami", "Popolnoma dopolnjen seznam (PDS)", "insert/delete", "O(n)", "v najslabsem primeru popravljamo veliko povezav", "P1"),
    ("Seznami", "Preskocni seznam", "find", "pričakovano O(log n), najslabse O(n)", "verjetnostna struktura", "P1,V"),
    ("Seznami", "Preskocni seznam", "insert/delete", "pričakovano O(log n), najslabse O(n)", "iskanje mesta + popravljanje do log n referenc v pricakovanju", "P1,V"),
    ("Seznami", "Deterministic skip list", "find/insert/delete", "O(log n)", "omenjen kot boljsa deterministična varianta", "P1"),
    ("Seznami", "Pretvorba urejenega seznama v skip-list", "build", "O(n)", "ce nivoje zgradimo po znanem vzorcu brez ponovnega iskanja", "V"),

    # Sklad in amortizacija
    ("Amortizacija", "Razsirjen sklad", "push/pop", "O(1)", "obicajni skladovni operaciji", "P2,V"),
    ("Amortizacija", "Razsirjen sklad", "multipop(k)", "O(k)", "realna cena je stevilo pobrisanih elementov", "P2,V"),
    ("Amortizacija", "Razsirjen sklad", "zaporedje push/pop/multipop", "amort. O(1) na operacijo", "vsak element je dodan in odstranjen najvec enkrat", "P2,V"),
    ("Amortizacija", "Razsirjen sklad", "multipush(k) kot ena operacija", "O(k), ne amort. O(1)", "ena operacija lahko vnese k novih elementov", "V"),
    ("Amortizacija", "Binarni stevec", "povecaj", "amort. O(1), najslabse O(log n) ali O(b)", "b je stevilo bitov; bit se ne obraca preveckrat", "P2,V"),
    ("Amortizacija", "Binarni stevec", "povecaj + zmanjsaj poljubno", "najs. O(b) na operacijo", "izmenjavanje lahko vedno obraca veliko bitov", "V"),
    ("Amortizacija", "Operacija s ceno i pri i=2^k, sicer 1", "n operacij", "skupaj O(n), amort. O(1)", "vsota potenc dvojke do n je <2n", "V"),

    # Slovarji in zgoscevanje
    ("Slovarji", "Slovar z neurejenim seznamom", "insert", "O(1) ali O(n)", "O(1) brez preverjanja duplikata, O(n) s preverjanjem", "P1,P3"),
    ("Slovarji", "Slovar z neurejenim seznamom", "find/delete", "O(n)", "zaporedni pregled", "P1,P3"),
    ("Slovarji", "Slovar z urejeno tabelo", "find", "O(log n)", "binarno iskanje", "P1,P3"),
    ("Slovarji", "Slovar z urejeno tabelo", "insert/delete", "O(n)", "premikanje elementov", "P1,P3"),
    ("Slovarji", "Zgoscena tabela z verizenjem", "find/insert/delete", "prič. O(1+alpha), najslabse O(n)", "alpha=n/m; v kosu je seznam", "P3,V"),
    ("Slovarji", "Zgoscena tabela z odprtim naslavljanjem", "find/insert/delete", "prič. O(1), najslabse O(n)", "velja pri dobri funkciji in majhnem alpha; brisanje rabi tombstone", "P3,V"),
    ("Slovarji", "Linearno sondiranje", "poskus iskanja prostega mesta", "do O(m)", "v najslabsem primeru pregled tabele; clustering", "P3,V"),
    ("Slovarji", "Bloomov filter", "insert/find", "O(k), ce je k konst. O(1)", "k zgoscevalnih funkcij; ni laznih negativnih", "P3,V"),
    ("Slovarji", "Counting Bloom filter", "insert/find/delete", "O(k)", "stevci omogocijo brisanje", "P3"),

    # Kopice
    ("Kopice / prioritetne vrste", "Dvojiska kopica", "min/max", "O(1)", "koren kopice", "P3,V"),
    ("Kopice / prioritetne vrste", "Dvojiska kopica", "insert", "O(log n)", "sift-up po visini", "P3,V"),
    ("Kopice / prioritetne vrste", "Dvojiska kopica", "deleteMin/deleteMax", "O(log n)", "zamenjava s koncem + sift-down", "P3,V"),
    ("Kopice / prioritetne vrste", "Dvojiska kopica", "decreaseKey/increaseKey", "O(log n)", "popravljanje po poti", "P3"),
    ("Kopice / prioritetne vrste", "Dvojiska kopica", "heapify", "O(h), najvec O(log n)", "h je visina poddrevesa", "V"),
    ("Kopice / prioritetne vrste", "Dvojiska kopica", "buildHeap", "O(n)", "od spodaj navzgor; vsota visin je linearna", "V"),
    ("Kopice / prioritetne vrste", "Heapsort / izpis vseh v urejenem vrstnem redu", "n krat deleteMin", "O(n log n)", "z min-kopico splosno ne gre O(n)", "V"),
    ("Kopice / prioritetne vrste", "Fibonaccijeva kopica", "insert, decreaseKey", "amort. O(1)", "teoreticno bolje kot dvojiska", "P3"),
    ("Kopice / prioritetne vrste", "Fibonaccijeva kopica", "deleteMin/delete", "amort. O(log n)", "zaporedje v insert/decrease in b delete: O(v+b log n)", "P3"),
    ("Kopice / prioritetne vrste", "Struktura: vstavi, izbriši najstarejsega, min", "insert O(log n), deleteOldest O(log n), min O(1)", "kombinacija prioritetne vrste in reda vstavljanja", "V"),

    # DSU
    ("Disjunktne množice", "Kazalec na predstavnika", "makeSet", "O(1)", "nov element kaze nase", "P3,V"),
    ("Disjunktne množice", "Kazalec na predstavnika", "find", "O(1)", "predstavnik je shranjen neposredno", "P3,V"),
    ("Disjunktne množice", "Kazalec na predstavnika", "union", "O(n)", "treba je popraviti predstavnika elementom ene mnozice", "P3,V"),
    ("Disjunktne množice", "Gozd brez optimizacij", "makeSet/union korenov", "O(1)", "ce sta korena ze znana", "P3,V"),
    ("Disjunktne množice", "Gozd brez optimizacij", "find", "O(h), najslabse O(n)", "sprehod do korena", "P3,V"),
    ("Disjunktne množice", "Union by rank/size + path compression", "find/union", "amort. O(alpha(n))", "alpha je inverzna Ackermannova funkcija, prakticno konstanta", "P3,V"),

    # Drevesa
    ("Drevesa", "Dvojiško drevo", "pregled preorder/inorder/postorder", "O(n)", "obiscemo vsako vozlisce", "P4"),
    ("Drevesa", "BST", "find/insert/delete", "Θ(h)", "h je visina drevesa", "P4,V"),
    ("Drevesa", "BST", "find/insert/delete, najslabse", "O(n)", "izrojeno drevo je veriga", "P4,V"),
    ("Drevesa", "BST", "find/insert/delete, uravnotezeno", "O(log n)", "ce je h=O(log n)", "P4,V"),
    ("Drevesa", "BST", "min/max/successor", "O(h)", "sprehod po levi/desni poti", "P4,V"),
    ("Drevesa", "Rotacija", "leva/desna rotacija", "O(1)", "lokalno prevezovanje kazalcev", "P4"),
    ("Drevesa", "AVL", "visina", "Θ(log n)", "zaradi pogoja uravnotezenosti", "P4"),
    ("Drevesa", "AVL", "find/insert/delete", "O(log n)", "sprehod po visini + rotacije", "P4,V"),
    ("Drevesa", "AVL", "posamezna rotacija", "O(1)", "insert potrebuje konst. st. rotacij, delete lahko vec, skupaj O(log n)", "P4"),
    ("Drevesa", "B-drevo", "find/search", "O(log n) oziroma O(log_b n) nivojev", "b je razvejanost; pri fiksnem b pisemo O(log n)", "P4"),
    ("Drevesa", "B-drevo", "insert/delete", "O(h)=O(log n)", "split/merge se lahko ponovi do korena", "P4"),
    ("Drevesa", "B+ drevo", "find/insert/delete", "O(log n)", "enaka visinska ideja kot B-drevo", "P4,V"),
    ("Drevesa", "B+ drevo", "range query z k izpisi", "O(log n + k)", "najdemo prvi list, nato sledimo povezavam listov", "P4"),
    ("Drevesa", "TTF / 2-3-4 drevo", "find/insert/delete", "O(log n)", "poseben primer B-drevesa z b=4", "P4"),
    ("Drevesa", "Rdece-crno drevo", "visina", "O(log n)", "povezava s TTF drevesi", "P4"),
    ("Drevesa", "Rdece-crno drevo", "find/insert/delete", "O(log n)", "BST sprehod + lokalna popravljanja/prebarvanja", "P4"),

    # DP, matrike, nahrbtnik
    ("DP", "Fibonacci, navadna rekurzija", "fib(n)", "eksponentno, O(2^n) / Θ(phi^n)", "podprobleme racuna znova", "P5"),
    ("DP", "Fibonacci z memoizacijo", "fibM(n)", "Θ(n)", "n sestevanj in shranjevanj", "P5"),
    ("DP", "Fibonacci s tabeliranjem", "fibT(n)", "Θ(n)", "ena zanka", "P5"),
    ("DP", "Mnozenje dveh matrik", "a x b krat b x c", "O(a*b*c)", "za kvadratni n x n matriki je O(n^3)", "P0,P5,V"),
    ("DP", "Verizno mnozenje matrik", "groba sila po oklepajih", "eksponentno", "stevilo postavitev oklepajev hitro narasca", "P5"),
    ("DP", "Verizno mnozenje matrik", "memoizacija / bottom-up DP", "O(n^3)", "O(n^2) stanj, do O(n) prehodov na stanje", "P5"),
    ("DP", "Verizno mnozenje matrik", "rekonstrukcija oklepajev", "O(n)", "ce hranimo optimalni k za vsako stanje", "P5"),
    ("DP", "Nahrbtnik z rezanjem (fractional)", "požrešno po c_i/v_i", "O(n log n)", "sortiranje predmetov je glavni del", "P5"),
    ("DP", "0/1 nahrbtnik", "pregled vseh podmnozic", "O(2^n)", "vsak predmet vzamemo ali ne", "P5"),
    ("DP", "0/1 nahrbtnik, tabela po kapaciteti", "DP", "O(nV)", "V je kapaciteta; psevdopolinomsko", "P5"),
    ("DP", "0/1 nahrbtnik, stopniscna/vogalna predstavitev", "dodajanje predmeta", "odvisno od st. vogalov, worst O(2^n)", "v praksi brisemo dominirane vogale", "P5"),

    # Najvecje podzaporedje in sortiranje
    ("Algoritmi iz vaj", "Najvecje podzaporedje", "groba sila", "O(n^3)", "vse intervale in vsote racunamo neposredno", "P7,V"),
    ("Algoritmi iz vaj", "Najvecje podzaporedje", "izboljsana groba sila", "O(n^2)", "vsote podaljsujemo sproti", "P7,V"),
    ("Algoritmi iz vaj", "Najvecje podzaporedje", "deli in vladaj", "O(n log n)", "dve polovici + presek v O(n)", "P7,V"),
    ("Algoritmi iz vaj", "Najvecje podzaporedje", "Kadanov algoritem", "O(n)", "en prehod", "P7,V"),
    ("Algoritmi iz vaj", "Urejanje z mehurcki", "sort", "O(n^2)", "primer iz kompleksnosti problemov", "P7"),
    ("Algoritmi iz vaj", "Hitro urejanje", "sort", "povp. O(n log n), najs. O(n^2)", "v prosojnicah omenjeno O(n log n) kot dober algoritem", "P7"),
    ("Algoritmi iz vaj", "Radix sort", "sort", "O(n) pri omejeni dolzini kljucev", "linearno v stevilu elementov za fiksno stevilo stevk", "P7"),
    ("Algoritmi iz vaj", "Iskanje k najmanjsih", "linearni izbor / median-of-medians", "O(n)", "v vajah zahtevana linearna resitev", "V"),

    # Grafi
    ("Grafi", "Matrika sosednosti", "prostor", "O(V^2)", "hitro vprasanje o povezavi, drago za redke grafe", "P6"),
    ("Grafi", "Matrika sosednosti", "ali je (u,v) povezava", "O(1)", "neposreden vpogled v matriko", "P6"),
    ("Grafi", "Matrika sosednosti", "nastej sosede vozlisca", "O(V)", "pregled celotne vrstice", "P6"),
    ("Grafi", "Seznam sosedov", "prostor", "O(V+E)", "boljse za redke grafe", "P6"),
    ("Grafi", "Seznam sosedov", "nastej sosede v", "O(deg(v))", "sprehod po seznamu sosedov", "P6"),
    ("Grafi", "Seznam sosedov", "ali je (u,v) povezava", "O(deg(u))", "ali O(1) z dodatno hash strukturo", "P6"),
    ("Grafi", "BFS", "pregled / najkrajse poti v neutezenem grafu", "O(V+E)", "z adjacency list; z matriko O(V^2)", "P6"),
    ("Grafi", "DFS", "pregled / komponente / cikli", "O(V+E)", "z adjacency list; z matriko O(V^2)", "P6"),
    ("Grafi", "Topološko urejanje", "sort DAG", "O(V+E)", "DFS ali Kahn", "P6"),
    ("Grafi", "Najkrajse poti v DAG", "topološko urejanje + relaksacije", "O(V+E)", "velja za aciklicen graf", "P6"),
    ("Grafi", "Prim", "preprosta izvedba z matriko/tabelo key", "O(V^2)", "vsakic iskanje najmanjsega key", "P6"),
    ("Grafi", "Prim", "adjacency list + dvojiska kopica", "O((V+E) log V)", "decreaseKey v kopici", "P3,P6"),
    ("Grafi", "Prim", "Fibonaccijeva kopica", "O(E + V log V)", "teoreticno boljsi decreaseKey", "P3,P6"),
    ("Grafi", "Kruskal", "MST", "O(E log E)", "sortiranje povezav + DSU", "P3,P6"),
    ("Grafi", "Kruskal z DSU optimizacijami", "union/find del", "O(E alpha(V))", "sortiranje ponavadi dominira", "P3,P6"),
    ("Grafi", "Pozresno barvanje", "barvanje v danem vrstnem redu", "O(V+E) do O(V^2)", "odvisno od predstavitve in preverjanja sosedov", "P6"),
    ("Grafi", "Barvanje s sestopanjem", "k-barvanje", "O(k^V)", "preiskovanje vseh dodelitev barv", "P6"),
    ("Grafi", "Dijkstra", "preprosta izvedba", "O(V^2)", "nenegativne utezi", "P6"),
    ("Grafi", "Dijkstra", "dvojiska kopica", "O((V+E) log V)", "najpogostejsa ocena", "P3,P6"),
    ("Grafi", "Dijkstra", "Fibonaccijeva kopica", "O(E + V log V)", "teoreticno boljsa za veliko decreaseKey", "P3,P6"),
    ("Grafi", "Bellman-Ford", "en izvor", "O(VE)", "dopusca negativne utezi, zazna negativen cikel", "P6"),
    ("Grafi", "Posploseni Bellman-Ford", "vsi pari poti", "O(V^4)", "za vsak h in vsak par preverjamo vmesna vozlisca", "P6"),
    ("Grafi", "Floyd-Warshall", "vsi pari najkrajsih poti", "O(V^3)", "tri gnezdene zanke po k,i,j", "P6"),
    ("Grafi", "Ford-Fulkerson", "najvecji pretok", "O(E * |f*|) pri celih kapacitetah", "stevilo izboljsav je odvisno od izbranih poti/kapacitet", "P6"),
    ("Grafi", "Iskanje nezasicene poti v pretoku", "ena iteracija", "O(V+E)", "BFS/DFS po residualnem omrezju", "P6"),

    # Kompleksnost problemov
    ("P/NP", "Preverjanje certifikata za NP problem", "verify", "polinomsko", "to je pogoj za razred NP", "P7"),
    ("P/NP", "NP-polni problemi", "znani splosni algoritmi", "pogosto eksponentno", "ne poznamo polinomskih algoritmov", "P7"),
    ("P/NP", "Polinomska redukcija A <=p B", "pretvorba primerka", "polinomsko", "ce znamo B, znamo A", "P7"),
]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write_markdown():
    md = []
    md.append("# Tabela casovnih zahtevnosti iz PDF gradiv\n")
    md.append("Tabela zdruzuje zahtevnosti, ki so eksplicitno omenjene ali neposredno zahtevane v predavanjih in vajah. Pri standardnih algoritmih je dodana obicajna ocena pod pogoji, ki so zapisani v stolpcu `Pogoji / opomba`.\n")
    md.append("## Legenda\n")
    md.append("- `n`: stevilo elementov.\n- `V`: stevilo vozlisc grafa ali kapaciteta nahrbtnika; pri grafih uporabljam tudi `|V|`, v tabeli zaradi berljivosti samo `V`.\n- `E`: stevilo povezav grafa.\n- `h`: visina drevesa ali kopice.\n- `b`: razvejanost B-drevesa ali stevilo bitov pri stevcu, odvisno od vrstice.\n- `k`: stevilo barv, hash funkcij ali izpisanih elementov, odvisno od vrstice.\n- `alpha(n)`: inverzna Ackermannova funkcija; v praksi skoraj konstanta.\n")
    md.append("## Tabela\n")
    md.append("| Sklop | Struktura / algoritem | Operacija / problem | Casovna zahtevnost | Pogoji / opomba | Vir |\n")
    md.append("|---|---|---|---|---|---|\n")
    for row in ROWS:
        md.append("| " + " | ".join(str(x).replace("|", "/") for x in row) + " |\n")
    md.append("\n## Viri\n")
    for key, value in SOURCE_MAP.items():
        md.append(f"- `{key}`: {value}\n")
    (OUT / "casovne_zahtevnosti_vsi_pdfji.md").write_text("".join(md), encoding="utf-8")


def make_pdf():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("Title2", parent=styles["Title"], fontName=FONT_BOLD, fontSize=18, leading=22, alignment=TA_CENTER, spaceAfter=10))
    styles.add(ParagraphStyle("Body2", parent=styles["BodyText"], fontName=FONT, fontSize=8.5, leading=10.5, spaceAfter=6))
    styles.add(ParagraphStyle("Small", parent=styles["BodyText"], fontName=FONT, fontSize=6.6, leading=7.8))
    styles.add(ParagraphStyle("SmallBold", parent=styles["BodyText"], fontName=FONT_BOLD, fontSize=6.7, leading=7.9))
    styles.add(ParagraphStyle("Section", parent=styles["Heading2"], fontName=FONT_BOLD, fontSize=11, leading=13, spaceBefore=8, spaceAfter=4))

    doc = SimpleDocTemplate(
        str(PDF / "casovne_zahtevnosti_vsi_pdfji.pdf"),
        pagesize=landscape(A4),
        rightMargin=0.7 * cm,
        leftMargin=0.7 * cm,
        topMargin=0.65 * cm,
        bottomMargin=0.65 * cm,
    )
    flow = [
        Paragraph("Tabela casovnih zahtevnosti iz PDF gradiv", styles["Title2"]),
        Paragraph("Zbrano iz predavanj in vaj. Kjer prosojnice vprasajo po zahtevnosti, je vpisana standardna ocena skupaj s pogoji uporabe.", styles["Body2"]),
        Paragraph("Legenda", styles["Section"]),
        Paragraph("n = stevilo elementov; V = stevilo vozlisc grafa oziroma kapaciteta pri nahrbtniku; E = stevilo povezav; h = visina; k = stevilo barv/hash funkcij/izpisov; alpha(n) = inverzna Ackermannova funkcija.", styles["Body2"]),
    ]

    grouped = {}
    for row in ROWS:
        grouped.setdefault(row[0], []).append(row)

    header = ["Sklop", "Struktura / algoritem", "Operacija / problem", "Casovna zahtevnost", "Pogoji / opomba", "Vir"]
    col_widths = [2.6 * cm, 4.6 * cm, 5.2 * cm, 3.7 * cm, 7.5 * cm, 2.1 * cm]
    for section, rows in grouped.items():
        flow.append(Paragraph(section, styles["Section"]))
        data = [[Paragraph(esc(x), styles["SmallBold"]) for x in header]]
        for row in rows:
            data.append([Paragraph(esc(str(x)), styles["Small"]) for x in row])
        table = Table(data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF7")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#B9C2D0")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 3),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FAFBFD")]),
        ]))
        flow.append(table)
        flow.append(Spacer(1, 5))

    flow.append(PageBreak())
    flow.append(Paragraph("Viri", styles["Section"]))
    for key, value in SOURCE_MAP.items():
        flow.append(Paragraph(f"<b>{esc(key)}</b>: {esc(value)}", styles["Body2"]))

    def footer(canvas, doc_):
        canvas.saveState()
        canvas.setFont(FONT, 7)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawRightString(landscape(A4)[0] - 0.7 * cm, 0.35 * cm, f"stran {doc_.page}")
        canvas.restoreState()

    doc.build(flow, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    write_markdown()
    make_pdf()
