package com.example.naloga1_3;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.stage.FileChooser;

import java.io.File;

public class HelloController {

    @FXML
    private CheckMenuItem imeMenuItem;

    @FXML
    private CheckMenuItem tipMenuItem;

    @FXML
    private CheckMenuItem terminMenuItem;

    @FXML
    private ComboBox<String> rezervacijeCombo;

    @FXML
    private RadioButton prijavaRadio;

    @FXML
    private RadioButton odjavaRadio;

    @FXML
    private RadioButton spremeniRadio;

    @FXML
    private Spinner<Integer> pozicijaSpinner;

    @FXML
    private TextArea izpisArea;

    @FXML
    private Label sporociloLabel;


    @FXML
    private TextField imeField;

    @FXML
    private TextField tipField;

    @FXML
    private TextField terminField;

    @FXML private Label statusLabel;

    @FXML
    private void izhodRA() {
        System.exit(0);
    }

    @FXML
    private void urediImeRA() {
        imeField.setDisable(!imeMenuItem.isSelected());
        statusLabel.setText("Urejanje imena");
    }

    @FXML
    private void urediTipRA() {
        tipField.setDisable(!tipMenuItem.isSelected());
        statusLabel.setText("Urejanje tipa");
    }

    @FXML
    private void urediTerminRA() {
        terminField.setDisable(!terminMenuItem.isSelected());
        statusLabel.setText("Urejanje termina");

    }


    @FXML
    public void odpriRA(ActionEvent actionEvent) {
        FileChooser fc = new FileChooser();
        File f = fc.showOpenDialog(null);
        if (f!=null)
            statusLabel.setText("Datoteka: " + f.getName());
    }



    @FXML
    private void comboBoxChanged() {
        String izbrano = rezervacijeCombo.getValue();

        if (izbrano == null || izbrano.isEmpty()) {
            return;
        }

        String[] parts = izbrano.split(";");

        if (parts.length >= 3) {
            imeField.setText(parts[0].trim());
            tipField.setText(parts[1].trim());
            terminField.setText(parts[2].trim());
        }
    }


    @FXML
    private void pobrisiRA() {
        statusLabel.setText("");
        sporociloLabel.setText("");
        izpisArea.setText("");
    }


    @FXML
    private void izpisiVseRA() {
        StringBuilder sb = new StringBuilder();

        for (String item : rezervacijeCombo.getItems()) {
            sb.append(item).append("\n");
        }

        izpisArea.setText(sb.toString());
        statusLabel.setText("Izpisujem vse rezervacije");
    }




    @FXML
    private void izvediAkcijoRA() {
        if (prijavaRadio.isSelected()) {

            if (!imeField.isDisabled() && !tipField.isDisabled() && !terminField.isDisabled()
                    && !imeField.getText().isBlank()
                    && !tipField.getText().isBlank()
                    && !terminField.getText().isBlank()) {



                String novVnos = imeField.getText().trim() + "; "
                        + tipField.getText().trim() + "; "
                        + terminField.getText().trim();

                if (!rezervacijeCombo.getItems().contains(novVnos)) {
                    rezervacijeCombo.getItems().add(novVnos);
                    rezervacijeCombo.setValue(novVnos);
                    sporociloLabel.setText("Prijavljam udelezenca");
                }
            }

        } else if (odjavaRadio.isSelected()) {

            String selected = rezervacijeCombo.getValue();
            if (selected != null) {
                rezervacijeCombo.getItems().remove(selected);
                sporociloLabel.setText("Odjavljam udelezenca");


                if (!rezervacijeCombo.getItems().isEmpty()) {
                    rezervacijeCombo.getSelectionModel().selectFirst();
                    comboBoxChanged();
                } else {
                    imeField.clear();
                    tipField.clear();
                    terminField.clear();
                }
            }

        } else if (spremeniRadio.isSelected()) {

            String selected = rezervacijeCombo.getValue();
            int index = rezervacijeCombo.getSelectionModel().getSelectedIndex();

            if (selected != null && index >= 0 &&
                    (!imeField.isDisabled() || !tipField.isDisabled() || !terminField.isDisabled()))  {

                sporociloLabel.setText("Spreminjam termin");
                String novVnos = imeField.getText().trim() + "; "
                        + tipField.getText().trim() + "; "
                        + terminField.getText().trim();

                rezervacijeCombo.getItems().set(index, novVnos);
                rezervacijeCombo.getSelectionModel().select(index);
            }
        }
    }



    @FXML
    private void initialize(){
        rezervacijeCombo.getItems().add("Ziga; Odbojka; Sreda 16:30");
        rezervacijeCombo.getSelectionModel().selectFirst();

        SpinnerValueFactory.IntegerSpinnerValueFactory valueFactory = new SpinnerValueFactory.IntegerSpinnerValueFactory(0, 20, 0);
        pozicijaSpinner.setValueFactory(valueFactory);

        pozicijaSpinner.valueProperty().addListener((obs, oldValue, newValue) -> {
            if (newValue >= 0 && newValue < rezervacijeCombo.getItems().size()) {
                sporociloLabel.setText(rezervacijeCombo.getItems().get(newValue));
            } else {
                sporociloLabel.setText("Ni elementa");
            }
        });

        comboBoxChanged();
    }

}