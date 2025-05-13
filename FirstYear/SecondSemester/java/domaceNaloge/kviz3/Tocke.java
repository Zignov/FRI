package domaceNaloge.kviz3;


public class Tocke {
    void preberiInIzpisi(String oznaka){

        java.util.ArrayList<Integer> seznamID = new java.util.ArrayList<>();
        java.util.ArrayList<String> seznamImen = new java.util.ArrayList<>();
        java.util.ArrayList<Integer> seznamTock = new java.util.ArrayList<>();

        try {
            java.util.Scanner sc = new java.util.Scanner(new java.io.File(oznaka + "-prijave.txt"));

            while (sc.hasNextLine()){
                String vrstica = sc.nextLine();
                seznamID.add(Integer.parseInt(vrstica.split(":")[0]));
                seznamImen.add(vrstica.split(":")[1]);
                seznamTock.add(0);
            }

            sc.close();


            for (int i = 1; i<5; i++){
                String imeDat = oznaka + "-n" + i + ".txt";


                try{
                    java.util.Scanner naloga = new java.util.Scanner(new java.io.File(imeDat));


                    while(naloga.hasNextLine()){
                        String vrstica = naloga.nextLine();

                        String[] podatki = vrstica.split(":");

                        for (int j = 0; i < seznamID.size(); j++){
                            if (Integer.parseInt(podatki[0]) == seznamID.get(j)){
                                seznamTock.set(j, seznamTock.get(j) +  Integer.parseInt(podatki[1]));
                                break;
                            }
                        }


                    }
                    naloga.close();
                }
                catch (Exception e){

                }
            }


        }
        catch (Exception e){

        }



        for (int i = 0; i < seznamImen.size() - 1; i++) {
            for (int j = i + 1; j < seznamImen.size(); j++) {
                if (seznamImen.get(i).compareTo(seznamImen.get(j)) > 0) {
                    String tempIme = seznamImen.get(i);
                    seznamImen.set(i, seznamImen.get(j));
                    seznamImen.set(j, tempIme);


                    int tempID = seznamID.get(i);
                    seznamID.set(i, seznamID.get(j));
                    seznamID.set(j, tempID);


                    int tempTocke = seznamTock.get(i);
                    seznamTock.set(i, seznamTock.get(j));
                    seznamTock.set(j, tempTocke);
                }
            }
        }



        java.util.ArrayList<String> vrstice = new java.util.ArrayList<>();

        for (int i = 0; i < seznamID.size(); i++) {
            int id = seznamID.get(i);
            String ime = seznamImen.get(i);
            int vsota = seznamTock.get(i);


            if (vsota == 0) {
                vrstice.add(id + ":" + ime + ":VP");
            } else {
                vrstice.add(id + ":" + ime + ":" + vsota);
            }
        }



        for (int i = 0; i<vrstice.size(); i++){
            System.out.println(vrstice.get(i));
        }

    }



}
