package vaje.vaje10;

import java.util.HashMap;
import java.util.Map;

public class Prijatelj implements Comparable<Prijatelj>{

    static int trenutniId = 1;
    String ime;
    int id;
    Map<Prijatelj, Double> dolgovi = new HashMap<>();

    public Prijatelj(String ime) {
        this.ime = ime;
        id = trenutniId;
        trenutniId++;
    }

    public Map<Prijatelj, Double> getDolgovi() {
        return dolgovi;
    }

    public String toString(){
        return String.format("[%03d] %s", id, ime);
    }


    public void dodajDolg(Prijatelj p, double znesek){
        if (dolgovi.containsKey(p)){
            double trenutniDolg = dolgovi.get(p);
            dolgovi.put(p, trenutniDolg + znesek);
        }
        else {
            dolgovi.put(p, znesek);
        }
    }

    public int compareTo(Prijatelj drugi){
        return this.ime.compareTo(drugi.ime);
    }


}
