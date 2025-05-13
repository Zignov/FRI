package domaceNaloge.kviz3;

public class Kompleksno {

    public String getIme() {
        return ime;
    }

    public double getRe() {
        return re;
    }

    public double getIm() {
        return im;
    }

    private String ime;
    private double re;
    private double im;

    public Kompleksno(String ime, double re, double im) {
        this.ime = ime;
        this.re = re;
        this.im = im;
    }

    public Kompleksno(double re, double im) {
        this.re = re;
        this.im = im;
    }


    public double velikost(){
        return (Math.sqrt((re*re)+(im*im)));
    }

    public void pristej(Kompleksno kompleksno){

        re += kompleksno.re;
        im += kompleksno.im;
    }

    public void pomnozi(Kompleksno kompleksno){

        double novRe = this.re * kompleksno.re - this.im * kompleksno.im;
        double novIm = this.re * kompleksno.im + this.im * kompleksno.re;
        this.re = novRe;
        this.im = novIm;
    }

    public String toString(){
        String rez = String.format("%s = (%.3f + %.3f*i)", ime, re, im);
        return(rez);
    }




}
