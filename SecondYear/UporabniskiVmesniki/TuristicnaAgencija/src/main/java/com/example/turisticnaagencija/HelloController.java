package com.example.turisticnaagencija;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.*;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;

import java.net.URL;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

import java.util.ArrayList;
import java.util.List;
import java.util.ResourceBundle;

public class HelloController implements Initializable {

    @FXML private TabPane tabPane;

    @FXML private VBox potnikiContainer;

    @FXML private ComboBox<String> odhodBox;
    @FXML private ComboBox<String> destinacijaBox;
    @FXML private DatePicker odhodOd;
    @FXML private DatePicker odhodDo;
    @FXML private DatePicker povratekOd;
    @FXML private DatePicker povratekDo;
    @FXML private ComboBox<String> razredBox;
    @FXML private ComboBox<String> sedezBox;
    @FXML private RadioButton jutranjiRadio;
    @FXML private RadioButton vecerniRadio;
    @FXML private RadioButton direktenRadio;

    @FXML private VBox obrokiContainer;
    @FXML private VBox prtljagaContainer;
    @FXML private CheckBox rentacarCheck;
    @FXML private ComboBox<String> kategorijaBox;
    @FXML private Label modelLabel;
    @FXML private CheckBox otroskiSedezCheck;
    @FXML private Label rentInfoLabel;

    @FXML private ComboBox<String> karticaBox;
    @FXML private TextField imeKarticaField;
    @FXML private TextField stevilkaKarticaField;
    @FXML private TextField veljavnostField;
    @FXML private PasswordField cvvField;
    @FXML private Label cenaKartLabel;
    @FXML private Label cenaAvtoLabel;
    @FXML private Label skupajDanesLabel;

    @FXML private TextArea povzetekPotnikiArea;
    @FXML private Label povzetekLet;
    @FXML private Label povzetekDatum;
    @FXML private Label povzetekRazred;
    @FXML private Label povzetekSedezi;
    @FXML private Label povzetekObroki;
    @FXML private Label povzetekPrtljaga;
    @FXML private Label povzetekAvto;
    @FXML private Label povzetekCenaKart;
    @FXML private Label povzetekCenaAvto;
    @FXML private Label povzetekKartica;
    @FXML private Label emailPoslanLabel;

    private final List<PassengerForm> potniki = new ArrayList<>();
    private final DateTimeFormatter fmt = DateTimeFormatter.ofPattern("dd. MM. yyyy");

    @Override
    public void initialize(URL url, ResourceBundle rb) {
        nastaviComboBoxe();

        ToggleGroup tg = new ToggleGroup();
        jutranjiRadio.setToggleGroup(tg);
        vecerniRadio.setToggleGroup(tg);
        direktenRadio.setToggleGroup(tg);

        dodajPotnika(true);
        nastaviKartico();

        rentacarCheck.setOnAction(e -> {
            toggleRentacar();
            posodobiCene();
        });

        kategorijaBox.setOnAction(e -> {
            posodobiModelAvta();
            posodobiCene();
        });

        odhodBox.setOnAction(e -> posodobiCene());
        destinacijaBox.setOnAction(e -> posodobiCene());
        razredBox.setOnAction(e -> posodobiCene());
        direktenRadio.setOnAction(e -> posodobiCene());
        jutranjiRadio.setOnAction(e -> posodobiCene());
        vecerniRadio.setOnAction(e -> posodobiCene());

        toggleRentacar();
        posodobiDodatke();
        posodobiCene();
    }

