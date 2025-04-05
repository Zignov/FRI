
public class Speed {
    public static void main(String args[]){

        long startTime = System.nanoTime();

        double a = 0;
        for (int x = 1; x<55; x++){
            a += 1.0 / (1<<x);
        }

        System.out.println(a);


        long endTime = System.nanoTime();
        long duration = endTime - startTime;

        System.out.println("Execution Time: " + duration + " nanoseconds");
        System.out.println("Execution Time: " + (duration / 1_000_000.0) + " milliseconds");
    }
}