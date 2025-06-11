package izpiti;

public class NajdaljseUjemanje {



    public String poisciUjemanje(String prvi, String drugi){
        int max = 0;
        String rez = "";
        for(int i = 0; i<prvi.length(); i++){
            for(int j = i+1; j<prvi.length()+1; j++){
                String sub = prvi.substring(i,j);
                //System.out.println(sub);

                if(drugi.contains(sub) && sub.length()>max){
                    rez = sub;
                    max = sub.length();
                }
            }

        }




        return rez;
    }


    public static void main (String[] args){
        NajdaljseUjemanje nu = new NajdaljseUjemanje();
        System.out.println(nu.poisciUjemanje("Danes je lep dan", "Dandanes je lepo"));
    }


}
