package izpiti;

import javax.swing.*;
import java.awt.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Date;
import java.util.Random;

public class gui2 {
    public static void gui(){

        Random rnd = new Random();
        JFrame okno = new JFrame();
        okno.setSize(500,500);

        okno.setLayout(new BorderLayout());

        Container zgoraj = new Container();
        zgoraj.setLayout(new FlowLayout(FlowLayout.LEFT));

        JButton dat = new JButton("datum");
        dat.setSize(60,10);
        zgoraj.add(dat);

        JTextField text = new JTextField();
        text.setPreferredSize(new Dimension(120, 30));
        zgoraj.add(text);

        JButton bar = new JButton("barva");
        bar.setSize(60,10);
        zgoraj.add(bar);


        okno.add(zgoraj, BorderLayout.BEFORE_FIRST_LINE);

        JTextArea prazno = new JTextArea();
        prazno.setPreferredSize(new Dimension(400,400));
        prazno.setBackground(new Color(3,230,3));
        okno.add(prazno, BorderLayout.CENTER);



        Container spodaj = new Container();
        spodaj.setLayout(new FlowLayout(FlowLayout.RIGHT));
        spodaj.setPreferredSize(new Dimension(120, 30));
        spodaj.setBackground(Color.BLUE);
        JTextArea poz = new JTextArea();

        spodaj.add(poz);
        okno.add(spodaj, BorderLayout.AFTER_LAST_LINE);

        LocalDateTime datu = LocalDateTime.now();

        bar.addActionListener(e -> prazno.setBackground(new Color(rnd.nextInt(255), rnd.nextInt(255), rnd.nextInt(255))));
        dat.addActionListener(e -> text.setText(String.valueOf(datu)));



        okno.setVisible(true);
    }


    public static void main(String[] args){
        gui();
    }

}
