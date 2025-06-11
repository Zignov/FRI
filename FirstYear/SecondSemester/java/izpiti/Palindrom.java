package izpiti;

public class Palindrom {

    public static boolean jePalindrom(String niz){
        boolean rez = true;
        for(int i = 0; i<niz.length()/2; i++){


            if(niz.charAt(i) != niz.charAt(niz.length()-1-i)){
                rez = false;
                break;
            }
        }

        return rez;
    }


    public boolean jePalindromR(String niz){
        boolean rez = false;
        StringBuilder sb = new StringBuilder(niz);
       // System.out.println(niz);
        if (niz.isEmpty()){
            //System.out.println("fdasfasdfas");
            rez = true;
            return rez;
        }
        else{
            //System.out.println(sb.charAt(sb.length()-1));
            if(sb.charAt(0) == sb.charAt(sb.length()-1)){
                sb.deleteCharAt(sb.length()-1);
                if(!sb.isEmpty()) {
                    sb.deleteCharAt(0);
                }

                return (jePalindromR(sb.toString()));
            }
            else{
                rez = false;
                return rez;
            }
        }
    }



    public static void main(String[]args){
        boolean rez = jePalindrom(args[0]);
        System.out.println(rez ? "da" : "ne");
        Palindrom pa = new Palindrom();
        boolean rez2 = pa.jePalindromR(args[0]);
        //System.out.println(rez2);
        System.out.println(rez2 ? "da" : "ne");
    }


}
