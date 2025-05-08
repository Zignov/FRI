package vaje.vaje9.kodirniki;

public class Kodiranje {

    public Kodiranje(Kodirnik kodirnik) {
        this.kodirnik = kodirnik;
    }

    Kodirnik kodirnik;


    public String zakodiranjeBesedila(String besedilo){
        kodirnik.ponsatavi();
        StringBuffer rez = new StringBuffer();

        for(int i = 0; i<besedilo.length(); i++){
            int znak = (besedilo.charAt(i));
            int kodiranZnak = (kodirnik.zakodiraj(znak));
            rez.append((char) (kodiranZnak));
        }

        return rez.toString();
    }

    public String odkodiranjeBesedila(String besedilo){
        kodirnik.ponsatavi();
        StringBuffer rez = new StringBuffer();

        for(int i = 0; i<besedilo.length(); i++){
            int znak = (besedilo.charAt(i));
            int kodiranZnak = (kodirnik.odkodiraj(znak));
            rez.append((char) (kodiranZnak));
        }

        return rez.toString();
    }

}
