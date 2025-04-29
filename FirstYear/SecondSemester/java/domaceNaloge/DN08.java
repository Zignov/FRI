package domaceNaloge;

public class DN08 {



    public static void main (String args[]) {
        int stLikov = args.length;
        Lik[] Liki = new Lik[stLikov];

        for (int i = 0; i < stLikov; i++) {
            String[] podatki = args[i].split(":");

            switch (podatki[0]) {
                case "kvadrat":
                    Liki[i] = new Kvadrat(Integer.parseInt(podatki[1]));
                    break;

                case "pravokotnik":
                    Liki[i] = new Pravokotnik(Integer.parseInt(podatki[1]), Integer.parseInt(podatki[2]));
                    break;

                case "nkotnik":
                    Liki[i] = new NKotnik(Integer.parseInt(podatki[1]), Integer.parseInt(podatki[2]));
                    break;
            }
        }

        double stevec = 0;

        for(int i = 0; i < Liki.length; i++){
            stevec += Liki[i].obseg();
        }

        System.out.print((int)stevec);
    }
}



abstract class Lik {
    abstract public double obseg();
}


class Kvadrat extends Lik{

    int stranica;

    Kvadrat(int stranica){
        this.stranica = stranica;
    }

    public double obseg(){
        return (stranica*4);
    }
}


class Pravokotnik extends Lik{
    int stranicaA;
    int stranicaB;

    Pravokotnik(int stranicaA, int stranicaB){
        this.stranicaA = stranicaA;
        this.stranicaB = stranicaB;
    }

    public double obseg(){
        return((stranicaA+stranicaB)*2);
    }
}

class NKotnik extends Lik{
    int stranica;
    int st;

    NKotnik(int st, int stranica){
        this.stranica = stranica;
        this.st = st;
    }

    public double obseg(){
        return(st*stranica);
    }
}

