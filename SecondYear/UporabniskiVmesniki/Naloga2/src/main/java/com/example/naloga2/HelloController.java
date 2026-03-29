package com.example.naloga2;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.stage.FileChooser;

import java.io.File;


public class HelloController {
    @FXML private ComboBox<String> categoryCombo;
    @FXML private ComboBox<String> fromUnitCombo;
    @FXML private ComboBox<String> toUnitCombo;
    @FXML private TextField displayField;
    @FXML private TextArea historyArea;
    @FXML private TextArea logArea;
    @FXML private Label statusLabel;



    private void updateUnits(){
        //System.out.println("Category: " + categoryCombo.getValue());

        fromUnitCombo.getItems().clear();
        toUnitCombo.getItems().clear();

        String category = categoryCombo.getValue();

        if (category == null){
            return;
        }

        switch (category){
            case "Dolzina":
                fromUnitCombo.getItems().addAll("m", "cm", "in", "ft");
                toUnitCombo.getItems().addAll("m", "cm", "in", "ft");
                break;

            case "Temperatura":
                fromUnitCombo.getItems().addAll("C", "F");
                toUnitCombo.getItems().addAll("C", "F");
                break;

            case "Masa":
                fromUnitCombo.getItems().addAll("kg", "g", "oz");
                toUnitCombo.getItems().addAll("kg", "g", "oz");
                break;

            case "Hitrost":
                fromUnitCombo.getItems().addAll("m/s", "km/h", "mph");
                toUnitCombo.getItems().addAll("m/s", "km/h", "mph");

        }

        fromUnitCombo.getSelectionModel().selectFirst();
        toUnitCombo.getSelectionModel().selectLast();
    }

    @FXML
    private void nextDigit(ActionEvent event){
        Button clickedButton = (Button) event.getSource();
        String digit = clickedButton.getText();
        displayField.appendText(digit);
    }

    @FXML
    private void handleDecimalPoint(){
        if(!displayField.getText().contains(".")){
            if(displayField.getText().isEmpty()){
                displayField.setText("0.");
            }
            else{
                displayField.appendText(".");
            }
        }
    }

    @FXML
    private void handleBack(){
        String text = displayField.getText();

        if(!text.isEmpty()){
            displayField.setText(text.substring(0, text.length()-1));
            statusLabel.setText("Nazaj");
            logArea.appendText("Brisanje zadnje cifre.\n");
        }
    }



    private double convert(double value, String category, String from, String to){
        switch (category){
            case "Dolzina":
                return convertDolzina(value, from, to);
            case "Temperatura":
                return convertTemp(value, from, to);
            case "Masa":
                return convertMass(value, from, to);
            case "Hitrost":
                return convertHitrost(value, from, to);

            default:
                return value;
        }
    }

    private double convertDolzina(double value, String from, String to){
        double meters;

        switch (from){
            case "m":
                meters = value;
                break;
            case "cm":
                meters = value/100.0;
                break;
            case "in":
                meters = value * 0.0254;
                break;
            case "ft":
                meters = value * 0.3048;
                break;
            default:
                meters = value;
        }

        return switch (to) {
            case "m" -> meters;
            case "cm" -> meters * 100.0;
            case "in" -> meters / 0.0254;
            case "ft" -> meters / 0.3048;
            default -> meters;
        };
    }


    private double convertTemp(double value, String from, String to){
        if (from.equals(to)) {
            return value;
        }

        if (from.equals("C") && to.equals("F")) {
            return (value * 9 / 5) + 32;
        }

        if (from.equals("F") && to.equals("C")) {
            return (value - 32) * 5 / 9;
        }

        return value;
    }

    private double convertMass(double value, String from, String to){
        double kilograms;

        switch(from){
            case "kg":
                kilograms = value;
                break;
            case "g":
                kilograms = value/1000.0;
                break;
            case "oz":
                kilograms = value * 0.0283495;
                break;
            default:
                kilograms = value;
                break;
        }

        return switch(to) {
            case "kg" -> kilograms;
            case "g" -> kilograms * 1000.0;
            case "oz" -> kilograms / 0.0283495;
            default -> kilograms;
        };

    }

