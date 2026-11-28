"""Education Mode: the controller methods (signal handlers) of this mode."""
import math
import random
import re

import networkx as nx
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QHeaderView, QMessageBox, QTableWidget, QTableWidgetItem

from common.additional_methods import AdditionalMethods
from education.dialogs_discrete import InterchangeStartSolutionDialog
from education.dialogs_network import InvalidNodeInputDialogEducation, InvalidTreeInputDialogEducation
from education.dialogs_planar import AddCoordsManualEducation

# numpy shows numbers inside lists as e.g. "np.float64(9.0)"; the solution text shows them as "9.0"
NUMPY_NUMBER = re.compile(r"np\.(?:float|int|uint)\d*\(([^()]*)\)")


def without_numpy_wrappers(text):
    """Return the text with numpy numbers like 'np.float64(9.0)' or 'np.int64(3)' written as '9.0' / '3'."""
    return NUMPY_NUMBER.sub(r"\1", text)


class EducationController:
    """Building block of the controller (MainController) for the Education Mode.

    Uses from the controller: view, model, modelmatrix, dualocObject and _get_delta_from_user.
    """

    def connect_education_signals(self):
        self.view.planar_education_run_algo_signal.connect(self.handle_planar_education_run_algorithm)
        self.view.planar_education_dataset_changed.connect(self.handle_planar_education_dataset_changed)
        self.view.planar_education_manual_input_signal.connect(self.handle_planar_education_manual_input)
        self.view.planar_education_remove_marker_signal.connect(self.handle_planar_education_remove_markers)
        self.view.planar_education_back_signal.connect(self.handle_planar_education_remove_markers)
        self.view.planar_education_random_instance_signal.connect(self.handle_planar_education_random_instance)

        self.view.network_education_matrix_signal.connect(self.handle_network_education_matrix)
        self.view.network_education_graph_signal.connect(self.handle_network_education_graph)
        self.view.network_education_reset_signal.connect(self.handle_network_education_reset)
        self.view.network_education_run_algo_signal.connect(self.handle_network_education_run_algorithm)
        self.view.network_education_back_signal.connect(self.handle_network_education_reset)
        self.view.network_education_algo_changed_signal.connect(self.handle_network_education_algo_changed)
        self.view.network_education_example_changed_signal.connect(self.handle_network_education_example_changed)
        self.view.network_education_random_instance_signal.connect(self.handle_network_education_random_instance)

        self.view.dualoc_dataset_changed.connect(self.handle_dualoc_dataset_changed)
        self.view.dualoc_back_signal.connect(self.handle_dualocEducation_back)
        self.view.create_matrix_dualoc_signal.connect(self.handle_dualocEducation_create_matrix)
        self.view.dualoc_save_matrix_signal.connect(self.handle_dualocEducation_save_matrix)
        self.view.dualoc_solve_signal.connect(self.handle_dualoc_solve)
        self.view.dualoc_random_instance_signal.connect(self.handle_dualocEducation_random_instance)

        self.view.discrete_education_reset_signal.connect(self.handle_discrete_education_reset)

        self.view.districting_education_dataset_changed.connect(self.handle_districting_education_dataset_changed)
        self.view.districting_education_create_table_signal.connect(self.handle_districting_education_create_table)
        self.view.districting_education_random_instance_signal.connect(self.handle_districting_education_random_instance)
        self.view.districting_education_table_changed_signal.connect(self.handle_districting_education_table_changed)
        self.view.districting_education_run_algo_signal.connect(self.handle_districting_education_run_algorithm)
        self.view.districting_education_reset_signal.connect(self.handle_districting_education_reset)

    "__________________________________________________________________________________________________________________"
    "Controller methods for Planar Education Mode signals"

    def handle_planar_education_dataset_changed(self, dataset_name):
        """
        Handler for when the dataset selection changes in the Education Mode page.
        It retrieves the dataset from the model, updates the text display with the dataset,
        and plots the points on the PlotCanvas.
        """
        self.model.remove_all_points()

        dataset = self.model.get_dataset(dataset_name)
        if dataset is None:
            self.view.planar_education_text_coords.setText(f"please select dataset/algorithm...")
            self.view.planar_education_plot_canvas.show_default_axes()
            return

        for i in range(len(dataset)):
            self.model.add_point(dataset[i])

        coords_text = "\n".join([f"{x:.2f}, {y: 2f}, {w:.2f}, {name}" for x, y, w, name in dataset])
        self.view.planar_education_text_coords.setText(coords_text)

        data_points = [(x, y) for x, y, _, _ in dataset]
        self.view.planar_education_plot_canvas.plot_data(data_points)

    def handle_planar_education_run_algorithm(self):
        """
        Handles the Run Algorithm button on the Planar Education page.
        It retrieves the current data points from the model, instantiates the selected
        algorithm class based on the combo box selection, runs the algorithm, and then
        updates the view accordingly.
        """

        # Retrieve the currently current dataset from the model
        points_string = self.model.points_toString()
        points = self.model.get_points()

        if not points:
            self.view.planar_education_text_coords.setText("No data points available.")
            return

        # Get the selected algorithm from the combo box
        algo_name = self.view.planar_education_combo_algos.currentText()

        # Instantiate the corresponding algorithm class based on the selection
        if algo_name == "Median l1 Metric Unweighted":
            from education.algorithms.median_l1_metric_unweighted import median_l1_metric_unweighted

            algo = median_l1_metric_unweighted(points)
        elif algo_name == "Median l1 Metric Weighted":
            from education.algorithms.median_l1_metric_weighted import median_l1_metric_weighted

            algo = median_l1_metric_weighted(points)
        elif algo_name == "Median l2 Metric Weighted":
            from education.algorithms.median_l2_metric_weighted import median_l2_metric_weighted
            delta = self._get_delta_from_user(self.view)
            if delta is None:   # the user cancelled the dialog
                return
            algo = median_l2_metric_weighted(points, delta)

        elif algo_name == "Median l2 Squared Weighted":
            from education.algorithms.median_l2_squared_weighted import median_l2_squared_weighted

            algo = median_l2_squared_weighted(points)
        elif algo_name == "Center l1 Metric Unweighted":
            from education.algorithms.center_l1_metric_unweighted import center_l1_metric_unweighted

            algo = center_l1_metric_unweighted(points)
        elif algo_name == "Center l1 Metric Weighted":
            from education.algorithms.center_l1_metric_weighted import center_l1_metric_weighted

            algo = center_l1_metric_weighted(points)
        elif algo_name == "Center l2 Metric Unweighted":
            from education.algorithms.center_l2_metric_unweighted import center_l2_metric_unweighted

            algo = center_l2_metric_unweighted(points)
        elif (algo_name== "Center l∞ Metric Unweighted"):
            from education.algorithms.center_linf_metric_unweighted import center_linf_metric_unweighted

            algo = center_linf_metric_unweighted(points)
        elif algo_name == "Center l∞ Metric Weighted":
            from education.algorithms.center_linf_metric_weighted import center_linf_metric_weighted
            
            algo = center_linf_metric_weighted(points)
        else:
            current_text = self.view.planar_education_text_coords.toPlainText()
            self.view.planar_education_text_coords.setText(current_text + "\n" + "\nNo valid algorithm selected." )
            return

        optimal_points, result_str, solution_path, _ = algo.run()   # no CSV output in the Education Mode
       
        # Plot the optimal points in the coordinate system (PlotCanvas): every problem in its own colour, with its short
        # name in the legend ("Median l1 Unweighted" for "Median l1 Metric Unweighted")
        self.view.planar_education_plot_canvas.plot_solution(optimal_points, algo_name.replace(" Metric", ""))

        # Check if the solution path checkbox is selected and update the text field
        if self.view.planar_education_show_solution_checkbox.isChecked():
            # Zeige Ergebnis und Lösungspfad
            self.view.planar_education_text_coords.setText(
                points_string
                + "\n\n"
                + "____________________________________________________________________________________"
                + "\n\n"
                + solution_path
                + "\n\n"
                + result_str
            )
        else:
            self.view.planar_education_text_coords.setText(
                points_string + "\n\n" + result_str
            )

    def handle_planar_education_remove_markers(self):
        self.model.remove_all_points()
        self.view.update_coordinate_display_points_education()
        self.view.planar_education_plot_canvas.show_default_axes()
        self.view.planar_education_combo_algos.setCurrentIndex(0)
        self.view.planar_education_combo_datasets.setCurrentIndex(0)

    def handle_planar_education_manual_input(self):
        # alles updaten, btn deaktiviern, punkte entfernen
        self.model.remove_all_points()
        self.view.update_coordinate_display_points_education()
        self.view.planar_education_combo_datasets.setCurrentIndex(0)

        dialog = AddCoordsManualEducation(self.view)
        if dialog.exec_() == dialog.Accepted:

            self.view.update_coordinate_display_points_education()
        return  

    def handle_planar_education_random_instance(self):
        try:
            number_points = int(
                self.view.planar_education_random_points_input.text()
            )
        except ValueError:
            self.view.planar_education_text_coords.setText(
                "Please enter a number between 1 and 10."
            )
            return

        if number_points < 1 or number_points > 10:
            self.view.planar_education_text_coords.setText(
                "Please enter a number between 1 and 10."
            )
            return

        # Remove previous points
        self.model.remove_all_points()

        # Reset example selection
        self.view.planar_education_combo_datasets.setCurrentIndex(0)

        # Generate unique coordinates
        generated_coordinates = set()

        while len(generated_coordinates) < number_points:
            x = random.randint(0, 10)
            y = random.randint(0, 10)

            generated_coordinates.add((x, y))

        # Add generated points to model, each with a random weight from 1 to 10 (weighted and unweighted problems differ)
        for x, y in generated_coordinates:
            self.model.add_point((x, y, float(random.randint(1, 10))))

        # Update text display
        self.view.update_coordinate_display_points_education()

        # Plot generated points
        self.view.planar_education_plot_canvas.plot_data(
            self.model.get_points()
        )
    '__________________________________________________________________________________________________________________'
    'Controller methods for Network Education Mode signals'

    def handle_network_education_matrix(self):
        """
        Reads the number of nodes from the input field, creates the matrix in the modelmatrix,
        and updates the matrix table in the view.
        """

        self.view.network_education_plot_canvas.show_network_default_axes()
        self.view.network_education_show_input_Widget()

        try:
            nodes = int(self.view.network_education_nodes_input.text())
            number_of_weights = int(self.view.network_education_weights_input.text())
        except ValueError:
            dialog = InvalidNodeInputDialogEducation(self.view)
            dialog.exec_()
            return

        if nodes < 2 or nodes > 10 or number_of_weights < 1:
            dialog = InvalidNodeInputDialogEducation(self.view)
            dialog.exec_()
            return

        # Algorithmusliste passend zur Anzahl der Gewichte aktualisieren
        self.view.update_network_education_algorithms()

        # Erzeuge die Matrix im ModelMatrix-Objekt
        self.modelmatrix.create_matrix(nodes)
        # Hole Matrix und Anzahl der Knoten
        matrix, count = self.modelmatrix.get_matrix()

        # Aktualisiere die Matrix-Tabelle in der View:
        self.view.network_education_matrix_table.setRowCount(count)
        self.view.network_education_matrix_table.setColumnCount(count + number_of_weights)

        # Überschriften der Gewichtsspalten
        for weight_index in range(number_of_weights):
            column = count + weight_index

            if number_of_weights == 1:
                header = "weights"
            else:
                header = f"weights {weight_index + 1}"

            self.view.network_education_matrix_table.setHorizontalHeaderItem(
                column,
                QTableWidgetItem(header)
            )
        
        for row in range(count):
            for col in range(count):
                value = matrix[row][col]
                if value == None:
                    value = ""

                item = QTableWidgetItem(str(value))

                if self.modelmatrix.is_directed():
                    # Directed: nur Diagonale blockieren
                    if row == col:
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                else:
                    # Undirected: Diagonale + alles unterhalb der Diagonale blockieren
                    if row >= col:
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                self.view.network_education_matrix_table.setItem(row, col, item)
        # Gewichtsspalte initial leer setzen
        for row in range(count):
            for weight_index in range(number_of_weights):
                column = count + weight_index
                self.view.network_education_matrix_table.setItem(
                    row,
                    column,
                    QTableWidgetItem("")
                )
        # Eingabefelder nach erfolgreicher Erstellung leeren

        # Nodes und Weights Input-Felder leeren
        self.view.network_education_nodes_input.clear()
        self.view.network_education_weights_input.blockSignals(True)
        self.view.network_education_weights_input.clear()
        self.view.network_education_weights_input.blockSignals(False)
               
    def handle_network_education_graph(self):
        self.view.network_education_hide_pareto_front()     # a new network: the front of the last run is gone
        # Read the updated matrix from the view’s table.
        table = self.view.network_education_matrix_table
        row_count = table.rowCount()
        updated_matrix = []
        for i in range(row_count):
            row = []
            for j in range(row_count):
                item = table.item(i, j)
                if item is not None:
                    text = item.text().strip()
                    if text == "" or text.lower() == "n":
                        row.append(None)
                    else:
                        try:   # a decimal comma is accepted as well
                            value = float(text.replace(",", "."))
                            if not math.isfinite(value):   # float() also accepts "nan" and "inf"
                                raise ValueError
                            row.append(value)
                        except ValueError:
                            QMessageBox.warning(self.view, "Invalid Input",
                                                f"Please enter a number for the edge from {i + 1} to {j + 1} or leave the cell empty.")
                            return
                else:
                    row.append(None)
            updated_matrix.append(row)

        # Every edge needs a positive length
        if any(updated_matrix[i][j] is not None and updated_matrix[i][j] <= 0
               for i in range(row_count) for j in range(row_count) if i != j):
            QMessageBox.warning(self.view, "Invalid Input", "An edge must have a length greater than 0.")
            return

        #Matrix symmetrisch machen, falls es ein ungerichtetes Netzwerk ist
        if not self.modelmatrix.is_directed():
            for i in range(row_count):
                for j in range(i + 1, row_count):
                    updated_matrix[j][i] = updated_matrix[i][j]

        # Matrix in der Tabelle anzeigen, damit die vervollständigte undirected Matrix sichtbar wird
        for i in range(row_count):
            for j in range(row_count):
                value = updated_matrix[i][j]

                if i == j:
                    display_value = "n"
                elif value is None:
                    display_value = ""
                else:
                    display_value = str(value)

                item = QTableWidgetItem(display_value)

                if self.modelmatrix.is_directed():
                    if i == j:
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                else:
                    if i >= j:
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                table.setItem(i, j, item)


        # Anzahl der Gewichtsspalten aus der Tabelle bestimmen
        number_of_weights = table.columnCount() - row_count

        all_weights = []

        # Gewichtsspalten nacheinander einlesen
        for weight_index in range(number_of_weights):
            column = row_count + weight_index
            raw_weights = []

            for row in range(row_count):
                item = table.item(row, column)
                text = item.text().strip().replace(",", ".") if item is not None else ""

                if text:
                    try:
                        weight = float(text)
                        if not math.isfinite(weight):   # float() also accepts "nan" and "inf"
                            raise ValueError
                    except ValueError:
                        QMessageBox.warning(self.view, "Invalid Input",
                                            f"Please enter a number as weight of vertex {row + 1} or leave the cell empty.")
                        return
                    if weight < 0:   # 0 is allowed: the vertex need not be reached
                        QMessageBox.warning(self.view, "Invalid Input", f"The weight of vertex {row + 1} must be 0 or greater.")
                        return
                    raw_weights.append(text)
                else:
                    raw_weights.append(None)

            # Leere Werte dieser Gewichtsspalte vervollständigen
            completed_weights = self.modelmatrix.complete_weights(
                raw_weights
            )

            all_weights.append(completed_weights)

            # Vervollständigte Werte wieder anzeigen
            for row in range(row_count):
                table.setItem(
                    row,
                    column,
                    QTableWidgetItem(
                        str(completed_weights[row])
                    )
                )

        # Speicherformat abhängig von der Anzahl der Gewichtsspalten
        if number_of_weights == 1:
            self.modelmatrix.set_weights(all_weights[0])
        else:
            self.modelmatrix.set_weights(all_weights)

        self.modelmatrix.set_matrix(updated_matrix, row_count)

        # Retrieve the updated matrix and convert it to a graph.
        graph = self.modelmatrix.matrix_in_graph()
        # Display the graph on the PlotCanvas.
        self.view.network_education_plot_canvas.plot_graph(graph, self.modelmatrix.get_pos())

      
        self.view.network_education_graph_button.setEnabled(False)
        self.view.network_education_matrix_button.setEnabled(False)
        self.view.network_education_matrix_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
    def handle_network_education_reset(self):
        """
        Resets the stored matrix in the modelmatrix and clears the corresponding view components.
        """
        self.modelmatrix.clear_matrix()
        self.view.network_education_matrix_table.clear()
        self.view.network_education_solution_label.clear()
        self.view.network_education_matrix_table.setRowCount(0)
        self.view.network_education_matrix_table.setColumnCount(0)
        self.view.network_education_combo_algos.setCurrentIndex(0)
        self.view.network_education_nodes_input.clear()
        self.view.network_education_plot_canvas.show_network_default_axes()
        self.view.network_education_show_input_Widget()
        self.view.network_education_matrix_table.setEditTriggers(QTableWidget.AllEditTriggers)
        self.view.network_education_graph_button.setEnabled(True)
        self.view.network_education_matrix_button.setEnabled(True)
        self.view.network_education_example_combo.setCurrentIndex(0)
        self.view.network_education_example_combo.setVisible(False)

    def handle_network_education_run_algorithm(self):
        """
        Handles the Run Algorithm button on the Network Education page.
        It retrieves the current network from the model, instantiates the selected
        algorithm class based on the combo box selection, runs the algorithm, and then
        updates the view accordingly.
        """
        self.view.network_education_hide_pareto_front()
        network_graph = self.modelmatrix.get_graph()
        network_matrix, row_count = self.modelmatrix.get_matrix()
        self.view.network_education_show_solution_Widget()

        if not network_graph:
            self.view.network_education_solution_label.setText("No matrix saved!")
            self.view.network_education_solution_label.setVisible(True)
            return

        algo_name = self.view.network_education_combo_algos.currentText()

        

        if algo_name == "Median Directed Network":
            from education.algorithms.median_directed_network import median_directed_network
            matrix, nodes = self.modelmatrix.get_matrix()
            algo = median_directed_network(self.modelmatrix.get_weights(), matrix)

        elif algo_name == "Median Undirected Network":
            from education.algorithms.median_undirected_network import median_undirected_network
            matrix, nodes = self.modelmatrix.get_matrix()
            algo = median_undirected_network(self.modelmatrix.get_weights(), matrix)

        elif algo_name == "In Median Directed Network":
            from education.algorithms.in_median_directed_network import in_median_directed_network
            matrix, nodes = self.modelmatrix.get_matrix()
            algo = in_median_directed_network(self.modelmatrix.get_weights(), matrix)

        elif algo_name == "Out Median Directed Network":
            from education.algorithms.out_median_directed_network import out_median_directed_network
            matrix, nodes = self.modelmatrix.get_matrix()
            algo = out_median_directed_network(self.modelmatrix.get_weights(), matrix)

        elif algo_name == "Center Undirected Network Vertex-Restricted":
            from education.algorithms.center_undirected_network_vertex_restricted import center_undirected_network_vertex_restricted
            matrix, nodes = self.modelmatrix.get_matrix()
            algo = center_undirected_network_vertex_restricted(self.modelmatrix.get_weights(), matrix)
        elif algo_name == "Center Undirected Tree Absolute Unweighted":
            from education.algorithms.center_undirected_tree_absolute_unweighted import center_undirected_tree_absolute_unweighted
            matrix, nodes = self.modelmatrix.get_matrix()
            algo = center_undirected_tree_absolute_unweighted(self.modelmatrix.get_weights(), matrix)
        elif algo_name == "Median Undirected Tree":
            from education.algorithms.median_undirected_tree import median_undirected_tree
            matrix, nodes = self.modelmatrix.get_matrix()
            algo = median_undirected_tree(self.modelmatrix.get_weights(), matrix)
        elif algo_name == "Center Undirected Tree Vertex-Restricted Unweighted":
            from education.algorithms.center_undirected_tree_vertex_restricted_unweighted import center_undirected_tree_vertex_restricted_unweighted
            matrix, nodes = self.modelmatrix.get_matrix()
            algo = center_undirected_tree_vertex_restricted_unweighted(self.modelmatrix.get_weights(), matrix)
        elif algo_name == "Center Undirected Network Absolute":
            from education.algorithms.center_undirected_network_absolute import center_undirected_network_absolute
            matrix, nodes = self.modelmatrix.get_matrix()
            algo = center_undirected_network_absolute(self.modelmatrix.get_weights(), matrix)
        elif algo_name == "Pareto Median Undirected Network":
            from education.algorithms.pareto_median_undirected_network import pareto_median_undirected_network
            matrix, nodes = self.modelmatrix.get_matrix()
            algo = pareto_median_undirected_network(self.modelmatrix.get_weights(), matrix)
        elif algo_name == "Out Center Directed Network":
            from education.algorithms.out_center_directed_network import out_center_directed_network
            matrix, nodes = self.modelmatrix.get_matrix()
            algo = out_center_directed_network(self.modelmatrix.get_weights(), matrix)   
        elif algo_name == "In Center Directed Network":
            from education.algorithms.in_center_directed_network import in_center_directed_network
            matrix, nodes = self.modelmatrix.get_matrix()
            algo = in_center_directed_network(self.modelmatrix.get_weights(), matrix)   
        elif algo_name == "Center Directed Network":
            from education.algorithms.center_directed_network import center_directed_network
            matrix, nodes = self.modelmatrix.get_matrix()
            algo = center_directed_network(self.modelmatrix.get_weights(), matrix)
        elif algo_name == "Pareto Median Undirected Network Vertex-Restricted":
            from education.algorithms.pareto_median_undirected_network_vertex_restricted import pareto_median_undirected_network_vertex_restricted
            matrix, nodes = self.modelmatrix.get_matrix()
            algo = pareto_median_undirected_network_vertex_restricted(self.modelmatrix.get_weights(), matrix)
        elif algo_name == "Pareto Median Directed Network":
            from education.algorithms.pareto_median_directed_network import pareto_median_directed_network
            matrix, nodes = self.modelmatrix.get_matrix()
            algo = pareto_median_directed_network(self.modelmatrix.get_weights(), matrix)
        elif algo_name == "Pareto In Median Directed Network":
            from education.algorithms.pareto_in_median_directed_network import pareto_in_median_directed_network
            matrix, nodes = self.modelmatrix.get_matrix()
            algo = pareto_in_median_directed_network(self.modelmatrix.get_weights(), matrix)
        elif algo_name == "Pareto Out Median Directed Network":
            from education.algorithms.pareto_out_median_directed_network import pareto_out_median_directed_network
            matrix, nodes = self.modelmatrix.get_matrix()
            algo = pareto_out_median_directed_network(self.modelmatrix.get_weights(), matrix)
        else:
            self.view.network_education_solution_label.setText("No valid algorithm selected.")
            self.view.network_education_solution_label.setVisible(True)
            return
        
        
        if "tree" in algo_name.lower():
            if not nx.is_tree(self.modelmatrix.get_graph()):
                self.view.network_education_solution_label.setText("No result: the network is not a tree.")
                self.view.network_education_solution_label.setVisible(True)
                self.view.network_education_matrix_table.setVisible(False)
                # show the network without the marks of the previous result
                self.view.network_education_plot_canvas.plot_solution_node(self.modelmatrix.get_graph(), [], self.modelmatrix.get_pos())
                dialog = InvalidTreeInputDialogEducation(self.view)
                dialog.exec_()
                return

        optimal_nodes, solution_string, solution_path, _ = algo.run()   # no CSV output in the Education Mode

        # every problem in its own colour, the earlier ones stay, with its short name in the legend ("Median" for "Median
        # Undirected Network", "In Center" for "In Center Directed Network")
        short = algo_name.replace(" Network", "").replace(" Undirected", "").replace(" Directed", "")
        self.view.network_education_plot_canvas.plot_solution_node(self.modelmatrix.get_graph(), optimal_nodes, self.modelmatrix.get_pos(), short)
        
        # Check if the solution path checkbox is selected and update the text field
        if self.view.network_education_show_solution_checkbox.isChecked():
            # Zeige Ergebnis und Lösungspfad
            self.view.network_education_solution_label.setText(
                solution_path
                + "\n\n"
                + solution_string
            )
        else:
            self.view.network_education_solution_label.setText(solution_string)


        self.view.network_education_solution_label.setVisible(True)
        self.view.network_education_matrix_table.setVisible(False)

        # Pareto median with two weight vectors: its front can be shown instead of the solution box ("Pareto Front")
        weights = self.modelmatrix.get_weights()
        if algo_name.startswith("Pareto") and optimal_nodes and len(weights) == 2 and all(isinstance(w, (list, tuple)) for w in weights):
            self.view.network_education_set_pareto_front(AdditionalMethods.pareto_front(
                optimal_nodes, matrix, weights, AdditionalMethods.network_direction(algo_name)))

        # No location exists (e.g. the customers are not connected): also show the reason in a warning dialog
        if solution_string.startswith("No result: "):
            reason = solution_string[len("No result: "):].split("\n")[0]
            QMessageBox.warning(self.view, "No Result", reason[0].upper() + reason[1:])

    def handle_network_education_algo_changed(self, algo_name):
        """
        Handler for when the algo selection changes in the Education network page.
        It adapts the gui to the algo.add
        :param: the selected algo_name
        """
        self.view.network_education_hide_pareto_front()     # the front belongs to the last run of the former algorithm
        if algo_name == "Shortest Path":
            self.view.network_education_show_default_view()
        elif algo_name == "Median Directed Network":
            self.view.network_education_show_default_view()
        elif algo_name == "Median Undirected Network":
            self.view.network_education_show_default_view()
        elif algo_name == "In Median Directed Network":
            self.view.network_education_show_default_view()
        elif algo_name == "Out Median Directed Network":
            self.view.network_education_show_default_view()
        elif algo_name == "Center Undirected Network Vertex-Restricted":
           self.view.network_education_show_default_view()
        elif algo_name == "Center Undirected Tree Absolute Unweighted":
            self.view.network_education_show_default_view()
        elif algo_name == "Median Undirected Tree":
            self.view.network_education_show_default_view()
        elif algo_name == "Center Undirected Tree Vertex-Restricted Unweighted":
            self.view.network_education_show_default_view()
        elif algo_name == "Please Select Algorithm...":
            self.view.network_education_show_default_view()
            self.handle_network_education_reset()
        else:
            return

    def handle_network_education_random_instance(self):
        self.view.network_education_hide_pareto_front()

        try:
            nodes = int(
                self.view.network_education_random_nodes_input.text()
            )
        except ValueError:
            self.view.network_education_solution_label.setText(
                "Please enter a number between 2 and 10."
            )
            self.view.network_education_solution_label.show()
            return

        if nodes < 2 or nodes > 10:
            self.view.network_education_solution_label.setText(
                "Please enter a number between 2 and 10."
            )
            self.view.network_education_solution_label.show()
            return

        try:
            number_of_weights = int(
                self.view.network_education_random_weights_input.text()
            )
        except ValueError:
            number_of_weights = 0

        if number_of_weights < 1:
            self.view.network_education_solution_label.setText(
                "Please enter at least 1 weight vector."
            )
            self.view.network_education_solution_label.show()
            return

        # The algorithm list depends on the number of weight vectors (several: only Pareto). Filling it selects
        # "Please Select Algorithm..." and so resets the page, therefore it comes before the new instance is built
        self.view.network_education_weights_input.setText(str(number_of_weights))
        self.view.update_network_education_algorithms()

        # Empty matrix
        matrix = []

        for i in range(nodes):
            row = []

            for j in range(nodes):
                if i == j:
                    row.append("n")
                else:
                    row.append(None)

            matrix.append(row)

        # Generate random edges depending on network type
        if self.modelmatrix.is_directed():

            # Directed:
            # Every direction gets its own random value
            for i in range(nodes):
                for j in range(nodes):
                    if i != j:
                        matrix[i][j] = random.randint(1, 10)

        else:

            # Undirected:
            # Generate one value and mirror it
            for i in range(nodes):
                for j in range(i + 1, nodes):

                    value = random.randint(1, 10)

                    matrix[i][j] = value
                    matrix[j][i] = value

        # Save matrix
        self.modelmatrix.set_matrix(matrix, nodes)

        # Node weights: one weight vector with weight 1 for every node; several weight vectors (Pareto median)
        # get random weights, otherwise all objective functions would be the same
        if number_of_weights == 1:
            all_weights = [[1] * nodes]
            self.modelmatrix.set_weights(all_weights[0])
        else:
            all_weights = [[random.randint(1, 5) for _ in range(nodes)] for _ in range(number_of_weights)]
            self.modelmatrix.set_weights(all_weights)

        # Display matrix
        table = self.view.network_education_matrix_table

        table.clear()
        table.setRowCount(nodes)
        table.setColumnCount(nodes + number_of_weights)

        for weight_index in range(number_of_weights):
            if number_of_weights == 1:
                header = "weights"
            else:
                header = f"weights {weight_index + 1}"
            table.setHorizontalHeaderItem(
                nodes + weight_index,
                QTableWidgetItem(header)
            )

        for row in range(nodes):

            for col in range(nodes):

                item = QTableWidgetItem(
                    str(matrix[row][col])
                )

                if row == col:
                    item.setFlags(
                        item.flags() & ~Qt.ItemIsEditable
                    )

                table.setItem(
                    row,
                    col,
                    item
                )

            for weight_index in range(number_of_weights):
                table.setItem(
                    row,
                    nodes + weight_index,
                    QTableWidgetItem(str(all_weights[weight_index][row]))
                )

        self.view.network_education_solution_label.hide()

        self.view.network_education_graph_button.setEnabled(True)

        table.setEditTriggers(
            QTableWidget.AllEditTriggers
        )
    
    def handle_network_education_example_changed(self, example_name):
        """
        Loads a predefined network example into the Education network matrix table.
        The matrix is only displayed here. It is saved/plotted later via Save Matrix.
        """
        self.view.network_education_hide_pareto_front()

        if example_name == "Please Select Example...":
            return

        dataset = self.model.get_network_problem(example_name)

        if dataset is None:
            self.view.network_education_solution_label.setText(
                "Example not found."
            )
            self.view.network_education_solution_label.setVisible(True)
            return

        adj_matrix = dataset.get("matrix")
        coords = dataset.get("coords", [])
        dataset_weights = dataset.get("weights")
        directed = dataset.get("directed", False)

        if adj_matrix is None:
            self.view.network_education_solution_label.setText(
                "Example has no matrix."
            )
            self.view.network_education_solution_label.setVisible(True)
            return

        node_count = len(adj_matrix)

        if node_count > 10:
            self.view.network_education_solution_label.setText(
                f"Example has {node_count} nodes. "
                "Education Mode currently supports max. 10 nodes."
            )
            self.view.network_education_solution_label.setVisible(True)
            return

        # Netzwerktyp des Beispiels übernehmen
        self.modelmatrix.set_directed(directed)

        # --------------------------------------------------
        # Gewichte bestimmen
        # --------------------------------------------------

        if dataset_weights is not None:
            # Neues Format:
            # ein Vektor: [1, 2, 3, 4]
            # mehrere Vektoren: [[1, 2, 3, 4], [3, 1, 2, 1]]
            weights = dataset_weights
        else:
            # Altes Format:
            # Gewichte weiterhin aus coords lesen
            weights = []

            for i in range(node_count):
                if (
                    i < len(coords)
                    and len(coords[i]) >= 4
                ):
                    weights.append(coords[i][2])
                else:
                    weights.append(1)

        # Prüfen, ob mehrere Gewichtsvektoren vorliegen
        multiple_weights = (
            isinstance(weights, (list, tuple))
            and len(weights) > 0
            and isinstance(weights[0], (list, tuple))
        )

        if multiple_weights:
            number_of_weights = len(weights)
        else:
            number_of_weights = 1

        # Validierung der Gewichtsvektoren
        if multiple_weights:
            for weight_vector in weights:
                if len(weight_vector) != node_count:
                    self.view.network_education_solution_label.setText(
                        "The number of weights does not match "
                        "the number of nodes."
                    )
                    self.view.network_education_solution_label.setVisible(True)
                    return
        elif len(weights) != node_count:
            self.view.network_education_solution_label.setText(
                "The number of weights does not match "
                "the number of nodes."
            )
            self.view.network_education_solution_label.setVisible(True)
            return

        # --------------------------------------------------
        # Alten Zustand zurücksetzen
        # --------------------------------------------------

        self.modelmatrix.clear_matrix()
        self.modelmatrix.graph = None
        self.modelmatrix.pos = None

        self.view.network_education_solution_label.clear()
        self.view.network_education_solution_label.setVisible(False)
        self.view.network_education_matrix_table.setVisible(True)
        self.view.network_education_plot_canvas.show_network_default_axes()

        # Gewichte direkt im Model speichern
        self.modelmatrix.set_weights(weights)

        # Eingabefelder an das Beispiel anpassen
        self.view.network_education_nodes_input.setText(str(node_count))
        self.view.network_education_weights_input.setText(
            str(number_of_weights)
        )

        # Algorithmusliste anhand der Gewichtsanzahl aktualisieren
        self.view.update_network_education_algorithms()

        # --------------------------------------------------
        # Tabelle erstellen
        # --------------------------------------------------

        table = self.view.network_education_matrix_table

        table.clear()
        table.setRowCount(node_count)
        table.setColumnCount(
            node_count + number_of_weights
        )

        # Matrixspalten benennen
        for column in range(node_count):
            table.setHorizontalHeaderItem(
                column,
                QTableWidgetItem(str(column + 1))
            )

        # Gewichtsspalten benennen
        for weight_index in range(number_of_weights):
            column = node_count + weight_index

            if number_of_weights == 1:
                header = "weights"
            else:
                header = f"weights {weight_index + 1}"

            table.setHorizontalHeaderItem(
                column,
                QTableWidgetItem(header)
            )

        # --------------------------------------------------
        # Adjazenzmatrix eintragen
        # --------------------------------------------------

        for row in range(node_count):
            for col in range(node_count):
                value = adj_matrix[row][col]

                if row == col:
                    text = "n"
                elif value is None:
                    text = ""
                else:
                    text = str(value)

                item = QTableWidgetItem(text)

                if directed:
                    # Gerichtetes Netzwerk:
                    # nur Diagonale sperren
                    if row == col:
                        item.setFlags(
                            item.flags() & ~Qt.ItemIsEditable
                        )
                else:
                    # Ungerichtetes Netzwerk:
                    # Diagonale und untere Hälfte sperren
                    if row >= col:
                        item.setFlags(
                            item.flags() & ~Qt.ItemIsEditable
                        )

                table.setItem(row, col, item)

            # Knotennamen als Zeilenüberschrift
            if (
                row < len(coords)
                and len(coords[row]) >= 4
            ):
                node_name = coords[row][3]
            else:
                node_name = str(row + 1)

            table.setVerticalHeaderItem(
                row,
                QTableWidgetItem(node_name)
            )

        # --------------------------------------------------
        # Gewichtsspalten eintragen
        # --------------------------------------------------

        if multiple_weights:
            for weight_index, weight_vector in enumerate(weights):
                column = node_count + weight_index

                for row in range(node_count):
                    table.setItem(
                        row,
                        column,
                        QTableWidgetItem(
                            str(weight_vector[row])
                        )
                    )
        else:
            for row in range(node_count):
                table.setItem(
                    row,
                    node_count,
                    QTableWidgetItem(str(weights[row]))
                )

        table.setEditTriggers(QTableWidget.AllEditTriggers)

        # Save-Matrix-Ablauf wieder aktivieren
        self.view.network_education_graph_button.setEnabled(True)
        self.view.network_education_matrix_button.setEnabled(True)

    '__________________________________________________________________________________________________________________'
    'Controller methods for Dualoc Education Mode'

    def handle_dualoc_dataset_changed(self, dataset_name: str):
        if dataset_name in (
            "",
            "Please Select Dataset...",
            "Please Select Example..."
        ):
            return

        problem = self.model.get_dualoc_problem(dataset_name)

        if problem is None:
            self.view.dualoc_info_text.setText(
                "Example not found."
            )
            self.view.dualoc_info_text.show()
            return

        # Tiefe Kopie der Matrixzeilen
        c_ij = [
            row.copy()
            for row in problem["c_ij_original"]
        ]
        f_j = problem["f_j"].copy()

        number_customers = len(c_ij)
        number_facilities = len(f_j)

        self.view.number_clients.setText(
            str(number_customers)
        )
        self.view.number_facilities.setText(
            str(number_facilities)
        )

        table = self.view.table_matrix_dualoc

        table.clear()
        table.setRowCount(number_customers + 1)
        table.setColumnCount(number_facilities)

        table.setHorizontalHeaderLabels(
            [
                f"Facility {j + 1}"
                for j in range(number_facilities)
            ]
        )

        table.setVerticalHeaderLabels(
            [
                f"Customer {i + 1}"
                for i in range(number_customers)
            ] + ["f(j)"]
        )

        # c(i,j) eintragen
        for i in range(number_customers):
            for j in range(number_facilities):
                table.setItem(
                    i,
                    j,
                    QTableWidgetItem(str(c_ij[i][j]))
                )

        # f(j) in der letzten Zeile eintragen
        fixed_cost_row = number_customers

        for j in range(number_facilities):
            table.setItem(
                fixed_cost_row,
                j,
                QTableWidgetItem(str(f_j[j]))
            )

        table.setEditTriggers(
            QTableWidget.AllEditTriggers
        )
        table.resizeColumnsToContents()

        self.dualocObject.clear()
        self.view.dualoc_save_matrix_button.setEnabled(True)
        self.view.dualoc_show_matrix_widget()
        self.view.dualoc_info_text.hide()
                
        self.view.number_clients.setEnabled(True)
        self.view.number_facilities.setEnabled(True)

        self.view.button_create_matrix_dualoc.setEnabled(True)
        self.view.dualoc_example_instance_button.setEnabled(True)
        self.view.table_matrix_dualoc.setEditTriggers(QTableWidget.AllEditTriggers)

    def handle_dualocEducation_create_matrix(self):
        try:
            number_customers = int(
                self.view.number_clients.text().strip()
            )
            number_facilities = int(
                self.view.number_facilities.text().strip()
            )
        except ValueError:
            QMessageBox.warning(
                self.view,
                "Invalid Input",
                "Please enter valid integer values for customers and facilities."
            )
            return

        if number_customers <= 0 or number_facilities <= 0:
            QMessageBox.warning(
                self.view,
                "Invalid Input",
                "Customers and facilities must be greater than zero."
            )
            return

        table = self.view.table_matrix_dualoc

        table.clear()
        table.setRowCount(number_customers + 1)
        table.setColumnCount(number_facilities)

        table.setHorizontalHeaderLabels(
            [
                f"Facility {j + 1}"
                for j in range(number_facilities)
            ]
        )

        table.setVerticalHeaderLabels(
            [
                f"Customer {i + 1}"
                for i in range(number_customers)
            ] + ["f(j)"]
        )

        # Alle Zellen tatsächlich anlegen
        for row in range(number_customers + 1):
            for column in range(number_facilities):
                table.setItem(
                    row,
                    column,
                    QTableWidgetItem("")
                )

        table.setEditTriggers(QTableWidget.AllEditTriggers)

        horizontal_header = table.horizontalHeader()
        horizontal_header.setStretchLastSection(False)
        horizontal_header.setSectionResizeMode(QHeaderView.Fixed)
        horizontal_header.setDefaultSectionSize(120)

        vertical_header = table.verticalHeader()
        vertical_header.setStretchLastSection(False)
        vertical_header.setSectionResizeMode(QHeaderView.Fixed)
        vertical_header.setDefaultSectionSize(38)

    def handle_dualocEducation_random_instance(self):
        try:
            number_customers = int(
                self.view.dualoc_random_customers_input.text().strip()
            )

            number_facilities = int(
                self.view.dualoc_random_facilities_input.text().strip()
            )

        except ValueError:
            QMessageBox.warning(
                self.view,
                "Invalid Input",
                "Please enter valid integer values for customers and facilities."
            )
            return

        # Maximum 10 customers / facilities
        if (
            number_customers < 1
            or number_customers > 10
            or number_facilities < 1
            or number_facilities > 10
        ):
            QMessageBox.warning(
                self.view,
                "Invalid Input",
                "Customers and facilities must be between 1 and 10."
            )
            return

        # Use existing matrix creation method
        self.view.number_clients.setText(
            str(number_customers)
        )

        self.view.number_facilities.setText(
            str(number_facilities)
        )

        self.handle_dualocEducation_create_matrix()

        table = self.view.table_matrix_dualoc

        # Random assignment costs c(i,j)
        for customer in range(number_customers):
            for facility in range(number_facilities):

                value = random.randint(0, 10)

                table.setItem(
                    customer,
                    facility,
                    QTableWidgetItem(str(value))
                )

        # Random facility costs f(j)
        fixed_cost_row = number_customers

        for facility in range(number_facilities):

            value = random.randint(1, 10)

            table.setItem(
                fixed_cost_row,
                facility,
                QTableWidgetItem(str(value))
            )

        self.view.dualoc_info_text.hide()

    def handle_dualocEducation_back(self):
        self.handle_discrete_education_reset()
        self.view.show_education_options()

    def handle_discrete_education_reset(self):
        self.dualocObject.clear()
        self.view.number_clients.clear()
        self.view.number_facilities.clear()

        self.view.table_matrix_dualoc.clear()
        self.view.table_matrix_dualoc.setRowCount(0)
        self.view.table_matrix_dualoc.setColumnCount(0)

        self.view.dualoc_table_widget.clear()
        self.view.dualoc_table_widget.setRowCount(0)
        self.view.dualoc_table_widget.setColumnCount(0)

        self.view.dualoc_solution_text.clear()
        self.view.discrete_education_show_solution_checkbox.setChecked(False)

        self.view.combo_algos_discrete_education.setCurrentIndex(0)
        self.view.dualoc_combo_datasets.setCurrentIndex(0)
        self.view.dualoc_combo_datasets.setVisible(False)

        self.view.dualoc_info_text.clear()
        self.view.dualoc_info_text.hide()

        self.view.dualoc_show_matrix_widget()

        self.view.table_matrix_dualoc.setEditTriggers(QTableWidget.AllEditTriggers)

        self.view.number_clients.setEnabled(True)
        self.view.number_facilities.setEnabled(True)

        self.view.button_create_matrix_dualoc.setEnabled(True)
        self.view.dualoc_example_instance_button.setEnabled(True)
        self.view.dualoc_save_matrix_button.setEnabled(True)

    def read_dualoc_cost_matrix(self):
        table = self.view.table_matrix_dualoc

        if table.rowCount() < 2 or table.columnCount() == 0:
            raise ValueError(
                "Please create or load a matrix first."
            )

        # Letzte Zeile gehört zu f(j)
        number_customers = table.rowCount() - 1
        number_facilities = table.columnCount()

        matrix = []

        for row in range(number_customers):
            row_values = []

            for column in range(number_facilities):
                item = table.item(row, column)

                if item is None or not item.text().strip():
                    raise ValueError(
                        f"Missing value for customer {row + 1}, "
                        f"facility {column + 1}."
                    )

                text = item.text().strip().replace(",", ".")

                try:
                    value = float(text)
                    if not math.isfinite(value):   # float() also accepts "nan" and "inf"
                        raise ValueError
                except ValueError:
                    raise ValueError(
                        f"Invalid value for customer {row + 1}, "
                        f"facility {column + 1}."
                    )

                if value < 0:
                    raise ValueError(
                        f"The value for customer {row + 1}, "
                        f"facility {column + 1} must be 0 or greater."
                    )

                row_values.append(value)

            matrix.append(row_values)

        return matrix

    def read_dualoc_fixed_costs(self):
        table = self.view.table_matrix_dualoc

        if table.rowCount() < 2 or table.columnCount() == 0:
            raise ValueError(
                "Please create or load a matrix first."
            )

        fixed_cost_row = table.rowCount() - 1
        fixed_costs = []

        for column in range(table.columnCount()):
            item = table.item(
                fixed_cost_row,
                column
            )

            if item is None or not item.text().strip():
                raise ValueError(
                    f"Missing fixed cost for facility {column + 1}."
                )

            text = item.text().strip().replace(",", ".")

            try:
                value = float(text)
                if not math.isfinite(value):   # float() also accepts "nan" and "inf"
                    raise ValueError
            except ValueError:
                raise ValueError(
                    f"Invalid fixed cost for facility {column + 1}."
                )

            if value < 0:
                raise ValueError(
                    f"The fixed cost of facility {column + 1} must be 0 or greater."
                )

            fixed_costs.append(value)

        return fixed_costs

    def handle_dualoc_solve(self, mode: str):

        if not self.dualocObject.c_ij or not self.dualocObject.f_j:
            self.view.dualoc_info_text.setText(
                "Please save the matrix before solving."
            )
            self.view.dualoc_info_text.show()
            self.view.dualoc_show_matrix_widget()
            return

        if mode != "education":
            return

        algorithm_name = (
            self.view.combo_algos_discrete_education.currentText()
        )

        if algorithm_name == "Please Select Algorithm...":
            self.view.dualoc_info_text.setText(
                "Please select an algorithm."
            )
            self.view.dualoc_info_text.show()
            return

        c_ij = self.dualocObject.c_ij
        f_j = self.dualocObject.f_j

        # --------------------------------------------------
        # DUALOC
        # --------------------------------------------------
        if algorithm_name == "Dualoc":
            from education.algorithms.dualoc import dualoc

            algo = dualoc(
                c_ij,
                f_j
            )

        # --------------------------------------------------
        # GREEDY
        # --------------------------------------------------
        elif algorithm_name == "Greedy Heuristic":
            from education.algorithms.greedy_heuristic import greedy_heuristic

            algo = greedy_heuristic(
                c_ij,
                f_j
            )

        # --------------------------------------------------
        # INTERCHANGE
        # --------------------------------------------------
        elif algorithm_name == "Interchange Heuristic":
            from education.algorithms.interchange_heuristic import interchange_heuristic

            num_facilities = len(f_j)

            dialog = InterchangeStartSolutionDialog(
                num_facilities,
                self.view
            )

            if dialog.exec_() != QDialog.Accepted:
                return

            X = dialog.opened_facilities


            algo = interchange_heuristic(
                c_ij,
                f_j,
                X
            )

        else:
            return

        # --------------------------------------------------
        # RUN SELECTED ALGORITHM
        # --------------------------------------------------

        solution_output, result_string, solution_path, _ = (   # no CSV output in the Education Mode
            algo.run()
        )


        # --------------------------------------------------
        # DISPLAY SOLUTION
        # --------------------------------------------------
        self.display_final_discrete_solution(
            solution_output,
            result_string,
            solution_path,
            mode
        )

        self.view.dualoc_info_text.hide()
        self.view.dualoc_show_solution_widget()

    def display_final_discrete_solution(
        self,
        solution_output,
        result_string,
        solution_path,
        mode
    ):
        table = self.view.dualoc_table_widget

        c_ij = self.dualocObject.c_ij
        f_j = self.dualocObject.f_j

        num_clients = len(c_ij)
        num_facilities = len(f_j)

        table.clear()
        table.setRowCount(num_clients)
        table.setColumnCount(num_facilities)

        # Headers
        table.setHorizontalHeaderLabels(
            [f"Facility {j + 1}" for j in range(num_facilities)]
        )

        table.setVerticalHeaderLabels(
            [f"Client {i + 1}" for i in range(num_clients)]
        )

        # Kostenmatrix anzeigen
        for i in range(num_clients):
            for j in range(num_facilities):
                table.setItem(
                    i,
                    j,
                    QTableWidgetItem(str(c_ij[i][j]))
                )

        # Lösung grafisch markieren
        self.view.highlight_discrete_solution(
            solution_output,
            mode
        )

        table.resizeColumnsToContents()
        table.resizeRowsToContents()

        # --------------------------------------------------
        # TEXTUELLE LÖSUNG
        # --------------------------------------------------
        if mode == "education":

            text = str(result_string)

            # Lösungsweg nur anzeigen, wenn Checkbox aktiviert ist
            if self.view.discrete_education_show_solution_checkbox.isChecked():

                if solution_path:
                    text += (
                        "\n\n"
                        "________________________________________\n\n"
                        "Solution Path:\n\n"
                        + str(solution_path)
                    )

            self.view.dualoc_solution_text.setPlainText(without_numpy_wrappers(text))

    def handle_dualocEducation_save_matrix(self):
        try:
            c_ij = self.read_dualoc_cost_matrix()
            f_j = self.read_dualoc_fixed_costs()
        except ValueError as error:
            self.view.dualoc_info_text.setText(str(error))
            self.view.dualoc_info_text.show()
            return

        if not c_ij:
            self.view.dualoc_info_text.setText(
                "Please create or load a matrix first."
            )
            self.view.dualoc_info_text.show()
            return

        if len(c_ij[0]) != len(f_j):
            self.view.dualoc_info_text.setText(
                "The number of matrix columns must match "
                "the number of facility costs."
            )
            self.view.dualoc_info_text.show()
            return

        # Im Modell speichern
        self.dualocObject.c_ij = c_ij
        self.dualocObject.f_j = f_j

        # Eingabe sperren
        self.view.table_matrix_dualoc.setEditTriggers(
            QTableWidget.NoEditTriggers)

        # Eingabefelder ebenfalls sperren
        self.view.number_clients.setEnabled(False)
        self.view.number_facilities.setEnabled(False)

        self.view.button_create_matrix_dualoc.setEnabled(False)
        self.view.dualoc_example_instance_button.setEnabled(False)

        # Save-Button nach erfolgreichem Speichern sperren
        self.view.dualoc_save_matrix_button.setEnabled(False)

        self.view.dualoc_info_text.setText(
            "Matrix saved successfully."
        )
        self.view.dualoc_info_text.show()

        self.view.dualoc_show_matrix_widget()

    "__________________________________________________________________________________________________________________"
    "Controller methods for Districting Education Mode signals"

    def _districting_education_number_of_areas(self, field):
        """The number of basic areas in the field (1 to 30), or None after a warning."""
        try:
            number = int(field.text().strip())
        except ValueError:
            number = 0
        if not 1 <= number <= 30:
            QMessageBox.warning(self.view, "Invalid Input", "Please enter a number of basic areas between 1 and 30.")
            return None
        return number

    def _districting_education_new_areas(self, areas):
        """Shows new basic areas (table and drawing) without a result."""
        self.view.fill_districting_education_table(areas)
        self.view.districting_education_result_text.clear()
        self.view.districting_education_plot_canvas.plot_districts([area for area in areas if None not in area])

    def handle_districting_education_dataset_changed(self, name):
        """An example: its basic areas and parameters."""
        problem = self.model.get_districting_problem(name)
        if problem is None:
            return
        self.view.districting_education_p.setValue(problem["p"])
        self.view.districting_education_K.setValue(problem["K"])
        self.view.districting_education_beta.setValue(problem["beta"])
        self._districting_education_new_areas(problem["areas"])

    def handle_districting_education_create_table(self):
        """Own instance: an empty table with the given number of basic areas."""
        number = self._districting_education_number_of_areas(self.view.districting_education_own_areas_input)
        if number is not None:
            self._districting_education_new_areas([(None, None, None)] * number)

    def handle_districting_education_random_instance(self):
        """Random instance: basic areas at different integer points from 0 to 10, activities from 1 to 10."""
        number = self._districting_education_number_of_areas(self.view.districting_education_random_areas_input)
        if number is None:
            return
        places = set()
        while len(places) < number:
            places.add((random.randint(0, 10), random.randint(0, 10)))
        self._districting_education_new_areas([(x, y, random.randint(1, 10)) for x, y in places])

    def handle_districting_education_table_changed(self):
        """A changed cell: the drawing of the filled rows, without the result of the last run."""
        areas, _ = self.view.districting_education_areas()
        self.view.districting_education_result_text.clear()
        self.view.districting_education_plot_canvas.plot_districts(areas)

    def handle_districting_education_run_algorithm(self):
        """Runs the chosen districting algorithm on the basic areas of the table and shows the districts."""
        view = self.view
        areas, invalid = view.districting_education_areas()
        p = view.districting_education_p.value()
        if not areas and not invalid:
            QMessageBox.warning(view, "Invalid Input", "Please enter basic areas first (own, example or random instance).")
            return
        if invalid:
            QMessageBox.warning(view, "Invalid Input", "Please enter a number for x, y and the activity w in row(s) "
                                + ", ".join(map(str, invalid)) + ".")
            return
        if len(areas) > 30:
            QMessageBox.warning(view, "Invalid Input", "The Education Mode computes at most 30 basic areas.")
            return
        if any(w < 0 for _, _, w in areas) or sum(w for _, _, w in areas) <= 0:
            QMessageBox.warning(view, "Invalid Input", "The activities must not be negative, and at least one must be "
                                                       "greater than 0.")
            return
        if p > len(areas):
            QMessageBox.warning(view, "Invalid Input", f"The number of districts p = {p} must not exceed the number of "
                                                       f"basic areas ({len(areas)}).")
            return
        algo_name = view.districting_education_combo_algos.currentText()
        if algo_name == "Recursive Partitioning":
            from education.algorithms.recursive_partitioning import recursive_partitioning

            algo = recursive_partitioning(areas, p, view.districting_education_K.value(),
                                          view.districting_education_beta.value())
        else:
            view.districting_education_result_text.setText("No valid algorithm selected.")
            return
        result, result_str, solution_path, _ = algo.run()
        view.districting_education_plot_canvas.plot_districts(areas, result)
        if view.districting_education_show_solution_checkbox.isChecked():
            view.districting_education_result_text.setText(
                solution_path + "\n\n" + "_" * 84 + "\n\n" + result_str)
        else:
            view.districting_education_result_text.setText(result_str)

    def handle_districting_education_reset(self):
        """Remove All Areas and Back: no basic areas, no result, the examples and algorithms unselected."""
        self.view.districting_education_combo_datasets.setCurrentIndex(0)
        self.view.districting_education_combo_algos.setCurrentIndex(0)
        self._districting_education_new_areas([])
