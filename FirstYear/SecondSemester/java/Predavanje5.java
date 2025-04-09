import edu.princeton.cs.introcs.StdDraw;
import java.awt.Color;

public class Predavanje5 {
    public static void elipse() {
        StdDraw.setScale(-100, 100);
        StdDraw.clear(Color.BLACK);
        StdDraw.setPenColor(Color.cyan);

        for(int i = 0; i<=100; i++){
            StdDraw.ellipse(0,0,100,100-i);
        }

        //StdDraw.ellipse(0,0,10,15);

        //StdDraw.circle(50, 50, 25);

    }

    public static void kvadrati(){
        int n = 25;
        int t = 10;

        StdDraw.setScale(0, n*t);
        for (int i = 0; i<t*n;i++){
            for (int j = 0; j<n;j++){
                int x = t/2 + t*j;
                int y = t/2 + t*i;

                StdDraw.setPenColor(new Color(j*10, i*10, 0));
                StdDraw.filledSquare(x,y,t/2);
            }
        }
    }


    public static void spirala(){
        StdDraw.setScale(-100, 100);
        int[][] smeri = {{0,-1}, {-1, 0}, {0,1}, {1,0}};

        int n = 200;
        int smer = 0;
        int trDolzina = 5;

        double trX = 0;
        double trY = 0;

        for(int i=0; i<n; i++){
            double nX = trX + smeri[smer][0] * trDolzina;
            double nY = trY + smeri[smer][1] * trDolzina;

            StdDraw.line(trX,trY,nX,nY);

            trX = nX;
            trY = nY;
            smer = (smer+1) % 4;
            trDolzina++;
        }

    }

    public static void risanje(){
        StdDraw.setScale(-100,100);
        while(true){
            StdDraw.filledCircle(StdDraw.mouseX(),StdDraw.mouseY(),1);
        }
    }


    public static void roza(int n){
        StdDraw.setScale(-100, 100);
        double trX = 0;
        double trY = 0;
        double d = 10;
        double fi = 0;
        double deltaFi = 2*Math.PI/n;

        for(int j = 0; j<n; j++){
            for (int i = 0; i<n;i++) {
                double nX = trX + Math.cos(fi) * (j<n-1 ? d : 2*d);
                double nY = trY + Math.sin(fi) * (j<n-1 ? d : 2*d);

                StdDraw.line(trX, trY, nX, nY);
                trX = nX;
                trY = nY;

                if(j<n-1) {
                    fi += deltaFi;
                }
            }
        }
    }

    public static void radar(){

        double kot = 0;
        double deltaKot = 2*Math.PI/360;
        while(true){

            StdDraw.setScale(-100, 100);
            StdDraw.clear(Color.black);

            StdDraw.setPenColor(Color.green);
            StdDraw.setPenRadius(0.007);

            StdDraw.enableDoubleBuffering();

            for(int i = 0; i<4; i++){
                StdDraw.circle(0,0,i*20 + 20);
            }


            double x = Math.cos(kot) * 80;
            double y = Math.sin(kot) * 80;

            StdDraw.line(0,0,x,y);
            kot-=deltaKot;


            StdDraw.show();
            StdDraw.pause(50);


        }
    }

    public static void ura(){
        StdDraw.setScale(-100, 100);

        double kot = 0;

        for(int i=0; i<36; i++){
            double x1 = 80 * Math.cos(Math.toRadians(kot));
            double y1 = 80 * Math.sin(Math.toRadians(kot));

            double x2 = 87 * Math.cos(Math.toRadians(kot));
            double y2 = 87 * Math.sin(Math.toRadians(kot));

            if(i % 3 == 0){
                StdDraw.setPenRadius(0.018);
            }
            else{
                StdDraw.setPenRadius(0.003);
            }

            StdDraw.line(x1, y1, x2, y2);
            kot+=10;
        }

        kot = 60;
        for(int i = 1; i<=12; i++){

            double x1 = 95 * Math.cos(Math.toRadians(kot));
            double y1 = 95 * Math.sin(Math.toRadians(kot));

            StdDraw.text(x1, y1, String.valueOf(i));
            kot-=360/12;
        }
    }

    public static void main (String[] args){
        //elipse();
        //kvadrati();
        //spirala();
        //risanje();
        //roza(5);
        //radar();
        ura();
    }
}


