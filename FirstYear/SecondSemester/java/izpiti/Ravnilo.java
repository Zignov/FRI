package izpiti;

import edu.princeton.cs.introcs.StdDraw;

import java.lang.reflect.Type;

public class Ravnilo {



    public static void main (String[]args){

        StdDraw.setScale(-100,100);

        //StdDraw.line(0,-40,80,-40);

        //StdDraw.line(0,-40, 100*Math.cos(Math.toRadians(0)), 100*Math.sin(Math.toRadians(0)));

        for(int i = 0; i<=180; i+=10) {
            //System.out.println(Math.sin(Math.toRadians(i)));
            if(i%90 == 0) {
                StdDraw.line(0, -40, 70 * Math.cos(Math.toRadians(i)), 70 * Math.sin(Math.toRadians(i)) - 40);
                StdDraw.line(80*Math.cos(Math.toRadians(i)), 80 * Math.sin(Math.toRadians(i))-40, 90 * Math.cos(Math.toRadians(i)), 90 * Math.sin(Math.toRadians(i)) - 40);
            }
            else{
                StdDraw.line(10*Math.cos(Math.toRadians(i)), 10 * Math.sin(Math.toRadians(i))-40, 70 * Math.cos(Math.toRadians(i)), 70 * Math.sin(Math.toRadians(i)) - 40);
                StdDraw.line(80*Math.cos(Math.toRadians(i)), 80 * Math.sin(Math.toRadians(i))-40, 90 * Math.cos(Math.toRadians(i)), 90 * Math.sin(Math.toRadians(i)) - 40);
            }

            //System.out.println(85 * Math.cos(Math.toRadians(i)));

            StdDraw.text((75 * Math.cos(Math.toRadians(i))), (75 * Math.sin(Math.toRadians(i)) - 40), String.valueOf(i), i-90);
            //StdDraw.text(85 * Math.cos(Math.toRadians(i)),85 * Math.sin(Math.toRadians(i)) - 40), String.valueOf(i), i+90);
        }

        for(int i = 0; i<=180; i+=2) {
            StdDraw.line(85*Math.cos(Math.toRadians(i)), 85 * Math.sin(Math.toRadians(i))-40, 90 * Math.cos(Math.toRadians(i)), 90 * Math.sin(Math.toRadians(i)) - 40);

        }


    }

}
