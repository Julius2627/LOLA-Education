"""Education Mode: the pages this mode adds to the main window.

Planar, network and discrete facility location problems and districting for teaching.
"""
import math

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QDoubleSpinBox, QFrame, QGroupBox, QHBoxLayout, QHeaderView,
                             QLabel, QLineEdit, QPushButton, QSizePolicy, QSpinBox, QTableWidget, QTableWidgetItem,
                             QTextEdit, QVBoxLayout, QWidget)

from common.graph_functions import ParetoFrontView, PlotCanvas
from common.ui_helpers import ui_font


class EducationPages:
    """Building block of the main window (MainView) for the Education Mode.

    Uses from the main window: stackedLayout, update_breadcrumb, show_mode_selection,
    show_network_type_selection, network_type_name, datapoints_model and modelmatrix.
    """

    planar_education_run_algo_signal = pyqtSignal()
    planar_education_manual_input_signal = pyqtSignal()
    planar_education_remove_marker_signal = pyqtSignal()
    planar_education_back_signal = pyqtSignal()
    planar_education_dataset_changed = pyqtSignal(str)
    planar_education_random_instance_signal = pyqtSignal()
    network_education_matrix_signal = pyqtSignal()
    network_education_graph_signal = pyqtSignal()
    network_education_reset_signal = pyqtSignal()
    network_education_run_algo_signal = pyqtSignal()
    network_education_back_signal = pyqtSignal()
    network_education_algo_changed_signal = pyqtSignal(str)
    network_education_example_changed_signal = pyqtSignal(str)
    network_education_random_instance_signal = pyqtSignal()
    dualoc_dataset_changed = pyqtSignal(str)
    dualoc_run_algo_signal = pyqtSignal()
    dualoc_back_signal = pyqtSignal()
    dualoc_random_instance_signal = pyqtSignal()
    dualoc_save_matrix_signal = pyqtSignal()
    dualoc_solve_signal = pyqtSignal(str)
    create_matrix_dualoc_signal = pyqtSignal()
    discrete_education_reset_signal = pyqtSignal()
    districting_education_dataset_changed = pyqtSignal(str)
    districting_education_create_table_signal = pyqtSignal()
    districting_education_random_instance_signal = pyqtSignal()
    districting_education_table_changed_signal = pyqtSignal()
    districting_education_run_algo_signal = pyqtSignal()
    districting_education_reset_signal = pyqtSignal()

    def setup_education_pages(self):
        '______________________________________________________________________________________________________________'
        # Page 4: Options for Education Mode (placeholder, navigation only)
        self.page_education = QWidget()
        layout_education = QVBoxLayout(self.page_education)
        layout_education_buttons = QHBoxLayout()
        btn_planar_education = QPushButton("Planar")
        btn_planar_education.setFont(ui_font(20))
        btn_planar_education.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn_planar_education.clicked.connect(self.show_planar_education_page)
        btn_network_education = QPushButton("Network")
        btn_network_education.setFont(ui_font(20))
        btn_network_education.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn_network_education.clicked.connect(self.show_network_type_selection)
        btn_discrete_education = QPushButton("Discrete")
        btn_discrete_education.setFont(ui_font(20))
        btn_discrete_education.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn_discrete_education.clicked.connect(self.show_discrete_education_options)
        btn_districting_education = QPushButton("Districting")
        btn_districting_education.setFont(ui_font(20))
        btn_districting_education.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn_districting_education.clicked.connect(self.show_districting_education_page)

        layout_education_buttons.addWidget(btn_planar_education)
        layout_education_buttons.addWidget(btn_network_education)
        layout_education_buttons.addWidget(btn_discrete_education)
        layout_education_buttons.addWidget(btn_districting_education)
        layout_education.addLayout(layout_education_buttons)
        back_education = QPushButton("Back")
        back_education.setStyleSheet("background-color: red; color: white;")
        back_education.clicked.connect(self.show_mode_selection)
        layout_education.addWidget(back_education)
        self.stackedLayout.addWidget(self.page_education)
        '______________________________________________________________________________________________________________'
        # Page 5: Integrated Planar Education Mode Page (Layout and PlotCanvas)
        self.page_planar_education = QWidget()
        layout_planar_education = QHBoxLayout(self.page_planar_education)

        # Left side: PlotCanvas (for graph) – takes 1/3 of the width
        self.planar_education_plot_canvas = PlotCanvas(self, width=5, height=4)
        layout_planar_education.addWidget(self.planar_education_plot_canvas, 1)

        # Right side: Control panel (takes 2/3 of the width)
        planar_education_control_panel = QVBoxLayout()

        # Title label
        planar_education_title = QLabel("Planar Facility Problems - Education Mode")
        planar_education_title.setFont(ui_font(20))
        planar_education_control_panel.addWidget(planar_education_title)

        # Instance selection
        planar_education_instance_layout = QHBoxLayout()

        self.planar_education_own_instance_button = QPushButton("Own Instance")
        self.planar_education_example_instance_button = QPushButton("Example Instance")
        self.planar_education_random_instance_button = QPushButton("Random Instance")

        # Random Instance Widget
        self.planar_education_random_widget = QWidget()
        planar_education_random_layout = QHBoxLayout(
            self.planar_education_random_widget
        )

        self.planar_education_random_points_label = QLabel("Number of points:")

        self.planar_education_random_points_input = QLineEdit()
        self.planar_education_random_points_input.setPlaceholderText("1-10")

        self.planar_education_generate_random_button = QPushButton(
            "Generate"
        )

        self.planar_education_generate_random_button.clicked.connect(lambda: self.planar_education_random_instance_signal.emit())

        planar_education_random_layout.addWidget(
            self.planar_education_random_points_label
        )
        planar_education_random_layout.addWidget(
            self.planar_education_random_points_input
        )
        planar_education_random_layout.addWidget(
            self.planar_education_generate_random_button
        )

        

        # Initially hidden
        self.planar_education_random_widget.hide()

        planar_education_instance_layout.addWidget(
            self.planar_education_own_instance_button
        )
        planar_education_instance_layout.addWidget(
            self.planar_education_example_instance_button
        )
        planar_education_instance_layout.addWidget(
            self.planar_education_random_instance_button
        )

        planar_education_control_panel.addLayout(
            planar_education_instance_layout
        )

        planar_education_control_panel.addWidget(
            self.planar_education_random_widget
        )

        self.planar_education_combo_algos = QComboBox()
        self.planar_education_combo_algos.addItem("Please Select Algorithm...")
        self.planar_education_combo_algos.addItem("Median l1 Metric Unweighted")
        self.planar_education_combo_algos.addItem("Median l1 Metric Weighted")
        self.planar_education_combo_algos.addItem("Median l2 Metric Weighted")
        self.planar_education_combo_algos.addItem("Median l2 Squared Weighted")
        self.planar_education_combo_algos.addItem("Center l1 Metric Unweighted")
        self.planar_education_combo_algos.addItem("Center l1 Metric Weighted")
        self.planar_education_combo_algos.addItem("Center l2 Metric Unweighted")
        self.planar_education_combo_algos.addItem("Center l∞ Metric Unweighted")
        self.planar_education_combo_algos.addItem("Center l∞ Metric Weighted")

        planar_education_control_panel.addWidget(self.planar_education_combo_algos)

        # Example Instance
        self.planar_education_combo_datasets = QComboBox()
        self.planar_education_combo_datasets.addItem("Please Select Dataset...")
        self.planar_education_combo_datasets.addItems(self.datapoints_model.list_datasets(education_only=True))

        planar_education_control_panel.addWidget(
            self.planar_education_combo_datasets
        )

        # Initially hidden
        self.planar_education_combo_datasets.hide()

        self.planar_education_combo_datasets.currentTextChanged.connect(
            lambda text: self.planar_education_dataset_changed.emit(text)
        )

        self.planar_education_own_instance_button.clicked.connect(
            lambda: self.show_planar_education_own_instance()
        )

        self.planar_education_example_instance_button.clicked.connect(
            lambda: self.show_planar_education_example_instance()
        )

        self.planar_education_random_instance_button.clicked.connect(
            lambda: self.show_planar_education_random_instance()
        )

        # Coordinates display
        self.planar_education_label_coords = QLabel("Coordinates (x, y, weight):")
        planar_education_control_panel.addWidget(self.planar_education_label_coords)
        self.planar_education_text_coords = QTextEdit()
        self.planar_education_text_coords.setReadOnly(True)
        planar_education_control_panel.addWidget(self.planar_education_text_coords)

        # Layout for the solution path checkbox
        planar_education_panel_path = QHBoxLayout()
        self.planar_education_show_solution_checkbox = QCheckBox("Show Solution Path")
        self.planar_education_show_solution_checkbox.setStyleSheet("QCheckBox::indicator { width: 25px; height: 25px; }")

        planar_education_panel_path.addWidget(self.planar_education_show_solution_checkbox)
        planar_education_control_panel.addLayout(planar_education_panel_path)

        # Run Algorithm button – signal emission (to be handled by the controller)
        self.planar_education_run_algo_button = QPushButton("Run Algorithm")
        planar_education_control_panel.addWidget(self.planar_education_run_algo_button)
        self.planar_education_run_algo_button.clicked.connect(lambda: self.planar_education_run_algo_signal.emit())
        

        # Additional action buttons
        planar_education_button_layout = QHBoxLayout()
        self.planar_education_remove_markers_button = QPushButton("Remove All Markers")
        self.planar_education_back_button = QPushButton("Back")
        self.planar_education_back_button.setStyleSheet("background-color: red; color: white;")
        # Back button navigates back to the mode selection page.
        self.planar_education_back_button.clicked.connect(self.show_education_options)
        self.planar_education_back_button.clicked.connect(lambda: self.planar_education_back_signal.emit())
        self.planar_education_remove_markers_button.clicked.connect(lambda: self.planar_education_remove_marker_signal.emit())

        planar_education_button_layout.addWidget(self.planar_education_remove_markers_button)
        planar_education_button_layout.addWidget(self.planar_education_back_button)
        planar_education_control_panel.addLayout(planar_education_button_layout)

        # Add the control panel to the layout with a stretch factor of 1.
        layout_planar_education.addLayout(planar_education_control_panel, 1)

        # Add the new page to the stacked layout.
        self.stackedLayout.addWidget(self.page_planar_education)
        '______________________________________________________________________________________________________________'
        # Page 6: Integrated Network Education Mode Page
        self.page_network_education = QWidget(self)
        layout_network_education = QHBoxLayout(self.page_network_education)

        #auxiliary lables to get two mode option!
        self.help_label_1 = QLabel("")
        self.help_label_2 = QLabel("")
        layout_network_education.addWidget(self.help_label_1, 1)

        # Left side: PlotCanvas for graph (takes 1/3 of the width)
        self.network_education_plot_canvas = PlotCanvas(self, width=5, height=4)
        self.network_education_plot_canvas.show_network_default_axes()
        layout_network_education.addWidget(self.network_education_plot_canvas, 2)

        # Right side: Control panel (takes 2/3 of the width)
        self.control_frame = QFrame()
        self.control_frame.setFrameShape(QFrame.StyledPanel)

        network_education_control_panel = QVBoxLayout()
        self.control_frame.setLayout(network_education_control_panel)

        # Title label
        network_education_title = QLabel("Network Facility Problems - Education Mode")
        network_education_title.setFont(ui_font(20))
        network_education_control_panel.addWidget(network_education_title, 2)

        # Instance selection
        network_education_instance_layout = QHBoxLayout()

        self.network_education_own_instance_button = QPushButton("Own Instance")
        self.network_education_example_instance_button = QPushButton("Example Instance")
        self.network_education_random_instance_button = QPushButton("Random Instance")

        network_education_instance_layout.addWidget(self.network_education_own_instance_button)
        network_education_instance_layout.addWidget(self.network_education_example_instance_button)
        network_education_instance_layout.addWidget(self.network_education_random_instance_button)

        network_education_control_panel.addLayout(network_education_instance_layout, 1)

        # Random Instance Widget
        self.network_education_random_widget = QWidget()

        network_education_random_layout = QHBoxLayout(self.network_education_random_widget)

        # Number of nodes
        self.network_education_random_nodes_label = QLabel("Number of nodes:")

        self.network_education_random_nodes_input = QLineEdit()
        self.network_education_random_nodes_input.setPlaceholderText("2-10")

        # Number of weight vectors (several: Pareto median)
        self.network_education_random_weights_label = QLabel("Number of weight vectors:")

        self.network_education_random_weights_input = QLineEdit()
        self.network_education_random_weights_input.setText("1")

        # Generate
        self.network_education_generate_random_button = QPushButton(
            "Generate"
        )

        self.network_education_generate_random_button.clicked.connect(
            lambda: self.network_education_random_instance_signal.emit()
        )

        network_education_random_layout.addWidget(
            self.network_education_random_nodes_label
        )

        network_education_random_layout.addWidget(
            self.network_education_random_nodes_input
        )

        network_education_random_layout.addWidget(
            self.network_education_random_weights_label
        )

        network_education_random_layout.addWidget(
            self.network_education_random_weights_input
        )

    
        network_education_random_layout.addWidget(
            self.network_education_generate_random_button
        )

        network_education_control_panel.addWidget(
            self.network_education_random_widget
        )

        # Initially hidden
        self.network_education_random_widget.hide()

        # Own Instance Widget
        self.network_education_own_instance_widget = QWidget()
        network_education_own_instance_layout = QVBoxLayout(
            self.network_education_own_instance_widget
        )

        # Nodes input
        self.network_education_nodes_label = QLabel("How many nodes?")
        network_education_own_instance_layout.addWidget(
            self.network_education_nodes_label
        )

        self.network_education_nodes_input = QLineEdit()
        network_education_own_instance_layout.addWidget(
            self.network_education_nodes_input
        )

        # Number of weights input
        self.network_education_weights_label = QLabel("How many weights?")
        network_education_own_instance_layout.addWidget(
            self.network_education_weights_label
        )

        self.network_education_weights_input = QLineEdit()
        self.network_education_weights_input.setText("1")
        network_education_own_instance_layout.addWidget(
            self.network_education_weights_input
        )

        # Create matrix button + info
        network_education_create_info_layout = QHBoxLayout()

        self.network_education_matrix_button = QPushButton(
            "Create Adjacency Matrix"
        )
        self.network_education_matrix_button.clicked.connect(
            lambda: self.network_education_matrix_signal.emit()
        )


        network_education_create_info_layout.addWidget(
            self.network_education_matrix_button, 8
        )

        self.network_education_info_label = QLabel("\u2139")
        self.network_education_info_label.setAlignment(Qt.AlignCenter)
        self.network_education_info_label.setFixedSize(20, 20)
        self.network_education_info_label.setStyleSheet(
            """QLabel {
                    background-color: #e0e0e0;
                    border-radius: 10px;
                    border: 1px solid #888;
                    color: #000;
                }"""
        )

        self.network_education_info_label.setToolTip(
            "n or empty indicates no connection between nodes!"
        )

        network_education_create_info_layout.addWidget(
            self.network_education_info_label, 1
        )

        network_education_own_instance_layout.addLayout(
            network_education_create_info_layout
        )

        network_education_control_panel.addWidget(
            self.network_education_own_instance_widget
        )

        # Initially hidden
        self.network_education_own_instance_widget.hide()

        # Example Instance
        self.network_education_example_combo = QComboBox()
        self.network_education_example_combo.addItem("Please Select Example...")

        # Add available network examples
        network_examples = self.datapoints_model.list_network_problems(max_nodes=10, education_only=True)   # at most 10 nodes
        self.network_education_example_combo.addItems(network_examples)

        network_education_control_panel.addWidget(
            self.network_education_example_combo
        )

        # Initially hidden
        self.network_education_example_combo.hide()


        self.network_education_example_combo.currentTextChanged.connect(
            lambda text: self.network_education_example_changed_signal.emit(text)
        )
        
        self.network_education_own_instance_button.clicked.connect(
            self.show_network_education_own_instance
        )

        self.network_education_example_instance_button.clicked.connect(
            lambda: self.show_network_education_example_instance()
        )
        
        self.network_education_random_instance_button.clicked.connect(lambda: self.show_network_education_random_instance())

        # Adjacency matrix table (falls benötigt)
        self.network_education_matrix_table = QTableWidget()
        network_education_control_panel.addWidget(self.network_education_matrix_table, 15)

        # solutionpath Label (anstelle von Adjacency matrix table)
        self.network_education_solution_label = QTextEdit("")
        self.network_education_solution_label.setReadOnly(True)
        network_education_control_panel.addWidget(self.network_education_solution_label, 15)
        self.network_education_solution_label.setVisible(False)

        # Pareto front (after a Pareto median with two weight vectors), shown instead of the matrix or the solution box
        self.network_education_front_view = ParetoFrontView(self)
        network_education_control_panel.addWidget(self.network_education_front_view, 15)
        self.network_education_front_view.setVisible(False)

        # Button: Show Graph
        self.network_education_graph_button = QPushButton("Save Matrix")
        self.network_education_graph_button.clicked.connect(lambda: self.network_education_graph_signal.emit())
        network_education_control_panel.addWidget(self.network_education_graph_button, 1)

        # ComboBox for algorithm selection
        self.network_education_combo_algos = QComboBox()
        self.network_education_combo_algos.addItem("Please Select Algorithm...")

        network_education_control_panel.addWidget(self.network_education_combo_algos, 1)
        self.network_education_combo_algos.currentTextChanged.connect(lambda text: self.network_education_algo_changed_signal.emit(text))

        network_education_checkboxes = QHBoxLayout()
        self.network_education_show_solution_checkbox = QCheckBox("Show Solution Path")
        self.network_education_show_solution_checkbox.setStyleSheet(
            "QCheckBox::indicator { width: 25px; height: 25px; }")
        network_education_checkboxes.addWidget(self.network_education_show_solution_checkbox)
        #network_education_checkboxes.addWidget(QLabel(""))
        self.network_education_graph_checkbox = QCheckBox("Graph View")
        self.network_education_graph_checkbox.setStyleSheet(
            "QCheckBox::indicator { width: 25px; height: 25px; }")
        self.network_education_graph_checkbox.setChecked(True)
        self.network_education_graph_checkbox.clicked.connect(lambda: self.update_network_education_graph_view())
        network_education_checkboxes.addWidget(self.network_education_graph_checkbox)
        self.network_education_matrix_solution_switch = QPushButton("Adjacency Matrix / Solution Box")
        network_education_checkboxes.addWidget(self.network_education_matrix_solution_switch)
        self.network_education_matrix_solution_switch.clicked.connect(lambda: self.network_education_switch_matrix_solutionBox())
        self.network_education_front_button = QPushButton("Pareto Front")     # only after a Pareto run with Q = 2
        self.network_education_front_button.setVisible(False)
        self.network_education_front_button.clicked.connect(self.network_education_show_front)
        network_education_checkboxes.addWidget(self.network_education_front_button)

        network_education_control_panel.addLayout(network_education_checkboxes, 1)

        # Now the four buttons, whose signals are handled in the controller:
        self.network_education_run_algo_button = QPushButton("Run Algorithm")
        self.network_education_reset_button = QPushButton("Reset")
        # Back button is handled directly in the view:
        self.network_education_back_button = QPushButton("Back")
        self.network_education_back_button.setStyleSheet("background-color: red; color: white;")
        self.network_education_back_button.clicked.connect(self.show_education_options)
        self.network_education_back_button.clicked.connect(lambda: self.network_education_back_signal.emit())

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.network_education_run_algo_button)
        button_layout.addWidget(self.network_education_reset_button)
        button_layout.addWidget(self.network_education_back_button)
        network_education_control_panel.addLayout(button_layout, 1)

        # Emit signals on run and reset button clicks:
        self.network_education_run_algo_button.clicked.connect(lambda: self.network_education_run_algo_signal.emit())
        self.network_education_reset_button.clicked.connect(lambda: self.network_education_reset_signal.emit())

        # Add the control panel to the layout with a stretch factor of 1.
        layout_network_education.addWidget(self.control_frame, 2)
        layout_network_education.addWidget(self.help_label_2, 1)
        self.stackedLayout.addWidget(self.page_network_education)
        '______________________________________________________________________________________________________________'
        # Page 7: Page for Education Mode Discrete Problems
        # Page XX: Discrete Education Mode Page (analogous to Planar Education)
        # named dualoc because previously it has been the only algorithm available
        self.page_dualoc_education = QWidget()
        self.stackedLayout.addWidget(self.page_dualoc_education)

        # Main Layout Dualoc page (centered main widget, not full width)
        self.layout_centering = QHBoxLayout()
        self.page_dualoc_education.setLayout(self.layout_centering)
        layout_dualoc = QVBoxLayout()
        self.dualoc_main_widget = QWidget()
        self.dualoc_main_widget.setLayout(layout_dualoc)
        self.help_label_dualoc_1 = QLabel("")
        self.help_label_dualoc_2 = QLabel("")
        self.layout_centering.addWidget(self.help_label_dualoc_1, 1)
        self.layout_centering.addWidget(self.dualoc_main_widget, 2) 
        self.layout_centering.addWidget(self.help_label_dualoc_2, 1)

        # Title, nothing changes ever
        dualoc_title = QLabel("Discrete Facility Problems - Education Mode")
        dualoc_title_font = QFont()
        dualoc_title_font.setPointSize(16)
        dualoc_title_font.setBold(True)
        dualoc_title.setFont(dualoc_title_font)
        dualoc_title.setAlignment(Qt.AlignCenter)
        layout_dualoc.addWidget(dualoc_title)

        # Instance selection
        dualoc_instance_layout = QHBoxLayout()

        self.dualoc_own_instance_button = QPushButton("Own Instance")
        self.dualoc_example_instance_button = QPushButton("Example Instance")
        self.dualoc_random_instance_button = QPushButton("Random Instance")

        dualoc_instance_layout.addWidget(self.dualoc_own_instance_button)
        dualoc_instance_layout.addWidget(self.dualoc_example_instance_button)
        dualoc_instance_layout.addWidget(self.dualoc_random_instance_button)

        layout_dualoc.addLayout(dualoc_instance_layout)

        # Info label (e.g. when no dataset is selected)
        self.dualoc_info_text = QLabel()
        self.dualoc_info_text.hide()

        # Remaining layouts dualoc page
        layout_switch_options = QHBoxLayout()
        layout_bottom_buttons = QHBoxLayout()

        # Oberer Eingabebereich
        dualoc_input_frame = QGroupBox("Problem Data")
        dualoc_input_layout = QVBoxLayout()
        dualoc_input_frame.setLayout(dualoc_input_layout)

        # Gemeinsamer Bereich für Matrix oder Lösung
        self.dualoc_display_frame = QGroupBox("Matrix")
        self.dualoc_display_layout = QVBoxLayout()
        self.dualoc_display_frame.setLayout(self.dualoc_display_layout)

        # Algorithm ComboBox
        self.combo_algos_discrete_education = QComboBox()
        self.combo_algos_discrete_education.addItem("Please Select Algorithm...")
        self.combo_algos_discrete_education.addItems(["Dualoc", "Greedy Heuristic", "Interchange Heuristic"])
       
        # Own Instance Widget
        self.dualoc_own_instance_widget = QWidget()
        dualoc_own_instance_layout = QVBoxLayout(
            self.dualoc_own_instance_widget
        )

        # Dimension inputs
        layout_dimension_inputs = QHBoxLayout()

        # Number of customers
        customers_layout = QVBoxLayout()
        customers_layout.addWidget(QLabel("Number of customers:"))

        self.number_clients = QLineEdit()
        self.number_clients.setPlaceholderText("e.g. 6")

        customers_layout.addWidget(self.number_clients)

        # Number of facilities
        facilities_layout = QVBoxLayout()
        facilities_layout.addWidget(QLabel("Number of facilities:"))

        self.number_facilities = QLineEdit()
        self.number_facilities.setPlaceholderText("e.g. 5")

        facilities_layout.addWidget(self.number_facilities)

        layout_dimension_inputs.addLayout(customers_layout)
        layout_dimension_inputs.addLayout(facilities_layout)

        dualoc_own_instance_layout.addLayout(layout_dimension_inputs)

        # Create Matrix
        self.button_create_matrix_dualoc = QPushButton("Create Matrix")
        self.button_create_matrix_dualoc.clicked.connect(
            lambda: self.create_matrix_dualoc_signal.emit()
        )

        dualoc_own_instance_layout.addWidget(
            self.button_create_matrix_dualoc
        )

        # Add Own Instance area
        dualoc_input_layout.addWidget(
            self.dualoc_own_instance_widget
        )

        # Initially hidden
        self.dualoc_own_instance_widget.hide()

        # Example Instance
        self.dualoc_combo_datasets = QComboBox()
        self.dualoc_combo_datasets.addItem("Please Select Example...")
        self.dualoc_combo_datasets.addItems(self.datapoints_model.list_dualoc_problems(education_only=True))

        dualoc_input_layout.addWidget(self.dualoc_combo_datasets)

        # Initially hidden
        self.dualoc_combo_datasets.hide()

        self.dualoc_combo_datasets.currentTextChanged.connect(lambda text: self.dualoc_dataset_changed.emit(text))

        # Random Instance Widget
        self.dualoc_random_instance_widget = QWidget()

        dualoc_random_instance_layout = QHBoxLayout(
            self.dualoc_random_instance_widget
        )

        # Number of customers
        random_customers_layout = QVBoxLayout()

        random_customers_layout.addWidget(
            QLabel("Number of customers:")
        )

        self.dualoc_random_customers_input = QLineEdit()
        self.dualoc_random_customers_input.setPlaceholderText("1-10")

        random_customers_layout.addWidget(
            self.dualoc_random_customers_input
        )

        # Number of facilities
        random_facilities_layout = QVBoxLayout()

        random_facilities_layout.addWidget(
            QLabel("Number of facilities:")
        )

        self.dualoc_random_facilities_input = QLineEdit()
        self.dualoc_random_facilities_input.setPlaceholderText("1-10")

        random_facilities_layout.addWidget(
            self.dualoc_random_facilities_input
        )

        # Generate button
        self.dualoc_generate_random_button = QPushButton("Generate")

        self.dualoc_generate_random_button.clicked.connect(
            lambda: self.dualoc_random_instance_signal.emit()
        )

        # Add everything
        dualoc_random_instance_layout.addLayout(
            random_customers_layout
        )

        dualoc_random_instance_layout.addLayout(
            random_facilities_layout
        )

        dualoc_random_instance_layout.addWidget(
            self.dualoc_generate_random_button,
            alignment=Qt.AlignBottom
        )

        # Add Random area to Problem Data
        dualoc_input_layout.addWidget(
            self.dualoc_random_instance_widget
        )

        # Initially hidden
        self.dualoc_random_instance_widget.hide()

        self.dualoc_own_instance_button.clicked.connect(lambda: self.show_dualoc_own_instance())

        self.dualoc_example_instance_button.clicked.connect(lambda: self.show_dualoc_example_instance())

        self.dualoc_random_instance_button.clicked.connect(lambda: self.show_dualoc_random_instance())

        # Gesamte Matrixansicht als ein Widget
        self.dualoc_matrix_widget = QWidget()
        dualoc_matrix_layout = QVBoxLayout(
            self.dualoc_matrix_widget
        )

        dualoc_matrix_layout.addWidget(
            QLabel(
                "Assignment costs c(i,j), and facility costs f(j)"
            )
        )

        self.table_matrix_dualoc = QTableWidget()
        self.table_matrix_dualoc.setRowCount(0)
        self.table_matrix_dualoc.setColumnCount(0)

        dualoc_matrix_layout.addWidget(
            self.table_matrix_dualoc
        )

        # Matrixansicht in den gemeinsamen Anzeigebereich einsetzen
        self.dualoc_display_layout.addWidget(self.dualoc_matrix_widget)

       # Lösungstabelle im gleichen Anzeigebereich
        self.dualoc_table_widget = QTableWidget()
        self.dualoc_table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.dualoc_table_widget.setRowCount(0)
        self.dualoc_table_widget.setColumnCount(0)
        self.dualoc_display_layout.addWidget(self.dualoc_table_widget)
        # Textuelle Lösung und optionaler Lösungsweg
        self.dualoc_solution_text = QTextEdit()
        self.dualoc_solution_text.setReadOnly(True)
        self.dualoc_display_layout.addWidget(self.dualoc_solution_text)
        

        #Zu Beginn nur Matrix anzeigen
        self.dualoc_matrix_widget.setVisible(True)
        self.dualoc_table_widget.setVisible(False)
        self.dualoc_solution_text.setVisible(False)

        self.discrete_education_show_solution_checkbox = QCheckBox("Show Solution Path")
        self.discrete_education_show_solution_checkbox.setStyleSheet("QCheckBox::indicator { width: 25px; height: 25px; }")

        self.dualoc_matrix_solution_switch = QPushButton("Cost Matrix / Solution Box")
        self.dualoc_matrix_solution_switch.clicked.connect(self.dualoc_switch_matrix_solutionBox)
        layout_switch_options.addWidget(self.discrete_education_show_solution_checkbox,2)
        layout_switch_options.addWidget(self.dualoc_matrix_solution_switch,1)

        #Save Matrix Button
        self.dualoc_save_matrix_button = QPushButton("Save Matrix")
        self.dualoc_save_matrix_button.clicked.connect(
            lambda: self.dualoc_save_matrix_signal.emit()
        )

        # Untere Buttonzeile analog zum Network Mode
        self.dualoc_solve_button = QPushButton("Solve")
        self.dualoc_solve_button.clicked.connect(lambda: self.dualoc_solve_signal.emit("education"))
        self.discrete_education_reset_button = QPushButton("Reset")
        self.discrete_education_reset_button.clicked.connect(lambda: self.discrete_education_reset_signal.emit())
        self.dualoc_back_button = QPushButton("Back")
        self.dualoc_back_button.clicked.connect(lambda: self.dualoc_back_signal.emit())
        self.dualoc_back_button.setStyleSheet("background-color: red; color: white;")
        layout_bottom_buttons.addWidget(self.dualoc_solve_button)
        layout_bottom_buttons.addWidget(self.discrete_education_reset_button)
        layout_bottom_buttons.addWidget(self.dualoc_back_button)

    
        #Layouts hinzufügen
        layout_dualoc.addWidget(dualoc_input_frame)
        layout_dualoc.addWidget(self.dualoc_info_text)
        layout_dualoc.addWidget(self.dualoc_display_frame,1)
        layout_dualoc.addWidget(self.dualoc_save_matrix_button)
        layout_dualoc.addWidget(self.combo_algos_discrete_education)
        layout_dualoc.addLayout(layout_switch_options)
        layout_dualoc.addLayout(layout_bottom_buttons)

        self.setup_districting_education_page()

    def setup_districting_education_page(self):
        """
        The districting page: the basic areas (points with an activity) in a coordinate system on the left; on the
        right their table (x, y, activity w), the number of districts p, the parameters of Recursive Partitioning
        (line directions K, weight beta), the algorithm, the result and Run.
        """
        self.page_districting_education = QWidget()
        layout = QHBoxLayout(self.page_districting_education)
        self.districting_education_plot_canvas = PlotCanvas(self, width=5, height=4)
        self.districting_education_plot_canvas.show_default_axes()
        layout.addWidget(self.districting_education_plot_canvas, 1)

        panel = QVBoxLayout()
        title = QLabel("Districting Problems - Education Mode")
        title.setFont(ui_font(20))
        panel.addWidget(title)

        # Own / example / random instance
        instance_buttons = QHBoxLayout()
        own_button = QPushButton("Own Instance")
        example_button = QPushButton("Example Instance")
        random_button = QPushButton("Random Instance")
        for button in (own_button, example_button, random_button):
            instance_buttons.addWidget(button)
        panel.addLayout(instance_buttons)

        self.districting_education_own_widget = QWidget()
        own_layout = QHBoxLayout(self.districting_education_own_widget)
        own_layout.addWidget(QLabel("Number of basic areas:"))
        self.districting_education_own_areas_input = QLineEdit()
        self.districting_education_own_areas_input.setPlaceholderText("1-30")
        own_layout.addWidget(self.districting_education_own_areas_input)
        create_button = QPushButton("Create Table")
        create_button.clicked.connect(lambda: self.districting_education_create_table_signal.emit())
        own_layout.addWidget(create_button)
        self.districting_education_own_widget.hide()
        panel.addWidget(self.districting_education_own_widget)

        self.districting_education_combo_datasets = QComboBox()
        self.districting_education_combo_datasets.addItem("Please Select Example...")
        self.districting_education_combo_datasets.addItems(
            self.datapoints_model.list_districting_problems(education_only=True))
        self.districting_education_combo_datasets.currentTextChanged.connect(
            lambda text: self.districting_education_dataset_changed.emit(text))
        self.districting_education_combo_datasets.hide()
        panel.addWidget(self.districting_education_combo_datasets)

        self.districting_education_random_widget = QWidget()
        random_layout = QHBoxLayout(self.districting_education_random_widget)
        random_layout.addWidget(QLabel("Number of basic areas:"))
        self.districting_education_random_areas_input = QLineEdit()
        self.districting_education_random_areas_input.setPlaceholderText("1-30")
        random_layout.addWidget(self.districting_education_random_areas_input)
        generate_button = QPushButton("Generate")
        generate_button.clicked.connect(lambda: self.districting_education_random_instance_signal.emit())
        random_layout.addWidget(generate_button)
        self.districting_education_random_widget.hide()
        panel.addWidget(self.districting_education_random_widget)

        own_button.clicked.connect(lambda: self.show_districting_education_instance("own"))
        example_button.clicked.connect(lambda: self.show_districting_education_instance("example"))
        random_button.clicked.connect(lambda: self.show_districting_education_instance("random"))

        # The basic areas
        panel.addWidget(QLabel("Basic areas (x, y, activity w):"))
        self.districting_education_table = QTableWidget(0, 3)
        self.districting_education_table.setHorizontalHeaderLabels(["x", "y", "Activity w"])
        self.districting_education_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.districting_education_table.itemChanged.connect(
            lambda item: self.districting_education_table_changed_signal.emit())
        panel.addWidget(self.districting_education_table, 1)

        # The number of districts and the parameters of Recursive Partitioning
        parameters = QHBoxLayout()
        self.districting_education_p = QSpinBox()
        self.districting_education_p.setRange(1, 8)       # Education Mode: at most 8 districts
        self.districting_education_p.setValue(4)
        self.districting_education_K = QSpinBox()
        self.districting_education_K.setRange(1, 4)       # Education Mode: at most 4 line directions
        self.districting_education_K.setValue(2)
        self.districting_education_beta = QDoubleSpinBox()
        self.districting_education_beta.setRange(0.0, 1.0)
        self.districting_education_beta.setSingleStep(0.1)
        self.districting_education_beta.setDecimals(2)
        self.districting_education_beta.setValue(0.5)
        for label, field, tip in (
                ("Districts p:", self.districting_education_p, "The number of districts (1 to 8)"),
                ("Line directions K:", self.districting_education_K,
                 "The number of line directions (1 to 4): K = 2 horizontal and vertical lines, K = 4 also diagonal ones"),
                ("β:", self.districting_education_beta,
                 "The weight of the balance against the compactness in the rank of a line partition (0 to 1)")):
            label_widget = QLabel(label)
            label_widget.setToolTip(tip)
            field.setToolTip(tip)
            parameters.addWidget(label_widget)
            parameters.addWidget(field)
        panel.addLayout(parameters)

        self.districting_education_combo_algos = QComboBox()
        self.districting_education_combo_algos.addItem("Please Select Algorithm...")
        self.districting_education_combo_algos.addItem("Recursive Partitioning")
        panel.addWidget(self.districting_education_combo_algos)

        # The result
        self.districting_education_result_text = QTextEdit()
        self.districting_education_result_text.setReadOnly(True)
        panel.addWidget(self.districting_education_result_text, 1)

        self.districting_education_show_solution_checkbox = QCheckBox("Show Solution Path")
        self.districting_education_show_solution_checkbox.setStyleSheet(
            "QCheckBox::indicator { width: 25px; height: 25px; }")
        panel.addWidget(self.districting_education_show_solution_checkbox)

        self.districting_education_run_algo_button = QPushButton("Run Algorithm")
        self.districting_education_run_algo_button.clicked.connect(
            lambda: self.districting_education_run_algo_signal.emit())
        panel.addWidget(self.districting_education_run_algo_button)

        bottom = QHBoxLayout()
        self.districting_education_reset_button = QPushButton("Remove All Areas")
        self.districting_education_reset_button.clicked.connect(lambda: self.districting_education_reset_signal.emit())
        back_button = QPushButton("Back")
        back_button.setStyleSheet("background-color: red; color: white;")
        back_button.clicked.connect(self.show_education_options)
        back_button.clicked.connect(lambda: self.districting_education_reset_signal.emit())
        bottom.addWidget(self.districting_education_reset_button)
        bottom.addWidget(back_button)
        panel.addLayout(bottom)

        layout.addLayout(panel, 1)
        self.stackedLayout.addWidget(self.page_districting_education)

    def show_education_options(self):
        self.update_breadcrumb(["Start", "Mode Selection", "Education Mode"])
        self.stackedLayout.setCurrentWidget(self.page_education)

    def show_planar_education_page(self):
        self.update_breadcrumb(["Start", "Mode Selection", "Education Mode", "Planar Problems"])
        self.stackedLayout.setCurrentWidget(self.page_planar_education)

    def show_network_education_page(self):
        self.update_breadcrumb(["Start", "Mode Selection", "Education Mode", "Network Problems", self.network_type_name])
        self.update_network_education_graph_view()
        self.stackedLayout.setCurrentWidget(self.page_network_education)

    def show_districting_education_page(self):
        self.update_breadcrumb(["Start", "Mode Selection", "Education Mode", "Districting Problems"])
        self.stackedLayout.setCurrentWidget(self.page_districting_education)

    def show_districting_education_instance(self, kind):
        """Shows the input of an own ("own"), an example ("example") or a random instance ("random")."""
        self.districting_education_own_widget.setVisible(kind == "own")
        self.districting_education_random_widget.setVisible(kind == "random")
        if kind == "example":
            self.districting_education_combo_datasets.setCurrentIndex(0)
        self.districting_education_combo_datasets.setVisible(kind == "example")

    def fill_districting_education_table(self, areas):
        """Writes the basic areas [(x, y, w), ...] into the table (one row each; None: an empty cell)."""
        table = self.districting_education_table
        table.blockSignals(True)
        table.setRowCount(len(areas))
        for row, area in enumerate(areas):
            for column, value in enumerate(area):
                table.setItem(row, column, QTableWidgetItem("" if value is None else f"{value:g}"))
        table.blockSignals(False)

    def districting_education_areas(self):
        """
        The basic areas of the table.

        :return: ([(x, y, w), ...] of the rows filled correctly, [numbers of the rows with an empty or invalid cell]);
                 a decimal comma is accepted
        """
        table, areas, invalid = self.districting_education_table, [], []
        for row in range(table.rowCount()):
            try:
                values = [float(table.item(row, column).text().strip().replace(",", ".")) for column in range(3)]
                if not all(math.isfinite(value) for value in values):
                    raise ValueError
                areas.append(tuple(values))
            except (AttributeError, ValueError):
                invalid.append(row + 1)
        return areas, invalid

    def show_discrete_education_options(self):
        self.update_breadcrumb(["Start", "Mode Selection", "Education Mode", "Discrete Problems"])
        self.stackedLayout.setCurrentWidget(self.page_dualoc_education)

    def update_coordinate_display_points_education(self):
        # Shows the data points of the model with 2 decimal places on the Education planar page
        points = self.datapoints_model.get_points()
        coords_text = "\n".join([f"{lat:.2f}, {lng:.2f}, {weight:.2f}" for lat, lng, weight, _ in points])
        self.planar_education_text_coords.setText(coords_text)

    def dualoc_switch_matrix_solutionBox(self):
        """
        Wechselt nach dem Solve zwischen
        textueller Lösung und markierter Lösungsmatrix.
        """

        # Vor Solve gibt es noch keine Lösung zum Umschalten
        if self.dualoc_matrix_widget.isVisible():
            return

        solution_is_visible = self.dualoc_solution_text.isVisible()

        if solution_is_visible:
            # Gelb markierte Matrix anzeigen
            self.dualoc_solution_text.setVisible(False)
            self.dualoc_table_widget.setVisible(True)
            self.dualoc_display_frame.setTitle("Solution Matrix")
        else:
            # Textuelle Lösung anzeigen
            self.dualoc_table_widget.setVisible(False)
            self.dualoc_solution_text.setVisible(True)
            self.dualoc_display_frame.setTitle("Solution")

    def dualoc_show_matrix_widget(self):
        """
        Zeigt die Eingabematrix vor dem Solve.
        """
        self.dualoc_matrix_widget.setVisible(True)
        self.dualoc_table_widget.setVisible(False)
        self.dualoc_solution_text.setVisible(False)
        self.dualoc_display_frame.setTitle("Matrix")

    def dualoc_show_solution_widget(self):
        """
        Zeigt nach Solve zunächst die textuelle Lösung.
        """
        self.dualoc_matrix_widget.setVisible(False)
        self.dualoc_table_widget.setVisible(False)
        self.dualoc_solution_text.setVisible(True)
        self.dualoc_display_frame.setTitle("Solution")

    def highlight_discrete_solution(self, solution, mode):
        """
        Highlights the solution of a discrete facility location problem.

        solution[0]:
            List of opened facilities, e.g. [2, 4]

        solution[1]:
            Facility assignment for each client, e.g. [2, 2, 4, 2, 4]

        Facility numbers are assumed to start at 1.
        """

        if not solution or len(solution) < 2:
            return

        opened_facilities = solution[0]
        assignments = solution[1]

        # Education result table
        table = self.dualoc_table_widget

        # Highlight style
        highlight_color = QColor("#FFD54F")  
        text_color = QBrush(QColor("#000000"))

        bold_font = QFont()
        bold_font.setBold(True)

        # --------------------------------------------------
        # 1. Highlight headers of opened facilities
        # --------------------------------------------------
        for facility in opened_facilities:

            # Facilities are numbered from 1,
            # QTableWidget columns start at 0.
            column = int(facility) - 1

            if 0 <= column < table.columnCount():

                header_item = table.horizontalHeaderItem(column)

                if header_item is not None:
                    header_item.setBackground(highlight_color)
                    header_item.setForeground(text_color)
                    header_item.setFont(bold_font)

        # --------------------------------------------------
        # 2. Highlight client -> facility assignments
        # --------------------------------------------------
        for client_index, facility in enumerate(assignments):

            column = int(facility) - 1
            row = client_index

            if (
                0 <= row < table.rowCount()
                and 0 <= column < table.columnCount()
            ):

                item = table.item(row, column)

                if item is not None:
                    item.setBackground(highlight_color)
                    item.setForeground(text_color)
                    item.setFont(bold_font)

    def toggle_dualoc_example_combo(self):
        is_visible = self.dualoc_combo_datasets.isVisible()
        self.dualoc_combo_datasets.setVisible(not is_visible)

    def update_network_education_graph_view(self):
        if self.network_education_graph_checkbox.isChecked():
            self.help_label_1.setVisible(False)
            self.help_label_2.setVisible(False)
            self.network_education_plot_canvas.setVisible(True)
        else:
            self.help_label_1.setVisible(True)
            self.help_label_2.setVisible(True)
            self.network_education_plot_canvas.setVisible(False)

    def network_education_show_default_view(self):
        self.network_education_hide_pareto_front()
        self.network_education_solution_label.setVisible(False)
        self.network_education_matrix_table.setVisible(True)

    def network_education_show_solution_Widget(self):
        self.network_education_front_view.setVisible(False)
        self.network_education_solution_label.setVisible(True)
        self.network_education_matrix_table.setVisible(False)

    def network_education_switch_matrix_solutionBox(self):
        self.network_education_front_view.setVisible(False)      # from the Pareto front back to the solution box
        if self.network_education_solution_label.isVisible():
            self.network_education_solution_label.setVisible(False)
            self.network_education_matrix_table.setVisible(True)
        else:
            self.network_education_solution_label.setVisible(True)
            self.network_education_matrix_table.setVisible(False)

    def network_education_show_input_Widget(self):
        self.network_education_hide_pareto_front()
        self.network_education_solution_label.setVisible(False)
        self.network_education_matrix_table.setVisible(True)

    def network_education_set_pareto_front(self, front):
        """After a Pareto median with two weight vectors: draws its front (AdditionalMethods.pareto_front) and offers
        the button "Pareto Front", which shows it instead of the matrix or the solution box."""
        self.network_education_front_view.plot(front)
        self.network_education_front_button.setVisible(True)

    def network_education_show_front(self):
        self.network_education_solution_label.setVisible(False)
        self.network_education_matrix_table.setVisible(False)
        self.network_education_front_view.setVisible(True)

    def network_education_hide_pareto_front(self):
        """Another run, another algorithm, a new network or Reset: the front of the last run is gone (if it was shown,
        the matrix is shown instead)."""
        self.network_education_front_button.setVisible(False)
        if self.network_education_front_view.isVisible():
            self.network_education_front_view.setVisible(False)
            self.network_education_matrix_table.setVisible(True)

    def network_type_selected_education(self, directed):
        # The input for several weight vectors (Pareto median) is shown for both network types
        self.network_education_weights_label.setVisible(True)
        self.network_education_weights_input.setVisible(True)

        self.update_network_education_algorithms()
        self.update_network_education_example_combo()
        self.show_network_education_page()

    def update_network_education_algorithms(self):
        self.network_education_combo_algos.clear()
        self.network_education_combo_algos.addItem("Please Select Algorithm...")
        

        try:
            number_of_weights = int(
                self.network_education_weights_input.text()
            )
        except ValueError:
            number_of_weights = 1

        if self.modelmatrix.directed:
            # Bei mindestens zwei Gewichten ausschließlich Pareto
            if number_of_weights >= 2:
                self.network_education_combo_algos.addItem("Pareto Median Directed Network")
                self.network_education_combo_algos.addItem("Pareto In Median Directed Network")
                self.network_education_combo_algos.addItem("Pareto Out Median Directed Network")
                return
            self.network_education_combo_algos.addItem("Median Directed Network")
            self.network_education_combo_algos.addItem("In Median Directed Network")
            self.network_education_combo_algos.addItem("Out Median Directed Network")
            self.network_education_combo_algos.addItem("Center Directed Network")
            self.network_education_combo_algos.addItem("Out Center Directed Network")
            self.network_education_combo_algos.addItem("In Center Directed Network")
            return 

        # Bei mindestens zwei Gewichten ausschließlich Pareto
        if number_of_weights >= 2:
            self.network_education_combo_algos.addItem(
                "Pareto Median Undirected Network"
            )
            self.network_education_combo_algos.addItem(
                "Pareto Median Undirected Network Vertex-Restricted"
            )
            return

        self.network_education_combo_algos.addItem("Median Undirected Network")
        self.network_education_combo_algos.addItem("Center Undirected Network Vertex-Restricted")
        self.network_education_combo_algos.addItem("Center Undirected Network Absolute")
        self.network_education_combo_algos.addItem("Center Undirected Tree Absolute Unweighted")
        self.network_education_combo_algos.addItem("Center Undirected Tree Vertex-Restricted Unweighted")
        self.network_education_combo_algos.addItem("Median Undirected Tree")

    def update_network_education_example_combo(self):
        self.network_education_example_combo.blockSignals(True)
        self.network_education_example_combo.clear()
        self.network_education_example_combo.addItem("Please Select Example...")

        directed = self.modelmatrix.directed

        self.network_education_example_combo.addItems(
            self.datapoints_model.list_network_problems(directed=directed, max_nodes=10, education_only=True)
        )

        self.network_education_example_combo.blockSignals(False)

    def show_network_education_own_instance(self):
         
        self.network_education_own_instance_widget.show()
        self.network_education_example_combo.hide()
        self.network_education_random_widget.hide()

    def show_network_education_example_instance(self):
        self.network_education_own_instance_widget.hide()
        self.network_education_example_combo.show()
        self.network_education_random_widget.hide()

    def show_network_education_random_instance(self):
        self.network_education_own_instance_widget.hide()
        self.network_education_example_combo.hide()
        self.network_education_random_widget.show()

    def toggle_network_education_example_combo(self):
        if not self.network_education_example_combo.isVisible():
            self.update_network_education_example_combo()

        self.network_education_example_combo.setVisible(
            not self.network_education_example_combo.isVisible()
        )

    def show_dualoc_own_instance(self):
        self.dualoc_own_instance_widget.show()
        self.dualoc_combo_datasets.hide()
        self.dualoc_random_instance_widget.hide()

    def show_dualoc_example_instance(self):
        self.dualoc_own_instance_widget.hide()
        self.dualoc_combo_datasets.show()
        self.dualoc_random_instance_widget.hide()

    def show_dualoc_random_instance(self):
        self.dualoc_own_instance_widget.hide()
        self.dualoc_combo_datasets.hide()
        self.dualoc_random_instance_widget.show()

    def show_planar_education_own_instance(self):
        self.planar_education_combo_datasets.hide()
        self.planar_education_random_widget.hide()
        self.planar_education_manual_input_signal.emit()

    def show_planar_education_example_instance(self):
        self.planar_education_random_widget.hide()
        self.planar_education_combo_datasets.setCurrentIndex(0)
        self.planar_education_combo_datasets.show()

    def show_planar_education_random_instance(self):
        self.planar_education_combo_datasets.hide()
        self.planar_education_random_widget.show()
