from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)


class InterchangeStartSolutionDialog(QDialog):
    """
    Dialog for entering an initial feasible solution
    for the Interchange heuristic.
    """

    def __init__(self, num_facilities, parent=None):
        super().__init__(parent)

        self.num_facilities = num_facilities
        self.opened_facilities = []

        self.setWindowTitle("Interchange Start Solution")
        self.setFixedWidth(400)

        layout = QVBoxLayout(self)

        info_label = QLabel(
            f"Enter the IDs of the opened facilities "
            f"(1 to {num_facilities}).\n"
            f"Example: 1, 3, 5"
        )
        layout.addWidget(info_label)

        self.facilities_input = QLineEdit()
        self.facilities_input.setPlaceholderText("e.g. 1, 3, 5")
        layout.addWidget(self.facilities_input)

        button_layout = QHBoxLayout()

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.validate_and_save)

        button_layout.addWidget(cancel_button)
        button_layout.addWidget(save_button)

        layout.addLayout(button_layout)

    def validate_and_save(self):
        text = self.facilities_input.text().strip()

        if not text:
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Please enter at least one facility."
            )
            return

        try:
            facilities = [
                int(value.strip())
                for value in text.split(",")
            ]
        except ValueError:
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Please enter facility IDs separated by commas."
            )
            return

        # No duplicates
        if len(facilities) != len(set(facilities)):
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Please enter each facility only once."
            )
            return

        # Check range
        invalid_facilities = [
            facility
            for facility in facilities
            if facility < 1 or facility > self.num_facilities
        ]

        if invalid_facilities:
            QMessageBox.warning(
                self,
                "Invalid Input",
                f"Facility IDs must be between 1 and "
                f"{self.num_facilities}."
            )
            return

        self.opened_facilities = facilities
        self.accept()