    private void nastaviComboBoxe() {
        odhodBox.getItems().addAll("Ljubljana", "Trst", "Benetke", "Zagreb", "Dunaj");
        destinacijaBox.getItems().addAll("New York", "London", "Pariz", "Berlin", "Rim", "Dubai");
        razredBox.getItems().addAll("Ekonomski", "Poslovni", "Prvi razred");
        sedezBox.getItems().addAll("Skupaj", "Skupaj in čim bolj spredaj", "Pri oknu", "Ob hodniku");
        kategorijaBox.getItems().addAll("Ekonomski", "Srednji razred", "SUV", "Luksuzni");
        karticaBox.getItems().addAll("VISA", "Mastercard", "American Express");

        odhodBox.setPromptText("Izberite odhod");
        destinacijaBox.setPromptText("Izberite destinacijo");
        razredBox.setPromptText("Izberite razred");
        sedezBox.setPromptText("Izberite sedeže");
        kategorijaBox.setPromptText("Izberite kategorijo");
        karticaBox.setPromptText("Izberite kartico");
    }

    private void nastaviKartico() {
        stevilkaKarticaField.textProperty().addListener((obs, oldVal, newVal) -> {
            String s = newVal.replaceAll("[^0-9]", "");

            if (s.length() > 16) {
                s = s.substring(0, 16);
            }

            StringBuilder sb = new StringBuilder();

            for (int i = 0; i < s.length(); i++) {
                if (i > 0 && i % 4 == 0) {
                    sb.append(" ");
                }
                sb.append(s.charAt(i));
            }

            if (!newVal.equals(sb.toString())) {
                stevilkaKarticaField.setText(sb.toString());
                stevilkaKarticaField.positionCaret(sb.length());
            }
        });
    }

    @FXML
    private void dodajPotnika() {
        dodajPotnika(false);
    }

    private void dodajPotnika(boolean glavni) {
        PassengerForm p = new PassengerForm(glavni);
        potniki.add(p);
        potnikiContainer.getChildren().add(p.root);
        osveziPotnike();
        posodobiDodatke();
        posodobiCene();
    }

    private void odstraniPotnika(PassengerForm p) {
        if (p.glavni) {
            return;
        }

        potniki.remove(p);
        potnikiContainer.getChildren().remove(p.root);
        osveziPotnike();
        posodobiDodatke();
        posodobiCene();
    }

    private void osveziPotnike() {
        for (int i = 0; i < potniki.size(); i++) {
            PassengerForm p = potniki.get(i);
            String text = "Potnik " + (i + 1);

            if (p.glavni) {
                text += " - glavni potnik";
            }

            p.naslov.setText(text);
        }
    }

    private void posodobiDodatke() {
        obrokiContainer.getChildren().clear();
        prtljagaContainer.getChildren().clear();

        for (int i = 0; i < potniki.size(); i++) {
            PassengerForm p = potniki.get(i);
            int st = i + 1;

            HBox vrstica = new HBox(10);
            vrstica.setAlignment(javafx.geometry.Pos.CENTER_LEFT);

            Label l = new Label("Potnik " + st + " (" + p.kratekNaziv() + "):");
            l.setMinWidth(180);

            vrstica.getChildren().addAll(l, p.obrokBox);
            obrokiContainer.getChildren().add(vrstica);

            p.prtljagaCheck.setText("Potnik " + st + ": dodatna prtljaga");
            prtljagaContainer.getChildren().add(p.prtljagaCheck);
        }
    }

    @FXML
    private void naprejTab1() {
        posodobiDodatke();
        tabPane.getSelectionModel().select(1);
    }

    @FXML
    private void nazajTab2() {
        tabPane.getSelectionModel().select(0);
    }

    @FXML
    private void naprejTab2() {
        posodobiDodatke();
        tabPane.getSelectionModel().select(2);
    }

    @FXML
    private void nazajTab3() {
        tabPane.getSelectionModel().select(1);
    }

    @FXML
    private void naprejTab3() {
        posodobiCene();
        tabPane.getSelectionModel().select(3);
    }

    @FXML
    private void nazajTab4() {
        tabPane.getSelectionModel().select(2);
    }

