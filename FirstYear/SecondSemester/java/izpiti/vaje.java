package izpiti;

import java.util.Random;

public class vaje {






    public static void main(String[] args){
        Random rnd = new Random();
        for(int i = 0; i<30; i++) {
            System.out.println(rnd.nextDouble(2, 3));
        }
    }


}
