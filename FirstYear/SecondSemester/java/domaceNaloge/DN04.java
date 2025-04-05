public class DN04 {

    public static char prevod (String vhod){

        int stevec = 0;

        for(int x = 7; x>=0; x--) {
            if ((Short.parseShort(vhod, 2) & (1 << x)) != 0) {
                stevec += 1 << x;
            }

        }
        char rez = (char) stevec;
        return rez;
    }



    public static void main (String[] args){
        if (args.length == 1){
            for(int x = 0; x < args[0].length()/8; x++) {
                String sub = args[0].substring(x*8, (x+1)*8);
                //System.out.println(sub);
                System.out.print(prevod(sub));
            }
        }

    }
}