    @FXML
    private void placaj() {
        if (!soPodatkiOk()) {
            opozorilo("Manjkajo podatki", "Izpolnite zahtevana polja pred zaključkom rezervacije.");
            return;
        }

        napolniPovzetek();

        Alert a = new Alert(Alert.AlertType.INFORMATION);
        a.setTitle("Plačilo uspešno");
        a.setHeaderText("Plačilo je bilo uspešno.");
        a.setContentText("Karte in potrdilo so bili poslani na e-poštni naslov.");
        a.showAndWait();

        tabPane.getSelectionModel().select(4);
    }

    @FXML
    private void toggleRentacar() {
        boolean izbran = rentacarCheck.isSelected();

        kategorijaBox.setDisable(!izbran);
        otroskiSedezCheck.setDisable(!izbran);
        modelLabel.setDisable(!izbran);
        rentInfoLabel.setDisable(!izbran);

        if (!izbran) {
            kategorijaBox.getSelectionModel().clearSelection();
            otroskiSedezCheck.setSelected(false);
            modelLabel.setText("");
            rentInfoLabel.setText("Rent-a-car ni izbran.");
        } else {
            rentInfoLabel.setText("Rent-a-car bo rezerviran za obdobje potovanja.");
        }
    }


    private boolean soPodatkiOk() {
        if (potniki.isEmpty()) {
            return false;
        }

        for (PassengerForm p : potniki) {
            if (!p.jeIzpolnjen()) {
                return false;
            }
        }

        return odhodBox.getValue() != null
                && destinacijaBox.getValue() != null
                && razredBox.getValue() != null
                && sedezBox.getValue() != null
                && izbranTipLeta() != null
                && karticaBox.getValue() != null
                && !prazen(imeKarticaField)
                && !prazen(stevilkaKarticaField)
                && !prazen(veljavnostField)
                && !prazen(cvvField);
    }

    private void napolniPovzetek() {
        StringBuilder sb = new StringBuilder();

        for (int i = 0; i < potniki.size(); i++) {
            PassengerForm p = potniki.get(i);

            sb.append("Potnik ").append(i + 1).append(": ")
                    .append(p.polnoIme()).append("\n")
                    .append("Datum rojstva: ").append(p.datumRojstva.getValue().format(fmt)).append("\n")
                    .append("Dokument: ").append(vrednost(p.tipDokumentaBox))
                    .append(", ").append(zakrij(p.dokumentField.getText())).append("\n")
                    .append("Naslov: ").append(p.naslovZaPovzetek()).append("\n\n");
        }

        povzetekPotnikiArea.setText(sb.toString());

        povzetekLet.setText(vrednost(odhodBox) + " → " + vrednost(destinacijaBox) + " (" + izbranTipLeta() + ")");
        povzetekDatum.setText("Odhod: " + datumInterval(odhodOd.getValue(), odhodDo.getValue())
                + " / Povratek: " + datumInterval(povratekOd.getValue(), povratekDo.getValue()));
        povzetekRazred.setText(vrednost(razredBox));
        povzetekSedezi.setText(vrednost(sedezBox));

        povzetekObroki.setText(opisObrokov());
        povzetekPrtljaga.setText(opisPrtljage());
        povzetekAvto.setText(opisAvta());

        povzetekCenaKart.setText(cenaKart() + " €");
        povzetekCenaAvto.setText(rentacarCheck.isSelected() ? cenaAvta() + " €" : "Ni izbran");

        String kartica = stevilkaKarticaField.getText().replaceAll(" ", "");
        povzetekKartica.setText(zakrijKartico(kartica));

        emailPoslanLabel.setText("Karte in potrdilo so bili poslani na: " + potniki.get(0).emailField.getText().trim());
    }

    private void posodobiCene() {
        int karte = cenaKart();
        int avto = cenaAvta();

        cenaKartLabel.setText("Letalske karte: " + (karte > 0 ? karte + " €" : "-"));

        if (rentacarCheck.isSelected()) {
            cenaAvtoLabel.setText("Rent-a-car: " + (avto > 0 ? avto + " €" + " (plačilo ob prevzemu)" : "-"));
        } else {
            cenaAvtoLabel.setText("Rent-a-car: ni izbran");
        }

        skupajDanesLabel.setText("Skupaj danes: " + (karte > 0 ? karte + "€" : "-"));
    }

