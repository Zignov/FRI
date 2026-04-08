import java.util.Comparator;

public class TabelaTabel {


    private static class Lokacija{
        int i;
        int j;

        Lokacija(int i, int j){
            this.i = i;
            this.j = j;
        }
    }


    private Comparator<String> comparator;


    private String[][] tabele;

    private int[][] pojavitve;

    private boolean[][] izbrisano;


    public TabelaTabel(Comparator<String> comparator){
        this.comparator = comparator;
        this.tabele = new String[1][];
        this.pojavitve = new int[1][];
        this.izbrisano = new boolean[1][];
    }



    public void izpisi(){
        boolean vsePrazno = true;

        for (int i = 0; i< tabele.length; i++){
            if(!jePrazna(i)){
                vsePrazno = false;
                break;
            }
        }

        if (vsePrazno){
            System.out.println("prazen");
            return;
        }

        for(int i = 0; i<tabele.length; i++){
            //System.out.print("A" + i+ ": ");

            if(tabele[i] == null){
                System.out.println("...");
                continue;
            }

            for(int j = 0; j<tabele[i].length; j++){
                if(j>0){
                    System.out.print(", ");
                }

                if(tabele[i][j] == null){
                    System.out.print("x");
                } else if (izbrisano[i][j]) {
                    System.out.print("x");

                }
                else{
                    System.out.print(tabele[i][j] + "/" + pojavitve[i][j]);
                }

                //System.out.println("");
            }

            System.out.println();
        }
    }


    //povecevvanje tabele.......


    private void naslednjiNivo(int level){

        if(level< tabele.length){
            return;
        }


        int novaDolzina = level + 1;

        String[][] noveTabele = new String[novaDolzina][];
        int[][] novePojavtive = new int[novaDolzina][];
        boolean[][] novaIzbrisano = new boolean[novaDolzina][];


        for (int i = 0; i < tabele.length; i++){
            noveTabele[i] = tabele[i];
            novePojavtive[i] = pojavitve[i];
            novaIzbrisano[i] = izbrisano[i];
        }

        tabele = noveTabele;
        pojavitve = novePojavtive;
        izbrisano = novaIzbrisano;
    }

    /*private void inicializacija(int i){
        if (tabele[i] != null){
            return;
        }

        int velikost = 1<<i;

        tabele[i] = new String[velikost];
        pojavitve[i] = new int [velikost];
        izbrisano[i] = new boolean[velikost];
    }*/



    //Pomozne metode o polnosti.......


    private boolean jePrazna(int i){
        if (i>= tabele.length || tabele[i] == null){
            return true;
        }

        for (int j = 0; j<tabele[i].length; j++){
            if (tabele[i][j] != null && !izbrisano[i][j]){
                return false;
            }
        }
        return true;
    }

    private boolean jePolna(int i){
        if(i>= tabele.length || tabele[i] == null){
            return false;
        }

        for (int j = 0; j<tabele[i].length; j++){
            if(tabele[i][j] == null || izbrisano[i][j]){
                return false;
            }
        }
        return true;
    }

    private boolean jeDelnoZasedena(int i){
        return !jePrazna(i) && !jePolna(i);
    }




    //Iskanje lokacije........


    private Lokacija poisciLokacijo(String element){
        for(int i = 0; i< tabele.length; i++){
            if(tabele[i] == null){
                continue;
            }

            for(int j = 0; j<tabele[i].length; j++){
                if(tabele[i][j] != null && !izbrisano[i][j] && comparator.compare(tabele[i][j], element) == 0){
                    return new Lokacija(i, j);
                }
            }
        }
        return null;
    }


    public void najdi(String element){
        Lokacija lokacija = poisciLokacijo(element);
        System.out.println(lokacija != null);
    }




    private String[] zlijElemente(String [] a, int[] pa, String[] b, int[] pb, int[] novePojavitve){

        String[] rezultat = new String[a.length + b.length];

        int i = 0;
        int j = 0;
        int k = 0;

        while(i<a.length && j<b.length){
            if(comparator.compare(a[i], b[j]) <= 0){
                rezultat[k] = a[i];
                novePojavitve[k] = pa[i];
                i++;
            }
            else{
                rezultat[k] = b[j];
                novePojavitve[k] = pb[j];
                j++;
            }
            k++;
        }

        while (i<a.length){
            rezultat[k] = a[i];
            novePojavitve[k] = pa[i];
            i++;
            k++;
        }

        while (j<b.length){
            rezultat[k] = b[j];
            novePojavitve[k] = pb[j];
            j++;
            k++;
        }

        return rezultat;
    }



