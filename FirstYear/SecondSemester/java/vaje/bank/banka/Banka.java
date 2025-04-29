package vaje.bank.banka;

public class Banka {

    int steviloRacunov = 0;
    Racun[] racuni = new Racun[500];

    public boolean dodajTekociRacun(String stevilka, double limit){
        Racun ra1 = new TekociRacun(stevilka, limit);

        for(int i = 0; i<steviloRacunov; i++){
            if(racuni[i].getStevilka().equals(stevilka)){
                return false;
            }
        }

        racuni[steviloRacunov] = ra1;
        steviloRacunov++;
        return true;
    }

    public boolean dodajVarcevalniRacun(String stevilka, double obresti) {
        Racun ra1 = new VarcevalniRacun(stevilka, obresti);
        for (int i = 0; i < steviloRacunov; i++) {
            if (racuni[i].getStevilka().equals(stevilka)) {
                return false;
            }
        }

        racuni[steviloRacunov] = ra1;
        steviloRacunov++;
        return true;
    }

    public void izpisiRacune(){
        for(int i = 0; i<steviloRacunov; i++){
            if(racuni[i] != null) {
                System.out.println(racuni[i].toString());
            }
        }
    }

    public void izpisiRacune(boolean varcevalni){
        int stevecV = 0;
        int stevecT = 0;
        for(int i = 0; i<steviloRacunov; i++){
            if(racuni[i] instanceof VarcevalniRacun == varcevalni) {
                System.out.println(racuni[i].toString());
                stevecV++;
            }
            else {
                System.out.println(racuni[i].toString());
                stevecT++;
            }
        }

        if(varcevalni){
            System.out.printf("Stevilo racunov: %d", stevecV);
        }
        else {
            System.out.printf("Stevilo racunov: %d", stevecT);
        }
    }

    public boolean dvig(String stevila, double znesek){
        for(int i = 0; i<steviloRacunov; i++){
            if(stevila.equals(racuni[i].getStevilka())){
                racuni[i].dvig(znesek);
                return true;
            }
        }
        return false;
    }

    public boolean polog(String stevila, double znesek){
        for(int i = 0; i<steviloRacunov; i++){
            if(stevila.equals(racuni[i].getStevilka())){
                racuni[i].polog(znesek);
                return true;
            }
        }
        return false;
    }
}