    private int cenaKart() {
        if (razredBox.getValue() == null) {
            return 0;
        }

        int cena = potniki.size() * 200;

        if ("Poslovni".equals(razredBox.getValue())) {
            cena += potniki.size() * 300;
        } else if ("Prvi razred".equals(razredBox.getValue())) {
            cena += potniki.size() * 400;
        }

        if (direktenRadio.isSelected()) {
            cena += potniki.size() * 80;
        }

        cena += steviloDodatnihPrtljag() * 40;
        return cena;
    }

    private int cenaAvta() {
        if (!rentacarCheck.isSelected() || kategorijaBox.getValue() == null) {
            return 0;
        }

        return 150;
    }


    private int steviloDodatnihPrtljag() {
        int st = 0;

        for (PassengerForm p : potniki) {
            if (p.prtljagaCheck.isSelected()) {
                st++;
            }
        }

        return st;
    }

    private String opisObrokov() {
        StringBuilder sb = new StringBuilder();

        for (int i = 0; i < potniki.size(); i++) {
            if (i > 0) {
                sb.append(", ");
            }

            sb.append("Potnik ").append(i + 1).append(": ").append(vrednost(potniki.get(i).obrokBox));
        }

        return sb.toString();
    }

    private String opisPrtljage() {
        StringBuilder sb = new StringBuilder();

        for (int i = 0; i < potniki.size(); i++) {
            if (potniki.get(i).prtljagaCheck.isSelected()) {
                sb.append("Potnik ").append(i + 1).append(", ");
            }
        }

        if (sb.length() == 0) {
            return "Brez dodatne prtljage";
        }

        return "Dodatna prtljaga: " + sb.substring(0, sb.length() - 2);
    }

    private String opisAvta() {
        if (!rentacarCheck.isSelected()) {
            return "Ni izbran";
        }

        String dodatek = otroskiSedezCheck.isSelected() ? ", otroški sedež" : "";
        return vrednost(kategorijaBox) + dodatek;
    }

    private void posodobiModelAvta() {
        if (kategorijaBox.getValue() == null) {
            modelLabel.setText("");
        } else {
            modelLabel.setText("Izbrana kategorija: " + kategorijaBox.getValue());
        }
    }

    private String izbranTipLeta() {
        if (jutranjiRadio.isSelected()) return "jutranji let";
        if (vecerniRadio.isSelected()) return "večerni let";
        if (direktenRadio.isSelected()) return "direkten let";
        return null;
    }

    private String datumInterval(LocalDate od, LocalDate doDatuma) {
        if (od == null && doDatuma == null) return "datum ni izbran";
        if (od != null && doDatuma != null) return od.format(fmt) + " - " + doDatuma.format(fmt);
        if (od != null) return "od " + od.format(fmt);
        return "do " + doDatuma.format(fmt);
    }


    private String vrednost(ComboBox<String> combo) {
        return combo.getValue() == null ? "Ni izbrano" : combo.getValue();
    }

    private boolean prazen(TextField field) {
        return field.getText() == null || field.getText().trim().isEmpty();
    }

    private String zakrij(String s) {
        if (s == null || s.isBlank()) return "Ni vneseno";

        s = s.trim();

        if (s.length() <= 3) return s;

        return "X".repeat(s.length() - 3) + s.substring(s.length() - 3);
    }

    private String zakrijKartico(String s) {
        if (s == null || s.length() < 4) {
            return "XXXX XXXX XXXX XXXX";
        }

        return "XXXX XXXX XXXX " + s.substring(s.length() - 4);
    }


    private void opozorilo(String naslov, String text) {
        Alert a = new Alert(Alert.AlertType.WARNING);
        a.setTitle(naslov);
        a.setHeaderText(null);
        a.setContentText(text);
        a.showAndWait();
    }



    private class PassengerForm {
        boolean glavni;

