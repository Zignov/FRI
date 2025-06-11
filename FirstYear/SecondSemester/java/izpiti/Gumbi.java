package izpiti;

import javax.swing.*;
import java.awt.*;
import java.util.ArrayList;
import java.util.Random;

public class Gumbi {
    public static void chaos(){
        JFrame okno = new JFrame();
        okno.setSize(900,900);
        okno.setLayout(new GridLayout(10,10));

        Random rnd = new Random();
        ArrayList<JButton> gumbi = new ArrayList<>();

        for(int i=0; i<100; i++){
            JButton gumb = new JButton(String.valueOf(i));
            gumbi.add(gumb);

            okno.add(gumb);
        }

        for (JButton gumb : gumbi){
            gumb.addActionListener(e -> {System.out.println(String.valueOf(gumb.getText()));});

            String zac = gumb.getText();
            JButton menjanGumb = gumbi.get(rnd.nextInt(gumbi.size()));
            String zac2 = menjanGumb.getText();
            gumb.addActionListener(e -> {gumb.setText(zac2); menjanGumb.setText(zac);});
        }

        okno.setVisible(true);
    }

    public static void main(String [] args){
            chaos();
    }



}
