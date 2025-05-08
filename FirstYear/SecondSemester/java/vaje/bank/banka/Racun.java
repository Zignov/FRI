package vaje.bank.banka;

public abstract class Racun {
    private double stanje; // stanje na računu
    private final String stevilka; // številka računa

    /**
     * Konstruktor: ustvari račun s podano številko računa in začetnim stanjem 0,00 EUR.
     *
     * @param stevilka - številka računa
     */
    Racun(String stevilka) {
        this.stanje = 0.0;
        this.stevilka = stevilka;
    }

    /**
     * Položi znesek "znesek" na račun.
     *
     * @param znesek - položen znesek, pozitivno število
     * @return true, če je polog uspešno izveden, sicer false (v primeru nepozitivnega pologa)
     */
    public boolean polog(double znesek) {
        if(znesek<=0){
            return false;
        }
        stanje += znesek;
        return true;
    }

    /**
     * Dvigne znesek "znesek" z računa. Stanje računa je lahko tudi negativno.
     *
     * @param znesek - dvignjen znesek, pozitivno število
     * @return true, če je dvig uspešno izveden, sicer false (v primeru nepozitivnega zneska)
     */
    public boolean dvig(double znesek) {
        if(znesek<=0){
            return false;
        }
        stanje -= znesek;
        return true;
    }

    /**
     * Vrne trenutno stanje na računu (getter).
     *
     * @return stanje na računu
     */
    public double getStanje() {
        return stanje;
    }

    /**
     * Vrne številko računa (getter).
     *
     * @return številka računa
     */
    public String getStevilka() {
        return stevilka;
    }

    /**
     * Abstraktna metoda, ki vrne opis računa glede na njegov tip.
     *
     * @return niz z opisom računa
     */
    abstract String opisRacuna();

    /**
     * Pripravi niz, ki opisuje račun in njegovo trenutno stanje.
     * Niz je naslednje oblike: "Račun <stevilka> (<opis>): <stanje> EUR",
     * kjer je <stevilka> številka računa, <stanje> je stanje na računu, <opis> pa je opis tipa računa.
     *
     * @return niz, ki opisuje račun in stanje na njem
     */
    public String toString() {
        String rez = String.format("Račun <%s> (<%s>): <%.2f> EUR", getStevilka(), opisRacuna(), getStanje());
        return rez;
    }

}

class VarcevalniRacun extends Racun{
    private double obresti;
    private double stanje = super.getStanje();

    VarcevalniRacun(String stevilka, double obresti){
        super(stevilka);
        this.obresti = obresti;
    }


    public void dodajObresti(){
         stanje *= obresti;
    }

    public String opisRacuna(){
        String rez = String.format("(varčevalni, obrestna mera: %.3f): %.2f EUR", obresti, stanje);
        return rez;
    }
}

class TekociRacun extends Racun{
    private double limit;
    double stanje = super.getStanje();

    TekociRacun(String stevilka, double limit){
        super(stevilka);
        this.limit = limit;
    }

    @Override
    public boolean dvig(double znesek){
        if(znesek<=limit){
            return super.dvig(znesek);
        }
        return false;
    }

    public String opisRacuna(){
        String rez = String.format("(tekoči, limit: %.2f EUR): %.2f EUR", limit, stanje);
        return rez;
    }
}