        VBox root = new VBox(8);
        Label naslov = new Label();

        TextField imeField = new TextField();
        TextField priimekField = new TextField();
        DatePicker datumRojstva = new DatePicker();
        TextField emailField = new TextField();
        ComboBox<String> tipDokumentaBox = new ComboBox<>();
        TextField dokumentField = new TextField();
        TextField naslovField = new TextField();
        CheckBox istiNaslovCheck = new CheckBox("Isti naslov kot glavni potnik");

        ComboBox<String> obrokBox = new ComboBox<>();
        CheckBox prtljagaCheck = new CheckBox();

        PassengerForm(boolean glavni) {
            this.glavni = glavni;


            tipDokumentaBox.getItems().addAll("Potni list", "Osebna izkaznica");
            obrokBox.getItems().addAll("Standardni", "Vegetarijanski", "Otroški", "Brez glutena");

            tipDokumentaBox.setPromptText("Tip dokumenta");
            obrokBox.setPromptText("Izberite obrok");

            if (!glavni) {
                istiNaslovCheck.setSelected(true);
                naslovField.setDisable(true);
            }

            sestavi();
        }

        void sestavi() {
            GridPane g = new GridPane();
            g.setHgap(10);
            g.setVgap(8);

            g.add(new Label("Ime:"), 0, 0);
            g.add(imeField, 1, 0);

            g.add(new Label("Priimek:"), 2, 0);
            g.add(priimekField, 3, 0);

            g.add(new Label("Datum rojstva:"), 0, 1);
            g.add(datumRojstva, 1, 1);

            if (glavni) {
                g.add(new Label("E-pošta:"), 2, 1);
                g.add(emailField, 3, 1);
            }

            g.add(new Label("Tip dokumenta:"), 0, 2);
            g.add(tipDokumentaBox, 1, 2);

            g.add(new Label("Številka dokumenta:"), 2, 2);
            g.add(dokumentField, 3, 2);

            g.add(new Label("Naslov:"), 0, 3);
            g.add(naslovField, 1, 3, 3, 1);

            root.getChildren().addAll(naslov, g);

            if (!glavni) {
                root.getChildren().add(istiNaslovCheck);

                Button odstrani = new Button("Odstrani potnika");
                odstrani.setOnAction(e -> odstraniPotnika(this));

                HBox h = new HBox(10, odstrani);
                h.setAlignment(javafx.geometry.Pos.CENTER_RIGHT);
                root.getChildren().add(h);
            }

            imeField.textProperty().addListener((a, b, c) -> posodobiDodatke());
            priimekField.textProperty().addListener((a, b, c) -> posodobiDodatke());
            obrokBox.setOnAction(e -> posodobiCene());
            prtljagaCheck.setOnAction(e -> posodobiCene());

            istiNaslovCheck.setOnAction(e -> {
                naslovField.setDisable(istiNaslovCheck.isSelected());

                if (istiNaslovCheck.isSelected()) {
                    naslovField.clear();
                }
            });
        }

        boolean jeIzpolnjen() {
            boolean ok = !prazen(imeField)
                    && !prazen(priimekField)
                    && datumRojstva.getValue() != null
                    && tipDokumentaBox.getValue() != null
                    && !prazen(dokumentField);

            if (glavni) {
                return ok && !prazen(emailField) && !prazen(naslovField);
            }

            return ok && (istiNaslovCheck.isSelected() || !prazen(naslovField));
        }

        String polnoIme() {
            return (imeField.getText().trim() + " " + priimekField.getText().trim()).trim();
        }

        String kratekNaziv() {
            String ime = polnoIme();
            return ime.isBlank() ? "brez imena" : ime;
        }

        String naslovZaPovzetek() {
            if (!glavni && istiNaslovCheck.isSelected()) {
                return "Isti naslov kot glavni potnik";
            }

            if (naslovField.getText() == null || naslovField.getText().isBlank()) {
                return "Ni vneseno";
            }

            return naslovField.getText().trim();
        }
    }
}