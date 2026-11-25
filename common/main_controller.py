from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QInputDialog, QMessageBox
from lola_edition import MODES
from common.main_window import MainView
from common.model.datapoints import Model
from common.model.dualocObject import DualocObject
from common.model.matrix_storage import MatrixStorage

# The controller building blocks of the modes in this edition (lola_edition.py); the Research Mode has none yet.
MODE_CONTROLLERS = []
if "education" in MODES:
    from education.controller import EducationController
    MODE_CONTROLLERS.append(EducationController)
if "applied" in MODES:
    from applied.controller import AppliedController
    MODE_CONTROLLERS.append(AppliedController)

class MainController(QObject, *MODE_CONTROLLERS):
    def __init__(self):
        super().__init__()
        # Initialize the data model
        self.model = Model()
        self.modelmatrix = MatrixStorage()
        self.dualocObject = DualocObject()
        # Create the main view and pass the model
        self.view = MainView(self.model, self.modelmatrix, self.dualocObject)
        # Setup signal connections from the view to controller methods
        self.setup_connections()

    def setup_connections(self):
        """
        Connect the signals of the MainView to the handler methods of each mode.
        """
        if "education" in MODES:
            self.connect_education_signals()
        if "applied" in MODES:
            self.connect_applied_signals()

    def show_view(self):
        """
        Simply display the main view.
        """
        self.view.show()

    def _get_delta_from_user(self, parent_window):
        """
        Displays a PyQt5 dialog to get delta value from the user.

        :param parent_window: Parent window for the dialog (can be None)
        :return: Positive float delta value, or None if the user cancels
        """
        while True:
            delta, ok = QInputDialog.getDouble(
                parent_window, "Input Required", "Enter the tolerance value (delta):", decimals=6
            )
            if ok:
                if delta > 0:
                    return delta
                else:
                    QMessageBox.warning(parent_window, "Invalid Input", "Delta must be a positive number!")
            else:
                return None
