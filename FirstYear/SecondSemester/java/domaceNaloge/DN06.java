//package DomaceNaloge;

import edu.princeton.cs.introcs.StdDraw;

public class DN06 {

    public static void main(String[] args){

        StdDraw.setScale(-150,310);
        StdDraw.setPenRadius(0.005);
        int stevec = 0;

        for(int i = 3; i>0; i--){

            for(int j = 0; j<3; j++){
                StdDraw.setPenRadius(0.005);
                StdDraw.square(100/3*j*2, 100/3*i*2, 100/3);

                StdDraw.setPenRadius(0.0027);
                for(int k = 3; k>0; k--){
                    for(int l = 0; l<3; l++){
                        StdDraw.square(100/3*j*2+100/9*(l-1)*2, 100/3*i*2+100/9*(k-2)*2, 100/9);

                        int vrstica = 3 * (3 - i) + (3 - k);
                        int stolpec = 3 * j + l;
                        Character stev = args[0].charAt(vrstica * 9 + stolpec);

                        //Character stev = args[0].charAt(stevec);
                        //System.out.println(stev);



                        if(!stev.equals('0')) {
                                StdDraw.text(100/3*j*2+100/9*(l-1)*2, 100/3*i*2+100/9*(k-2)*2, String.valueOf(stev));
                                //System.out.printf("X: %d, Y: %d, ST: %s" + "\n", 100/3*j*2+100/9*(l-1)*2, 100/3*i*2+100/9*(k-2)*2, String.valueOf(stev));

                        }
                        stevec++;
                    }
                }
            }

            //StdDraw.circle(22, -22, 6);
        }

    }




}

