public class pitagoroviTrojcki {
    public static void pitagoroviTrojcki(int x){
        int[] seznam = new int[x+1];
        for(int i = 1; i<=x; i++){
            seznam[i-1] = i*i;
        }

        for (int i = 0; i<seznam.length; i++){
            System.out.println(seznam[i]);
        }
    }


    public static void main(String[] args) {
        pitagoroviTrojcki(5);

    }
}
