import java.util.Random;


public class Loto {
    public static void main(String[] args) throws InterruptedException {
        Random rnd = new Random();

        while (true){
            System.out.println(1 + rnd.nextInt(39));
            //Thread.sleep(200);
        }



    }
}
