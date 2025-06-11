package izpiti;
import javax.swing.*;
import javax.swing.border.Border;
import java.awt.*;

public class guiVaja {

    public static void First(){
        JFrame okno = new JFrame("glava");
        okno.setVisible(true);
        okno.setSize(300, 173);
        okno.setResizable(false);

        Container vse = okno.getContentPane();
        vse.setLayout(null);


        JLabel ime = new JLabel("ime:");
        ime.setBounds(10,10,50,20);
        vse.add(ime);

        JTextField vnos = new JTextField();
        vnos.setBounds(60, 10, 140, 20);
        vse.add(vnos);

        JButton isci = new JButton("Isci");
        isci.setBounds(210, 10, 70, 20);
        vse.add(isci);

        JTextField belo = new JTextField();
        belo.setBounds(10, 40, 270, 80);
        vse.add(belo);
    }


    public static void Gumbi(){
        JFrame okno = new JFrame("FlowLayout test");
        okno.setSize(500,200);


        Container kont = okno.getContentPane();
        kont.setLayout(new BorderLayout());

        JButton ena = new JButton("prvi");
        okno.add(ena, BorderLayout.CENTER);

        JButton dva = new JButton("drugi");
        okno.add(dva, BorderLayout.PAGE_END);

        JButton tri = new JButton("tretji");
        okno.add(tri, BorderLayout.LINE_START);

        JButton stiri = new JButton("cetrti");
        okno.add(stiri, BorderLayout.WEST);

        okno.setVisible(true);


        if (stiri.getAction() != null){
            System.out.print("dela");
        }
    }

    public static void JPanelTest(){
        JFrame okno = new JFrame("BorderLayout");
        okno.setSize(300, 300);

        okno.setLayout(new BorderLayout());
        JTextField text = new JTextField();
        okno.add(text, BorderLayout.CENTER);

        JPanel gumbi = new JPanel();
        gumbi.setLayout(new FlowLayout());


        JButton ok = new JButton("OK");
        JButton cancel = new JButton("Cancel");

        gumbi.add(ok);
        gumbi.add(cancel);

        okno.add(gumbi, BorderLayout.PAGE_END);

        okno.setVisible(true);

        // Change color of the text field when OK button is clicked
        ok.addActionListener(e -> text.setBackground(Color.YELLOW));
        // Change color of the text field when Cancel button is clicked
        cancel.addActionListener(a -> text.setBackground(Color.RED));
    }



    public static String racunaj(int a, int b, String znak) {
        switch (znak) {
            case ("+"):
                return (String.valueOf(a + b));
            case ("-"):
                return (String.valueOf(a - b));
            case ("*"):
                return (String.valueOf(a * b));
            case ("/"):
                return (String.valueOf(a / b));
            default:
                return ("napaka");
        }

    }

    public static void kalk(){
        JFrame okno = new JFrame("kalkulator");

        okno.setSize(500,120);

        okno.setLayout(new BorderLayout());

        JPanel vnos = new JPanel();
        vnos.setLayout(new FlowLayout());

        JTextField prva = new JTextField();
        JTextField znak = new JTextField();
        JTextField druga = new JTextField();
        JTextField rezultat = new JTextField();
        JLabel je = new JLabel("=");

        prva.setPreferredSize(new Dimension(120,  30));
        znak.setPreferredSize(new Dimension(60,  30));
        druga.setPreferredSize(new Dimension(120,  30));
        rezultat.setPreferredSize(new Dimension(120,  30));
        je.setPreferredSize(new Dimension(25,  30));

        vnos.setSize(500,150);
        vnos.setBackground(Color.yellow);

        vnos.add(prva);
        vnos.add(znak);
        vnos.add(druga);
        vnos.add(je);
        vnos.add(rezultat);

        vnos.setVisible(true);

        okno.add(vnos, BorderLayout.CENTER);

        JButton izr = new JButton("Izracunaj");
        izr.setSize(200,40);
        okno.add(izr, BorderLayout.PAGE_END);

        okno.setVisible(true);



        izr.addActionListener(e -> rezultat.setText(racunaj(Integer.parseInt(prva.getText()), Integer.parseInt(druga.getText()), znak.getText())));

    }



    public static void main (String args[]) {

        //First();
        //Gumbi();
        //JPanelTest();


        kalk();

    }
}




