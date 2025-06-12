package prviRok;

import edu.princeton.cs.introcs.StdDraw;

import java.util.Random;

public class Trikotnik {


    public static void main(String[]args){
        StdDraw.setScale(-100,100);

        int[][] tocke = {{0,100}, {-100,-100}, {100,-100}};

        StdDraw.line(tocke[0][0], tocke[0][1], tocke[1][0], tocke[1][1]);
        StdDraw.line(tocke[1][0], tocke[1][1], tocke[2][0], tocke[2][1]);
        StdDraw.line(tocke[0][0], tocke[0][1], tocke[2][0], tocke[2][1]);


        Random rnd = new Random();

        int nakljY = rnd.nextInt(-100,100);
        int nakljX = rnd.nextInt(nakljY)-nakljY/2;

        //StdDraw.setPenRadius(0.05);
        StdDraw.point(nakljX, nakljY);

        for(int i = 0; i<10000; i++){
            int a = rnd.nextInt(3);

            int x = (nakljX + tocke[a][0])/2;
            int y = (nakljY + tocke[a][1])/2;

            StdDraw.point(x,y);
            nakljX = x;
            nakljY = y;
        }
    }

}