    //Pomozne metode za pol polno tabelo........


    private int stAktivnihElementov(int i){
        if(i>= tabele.length || tabele[i] == null){
            return 0;
        }

        int st = 0;
        for (int j = 0; j< tabele[i].length; j++){
            if(tabele[i][j] != null && !izbrisano[i][j]){
                st++;
            }
        }
        return st;
    }


    private String[] aktivniElementi(int i){

        int st = stAktivnihElementov(i);

        String[] rezultat = new String[st];

        int k = 0;

        for(int j = 0; j< tabele[i].length; j++){
            if (tabele[i][j] != null && !izbrisano[i][j]){
                rezultat[k] = tabele[i][j];
                k++;
            }
        }

        return rezultat;
    }

    private int[] aktivnePojavitve(int i){

        int st = stAktivnihElementov(i);

        int[] rezultat = new int[st];

        int k = 0;

        for(int j = 0; j< tabele[i].length; j++){
            if (tabele[i][j] != null && !izbrisano[i][j]){
                rezultat[k] = pojavitve[i][j];
                k++;
            }
        }

        return rezultat;
    }



    private void vstaviVDelno(int i, String element){
        String[] stariElementi = aktivniElementi(i);
        int[] starePojavitve = aktivnePojavitve(i);

        String[] novElement = {element};
        int[] novPojavitve = {1};

        int[] zdruzenePojavitve = new int[stariElementi.length +1];
        String[] zdruzeniElementi = zlijElemente(stariElementi, starePojavitve, novElement, novPojavitve, zdruzenePojavitve);

        int velikost = tabele[i].length;

        String[] novaTabela = new String[velikost];
        int[] novaPoj = new int[velikost];
        boolean[] novaIzb = new boolean[velikost];


        int k = 0;

        for (; k<zdruzeniElementi.length; k++){
            novaTabela[k] = zdruzeniElementi[k];
            novaPoj[k] = zdruzenePojavitve[k];
            novaIzb[k] = false;
        }

        for(; k<velikost; k++){
            novaTabela[k] = null;
            novaPoj[k] = 0;
            novaIzb[k] = true;
        }

        tabele[i] = novaTabela;
        pojavitve[i] = novaPoj;
        izbrisano[i] = novaIzb;
    }






    // Logika za vstavljanje.........

    public void vstavi(String element){
        Lokacija lokacija = poisciLokacijo(element);

        if(lokacija != null){
            pojavitve[lokacija.i][lokacija.j]++;
            return;
        }

        String[] tempEl = {element};
        int[] tempPoj = {1};

        int nivo = 0;

        while(true){
            naslednjiNivo(nivo);

            if(tabele[nivo] == null || jePrazna(nivo)){
                tabele[nivo] = tempEl;
                pojavitve[nivo] = tempPoj;
                izbrisano[nivo] = new boolean[tempEl.length];
                return;
            }


            if(jePolna(nivo)){
                int[] novePojavtive = new int[tempEl.length + tabele[nivo].length];
                String[] zlitje = zlijElemente(tempEl, tempPoj, tabele[nivo], pojavitve[nivo], novePojavtive);

                tempEl = zlitje;
                tempPoj = novePojavtive;

                tabele[nivo] = null;
                pojavitve[nivo] = null;
                izbrisano[nivo] = null;

                nivo ++;
            }
            else{
                vstaviVDelno(nivo, element);
                return;
            }
        }
    }




    // brisanje.......


    public void izbrisi(String element){
        Lokacija lokacija = poisciLokacijo(element);

        if(lokacija == null){
            System.out.println(false);
            return;
        }


        if(pojavitve[lokacija.i][lokacija.j] > 1){
            pojavitve[lokacija.i][lokacija.j] --;
        }
        else{
            izbrisano[lokacija.i][lokacija.j] = true;
        }

        System.out.println(true);
    }
}