    private double convertHitrost(double value, String from, String to){
        double ms;

        switch (from) {
            case "m/s":
                ms = value;
                break;
            case "km/h":
                ms = value / 3.6;
                break;
            case "mph":
                ms = value * 0.44704;
                break;
            default:
                ms = value;
        }

        return switch (to) {
            case "m/s" -> ms;
            case "km/h" -> ms * 3.6;
            case "mph" -> ms / 0.44704;
            default -> ms;
        };
    }

    @FXML
    private void handleConversion(){

        String text = displayField.getText();

        if (text.isEmpty()) {
            statusLabel.setText("Vnos je prazen.");
            logArea.appendText("Napaka: prazen vnos.\n");
            return;
        }

        String category = categoryCombo.getValue();
        String toUnit = toUnitCombo.getValue();
        String fromUnit = fromUnitCombo.getValue();

        if(category == null || fromUnit == null || toUnit == null){
            statusLabel.setText("Izberi kategorijo in enoti.");
            logArea.appendText("Napaka: manjkajoča izbira kategorije ali enot.\n");
            return;
        }

        double value;
        try {
            value = Double.parseDouble(text);
        } catch (NumberFormatException e) {
            statusLabel.setText("Neveljaven vnos.");
            logArea.appendText("Napaka: neveljaven številčni vnos.\n");
            return;
        }

        double result = Math.round(convert(value, category, fromUnit, toUnit) * 100.0) / 100.0;
        String record = value + " " + fromUnit + " -> " + result + " " + toUnit;


        displayField.setText(String.valueOf(result));
        historyArea.appendText(record + "\n");
        logArea.appendText("Pretvorba izvedena: " + record + "\n");
        statusLabel.setText("Uspešna pretvorba: " + record);
    }



    @FXML
    private void handleClear() {
        displayField.clear();
        historyArea.clear();
        statusLabel.setText("Vnos in zgodovina sta pobrisana.");
        logArea.appendText("Uporabnik je pobrisal vnos in zgodovino.\n");
    }


    @FXML
    private void handleExit(){
        logArea.appendText("Zahteva za zapiranje aplikacije.\n");
        statusLabel.setText("Aplikacija se zapira.");
        System.exit(0);
    }


    public void odpriCB(ActionEvent actionEvent) {
        FileChooser fc = new FileChooser();
        File file = fc.showOpenDialog(null);

        if (file != null) {
            try {
                historyArea.setText(java.nio.file.Files.readString(file.toPath()));

                long size = file.length();
                statusLabel.setText("Odprta: " + file.getName() + " (" + size + " B)");
                logArea.appendText("Odprta datoteka: " + file.getName() + " (" + size + " B)\n");

            } catch (Exception ex) {
                statusLabel.setText("Napaka pri odpiranju.");
                logArea.appendText("Napaka pri odpiranju datoteke.\n");
            }
        }
    }

    @FXML
    public void shraniCB(ActionEvent actionEvent) {
        FileChooser fc = new FileChooser();
        fc.setTitle("Shrani datoteko");

        fc.setInitialFileName("zgodovina.txt");

        File file = fc.showSaveDialog(null);

        if (file != null) {
            try (java.io.PrintWriter writer = new java.io.PrintWriter(file)) {
                writer.write(historyArea.getText());

                statusLabel.setText("Shranjeno: " + file.getName());
                logArea.appendText("Shranjena datoteka: " + file.getName() + "\n");

            } catch (Exception e) {
                statusLabel.setText("Napaka pri shranjevanju.");
                logArea.appendText("Napaka pri shranjevanju datoteke.\n");
            }
        }
    }

    @FXML
    private void handleDel(){
        displayField.clear();
        statusLabel.setText("Vnos pobrisan.");
        logArea.appendText("Brisanje trenutnega vnosa.\n");
    }


    @FXML
    private void handleAuthor() {
        String authorInfo = "Ziga Nova, 2. letnik, VSŠ";
        statusLabel.setText(authorInfo);
        logArea.appendText("Prikazani podatki o avtorju.\n");
    }


    @FXML
    public void initialize(){
        categoryCombo.getItems().addAll("Dolzina", "Temperatura", "Masa", "Hitrost");
        categoryCombo.setOnAction(e -> updateUnits());
    }
}