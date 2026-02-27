


public class Sudoku {


    public static final int velikostTabele = 9;


    static void printBoard(int[][] povrsina, boolean[][] podane){
        for(int r = 0; r<9; r++){
            if(r%3 == 0) System.out.println("+-------+-------+-------+");

            for(int c = 0; c<9; c++){
                if(c%3 == 0) System.out.println("| ");

                int celica = povrsina[r][c];

                if(celica == 0){
                    System.out.println(". ");
                }
                else{
                    if(podane[r][c]) System.out.println("[" + celica + "]");
                    else{
                        System.out.println(celica + " ");
                    }
                }
            }
        }
        System.out.println("+-------+-------+-------+");
    }






}