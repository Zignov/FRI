package com.example.naloga3;

import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.stage.FileChooser;
import javafx.stage.Stage;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.time.LocalDate;

public class HelloController {

    @FXML private ComboBox<String> drzavaCombo;
    @FXML private ComboBox<String> drzavaNarocnikaCombo;

    @FXML private TextField krajNastanitveField;
    @FXML private TextField imeField;
    @FXML private TextField priimekField;
    @FXML private TextField ulicaField;
    @FXML private TextField postnaStevilkaField;
    @FXML private TextField stevilkaKreditneKarticeField;

    @FXML private DatePicker datumOdhodaPicker;
    @FXML private DatePicker datumVrnitvePicker;
    @FXML private DatePicker datumRojstvaPicker;

    @FXML private Spinner<Integer> odrasliSpinner;
    @FXML private Spinner<Integer> otrociSpinner;
    @FXML private Spinner<Integer> otrociDo7Spinner;

    @FXML private RadioButton letaloRadio;
    @FXML private RadioButton avtobusRadio;
    @FXML private RadioButton koloRadio;
    @FXML private RadioButton vlakRadio;
    @FXML private ToggleGroup prevozGroup;

    @FXML private ToggleGroup nastanitevGroup;

    @FXML private CheckBox wifiCheck;
    @FXML private CheckBox parkirisceVSenciCheck;
    @FXML private CheckBox hladilnikCheck;
    @FXML private CheckBox elektrikaCheck;
    @FXML private CheckBox klimaCheck;
    @FXML private CheckBox posteljninaCheck;
    @FXML private CheckBox blizinaCheck;
    @FXML private CheckBox toplaVodaCheck;

    @FXML private TextArea gostiArea;
    @FXML private Label statusLabel;

    @FXML
    public void initialize() {
        drzavaCombo.getItems().addAll(
                "Slovenija",
                "Hrvaška",
                "Italija",
                "Avstrija",
                "Grčija",
                "Španija"
        );

        drzavaNarocnikaCombo.getItems().addAll(
                "Slovenija",
                "Hrvaška",
                "Italija",
                "Avstrija",
                "Grčija",
                "Španija"
        );

        odrasliSpinner.setValueFactory(
                new SpinnerValueFactory.IntegerSpinnerValueFactory(1, 20, 2));

        otrociSpinner.setValueFactory(
                new SpinnerValueFactory.IntegerSpinnerValueFactory(0, 20, 0));



        otrociDo7Spinner.setValueFactory(
                new SpinnerValueFactory.IntegerSpinnerValueFactory(0, 20, 0));


    }

    @FXML
    private void ponastaviVnose() {
        drzavaCombo.getSelectionModel().clearSelection();
        drzavaNarocnikaCombo.getSelectionModel().clearSelection();

        krajNastanitveField.clear();
        imeField.clear();
        priimekField.clear();
        ulicaField.clear();
        postnaStevilkaField.clear();
        stevilkaKreditneKarticeField.clear();

        datumOdhodaPicker.setValue(null);
        datumVrnitvePicker.setValue(null);
        datumRojstvaPicker.setValue(null);

        prevozGroup.selectToggle(null);
        nastanitevGroup.selectToggle(null);

        wifiCheck.setSelected(false);
        parkirisceVSenciCheck.setSelected(false);
        hladilnikCheck.setSelected(false);
        elektrikaCheck.setSelected(false);
        klimaCheck.setSelected(false);
        posteljninaCheck.setSelected(false);
        blizinaCheck.setSelected(false);
        toplaVodaCheck.setSelected(false);

        odrasliSpinner.getValueFactory().setValue(2);
        otrociSpinner.getValueFactory().setValue(0);
        otrociDo7Spinner.getValueFactory().setValue(0);

        gostiArea.clear();
        statusLabel.setText("Vnosi so bili ponastavljeni.");
    }





