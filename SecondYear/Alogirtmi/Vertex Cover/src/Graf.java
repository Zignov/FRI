


public class Graf{
    private int stVozlisc;
    private boolean[][] povezave;


    public Graf(int stVozlisc){
        this.stVozlisc = stVozlisc;
        this.povezave = new boolean[stVozlisc][stVozlisc];
    }


    public void povezi(int u, int v){
        povezave[u][v] = true;
        povezave[v][u] = true;
    }


    public void grobaSila(){


        int vseh = 1;

        for (int i = 0; i < stVozlisc; i++) {
            vseh *= 2;
        }


        boolean[] najboljsa = new boolean[stVozlisc];
        int najlojsaVelikost = stVozlisc + 1;



        for (int k = 0; k<vseh; k++){
            boolean[] trenutna = narediMnozico(k);

            if (jeVC(trenutna)){
                int velikost = velikost(trenutna);

                if (velikost < najlojsaVelikost){
                    najlojsaVelikost = velikost;

                    for (int i = 0; i < stVozlisc; i++) {
                        najboljsa[i] = trenutna[i];
                    }
                }
            }
        }

        for (int i = 0; i < stVozlisc; i++) {
            if (najboljsa[i]){
                System.out.print(i+" ");
            }
        }


    }


    private boolean[] narediMnozico(int k){
        boolean[] mnozica = new boolean[stVozlisc];

        for (int i = 0; i < stVozlisc; i++) {
            if (k%2 == 1){
                mnozica[i] = true;
            }

            k = k/2;
        }

        return mnozica;
    }


    private boolean jeVC(boolean[] mnozica){
        for (int i = 0; i < stVozlisc; i++) {
            for (int j = i+1; j < stVozlisc; j++) {
                if (povezave[i][j] && !mnozica[i] && !mnozica[j]){
                    return false;
                }
            }
        }

        return true;
    }

    private int velikost(boolean[] mnozica){
        int velikost = 0;

        for (int i = 0; i < stVozlisc; i++) {
            if (mnozica[i]){
                velikost++;
            }
        }

        return velikost;
    }


    public void pozresni(){
    }
}