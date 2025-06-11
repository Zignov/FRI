package izpiti;

import edu.princeton.cs.introcs.StdDraw;

import java.awt.*;

public class logotip {

    public static void izrisi(){
        StdDraw.setXscale(0,5);
        StdDraw.setYscale(0,5);
        int logotip = 0b1111101010001000101010001;
        int x = 0;
        int y = 0;
        int stevec = 1;

        while (logotip > 0){
            //System.out.println(Integer.toBinaryString(logotip));
            if ((logotip & 1) == 1){
                StdDraw.setPenColor(Color.BLACK);
            }
            else{
                StdDraw.setPenColor(Color.white);
            }
            StdDraw.filledSquare(x+0.5, y+0.5, 0.5);
            System.out.printf("bin: %s, x: %d, y: %d\n", Integer.toBinaryString(logotip), x, y);
            x+=1;
            if(stevec % 5 == 0) {
                y += 1;
                x = 0;
            }
            logotip = logotip >> 1;
            stevec++;
        }

        //StdDraw.filledSquare(-100,100,40);

    }


    public static void barvno(int prva, int druga) {
        StdDraw.setXscale(0, 5);
        StdDraw.setYscale(0, 5);
        int logotip = 0b1111101010001000101010001;
        int x = 0;
        int y = 0;
        int stevec = 1;

        while (prva > 0 || druga > 0) {
            //System.out.println(Integer.toBinaryString(logotip));
            if (((prva & 1) == 1) && (druga & 1) == 0) {
                StdDraw.setPenColor(Color.RED);
            } else if (((prva & 1) == 0) && (druga & 1) == 1) {
                StdDraw.setPenColor(Color.GREEN);
            } else if (((prva & 1) == 1) && (druga & 1) == 1) {
                StdDraw.setPenColor(Color.BLACK);
            }else {
                StdDraw.setPenColor(Color.WHITE);
            }

            StdDraw.filledSquare(x + 0.5, y + 0.5, 0.5);
            System.out.printf("bin: %s, x: %d, y: %d\n", Integer.toBinaryString(logotip), x, y);
            x += 1;
            if (stevec % 5 == 0) {
                y += 1;
                x = 0;
            }
            prva = prva >> 1;
            druga = druga >> 1;
            stevec++;
        }
    }


    public static void test(){
        StdDraw.setScale(-100,100);
        StdDraw.filledSquare(-20,-20,20);
    }




    public static void main(String[] args){
        izrisi();
        //test();

        //barvno( 32837969, 15259182);
    }


}
