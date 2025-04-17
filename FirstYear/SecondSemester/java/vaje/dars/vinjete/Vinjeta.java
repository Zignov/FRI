package vaje.dars.vinjete;

public class Vinjeta    {


    public Vinjeta(String registerska, String razred, String datum, String vrsta) {
        this.registerska = registerska;
        this.razred = razred;
        this.datum = datum;
        this.vrsta = vrsta;
    }


    private String registerska;
    private String razred;
    private String datum;
    private String vrsta;

    public String toString(){
        String rez = String.format("%s, [%s]: %s (%s)", registerska, razred, vrsta, datum);
        return (rez);
    }

    public String getRegisterska() {
        return registerska;
    }

    public void setRegisterska(String registerska) {
        this.registerska = registerska;
    }

    public String getRazred() {
        return razred;
    }

    public void setRazred(String razred) {
        this.razred = razred;
    }

    public String getDatum() {
        return datum;
    }

    public void setDatum(String datum) {
        this.datum = datum;
    }

    public String getVrsta() {
        return vrsta;
    }

    public void setVrsta(String vrsta) {
        this.vrsta = vrsta;
    }
}