    @FXML
    private void shraniVnos() {
        if (!preveriVnos()) {
            return;
        }

        FileChooser fileChooser = new FileChooser();
        fileChooser.setInitialFileName("rezervacija.txt");
        fileChooser.getExtensionFilters().add(
                new FileChooser.ExtensionFilter("Tekstovne datoteke", "*.txt")
        );

        Stage stage = (Stage) imeField.getScene().getWindow();
        File file = fileChooser.showSaveDialog(stage);

        if (file == null) {
            return;
        }

        try (FileWriter writer = new FileWriter(file)) {
            writer.write("Država: " + drzavaCombo.getValue() + "\n");
            writer.write("Kraj: " + krajNastanitveField.getText() + "\n");
            writer.write("Datum odhoda: " + datumOdhodaPicker.getValue() + "\n");
            writer.write("Datum vrnitve: " + datumVrnitvePicker.getValue() + "\n");

            writer.write("Ime: " + imeField.getText() + "\n");
            writer.write("Priimek: " + priimekField.getText() + "\n");
            writer.write("Ulica: " + ulicaField.getText() + "\n");
            writer.write("Poštna številka: " + postnaStevilkaField.getText() + "\n");
            writer.write("Država naročnika: " + drzavaNarocnikaCombo.getValue() + "\n");
            writer.write("Datum rojstva: " + datumRojstvaPicker.getValue() + "\n");
            writer.write("Številka kreditne kartice: " + stevilkaKreditneKarticeField.getText() + "\n");

            writer.write("Prevoz: " + izbranPrevoz() + "\n");
            writer.write("Nastanitev: " + izbranaNastanitev() + "\n");

            writer.write("Odrasli: " + odrasliSpinner.getValue() + "\n");
            writer.write("Otroci: " + otrociSpinner.getValue() + "\n");
            writer.write("Otroci do 7: " + otrociDo7Spinner.getValue() + "\n");

            writer.write("Posebne zahteve: " + posebneZahteve() + "\n");

            writer.write("Podatki gostov:\n");
            writer.write(gostiArea.getText() + "\n");

            showInfo("Uspeh", "Podatki so shranjeni.");
            statusLabel.setText("Vnos uspešno shranjen.");
        } catch (IOException e) {
            showError("Napaka", "Shranjevanje ni uspelo.");
        }
    }

    @FXML
    private void rezerviraj() {
        if (!preveriVnos()) {
            return;
        }

        showInfo("Uspeh", "Rezervacija uspešna.");
        statusLabel.setText("Rezervacija uspešno oddana.");
    }

    private boolean preveriVnos() {
        if (drzavaCombo.getValue() == null ||
                krajNastanitveField.getText().isBlank() ||
                datumOdhodaPicker.getValue() == null ||
                datumVrnitvePicker.getValue() == null ||
                imeField.getText().isBlank() ||
                priimekField.getText().isBlank()) {



            showError("Napaka", "Izpolnite vsa obvezna polja.");
            return false;
        }




        LocalDate odhod = datumOdhodaPicker.getValue();
        LocalDate vrnitev = datumVrnitvePicker.getValue();

        if (!vrnitev.isAfter(odhod)) {
            showError("Napaka", "Datum vrnitve mora biti po datumu odhoda.");
            return false;
        }

        if (!postnaStevilkaField.getText().matches("\\d{4}")) {
            showError("Napaka", "Poštna številka mora imeti 4 številke.");
            return false;
        }

        return true;
    }




    private String izbranPrevoz() {
        if (letaloRadio.isSelected()) return "Letalo";
        if (avtobusRadio.isSelected()) return "Avtobus";
        if (koloRadio.isSelected()) return "Kolo";
        if (vlakRadio.isSelected()) return "Vlak";

        return "Ni izbrano";
    }

    private String izbranaNastanitev() {
        Toggle selected = nastanitevGroup.getSelectedToggle();
        if (selected instanceof RadioButton rb) {
            return rb.getText();
        }
        return "Ni izbrano";
    }



    private String posebneZahteve() {

        StringBuilder sb = new StringBuilder();

        if (wifiCheck.isSelected()) sb.append("WiFi, ");
        if (parkirisceVSenciCheck.isSelected()) sb.append("Parkirišče v senci, ");

        if (hladilnikCheck.isSelected()) sb.append("Hladilnik, ");
        if (elektrikaCheck.isSelected()) sb.append("Elektrika, ");
        if (klimaCheck.isSelected()) sb.append("Klima, ");
        if (posteljninaCheck.isSelected()) sb.append("Posteljnina, ");
        if (blizinaCheck.isSelected()) sb.append("Bližina, ");
        if (toplaVodaCheck.isSelected()) sb.append("Topla voda, ");

        if (sb.length() == 0) {
            return "Ni posebnih zahtev";
        }

        sb.setLength(sb.length() - 2);
        return sb.toString();
    }



    private void showInfo(String title, String text) {
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(text);
        alert.showAndWait();
    }


    private void showError(String title, String text) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(text);
        statusLabel.setText(text);
        alert.showAndWait();
    }
}