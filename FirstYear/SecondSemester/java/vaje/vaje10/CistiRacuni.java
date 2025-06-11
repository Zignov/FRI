package vaje.vaje10;

public class CistiRacuni {



    public static void main(String[] args) {
        Dolgovi dolgovi = new Dolgovi();
        dolgovi.preberiPrijatelje(dolgovi.pri);
        dolgovi.izpisi();
        dolgovi.preberiDolgove(dolgovi.dol);
        dolgovi.izpisi();

        System.out.println("====================");
        dolgovi.izpisBrez(dolgovi.vrniBrezDolgov());

    }
}



