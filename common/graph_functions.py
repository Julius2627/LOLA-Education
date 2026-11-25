import networkx as nx
from numbers import Integral, Real
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QVBoxLayout, QWidget
import matplotlib
from matplotlib.patches import Polygon, Rectangle
from numbers import Real

# Two opposite arcs between the same two nodes (u -> v and v -> u) are drawn as curves, each bent to the right of its
# direction, so that they do not lie on top of each other; all other arcs and the edges stay straight
BEND = 0.15
CURVED = f"arc3,rad={BEND}"


def curve_points(start, end, curved, t1=0.0, t2=1.0, points=20):
    """
    The line of an edge or arc from start to end ((x, y), y upwards) as it is drawn, from t1 to t2: straight, or (curved:
    one of two opposite arcs) the curve of CURVED, as matplotlib computes it: the quadratic Bezier curve whose control
    point lies BEND times (dy, -dx) beside the middle, i.e. right of the direction (dx, dy). The graph pages draw it in
    pixels, the map on a local projection (applied/leaflet_map.arc_latlngs).

    :return: [(x, y), ...]: the points at t1 and t2 (straight), or `points` points of the curve at equal steps of its
             parameter (one point: at t1)
    """
    (xa, ya), (xb, yb) = start, end
    ts = [t1 + (t2 - t1) * k / max(points - 1, 1) for k in range(points)] if curved or points == 1 else [t1, t2]
    if not curved:
        return [(xa + t * (xb - xa), ya + t * (yb - ya)) for t in ts]
    xc, yc = (xa + xb) / 2 + BEND * (yb - ya), (ya + yb) / 2 - BEND * (xb - xa)
    return [((1 - t) ** 2 * xa + 2 * (1 - t) * t * xc + t * t * xb, (1 - t) ** 2 * ya + 2 * (1 - t) * t * yc + t * t * yb)
            for t in ts]


class PlotCanvas(FigureCanvas):
    """
    PlotCanvas provides a matplotlib canvas integrated into a PyQt5 widget.
    It supports plotting network graphs, data points, and solution points.
    """

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # Create a new matplotlib figure with a single subplot.
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # Initialize the FigureCanvas with the created figure.
        super().__init__(fig)
        self.setParent(parent)

    def plot_graph(self, graph, pos=None):
        """
        Plots a networkx graph on the canvas.
        :param graph: A networkx graph object.
        :param pos: The positions of the nodes (the layout stored with the graph); a new layout if None.
        """
        self.axes.clear()
        if pos is None:
            pos = nx.spring_layout(graph)  # Compute positions for all nodes.

        labels = {}
        for node in graph.nodes():
            weight = graph.nodes[node].get("weight", "")
            labels[node] = f"{node}\n({weight})"

        # Draw nodes, edges, and labels (two opposite arcs as curves).
        curved = self._opposite_arcs(graph)
        nx.draw(graph, pos, ax=self.axes, labels=labels, node_color='skyblue',
                node_size=2000, font_size=15, arrows=True, edgelist=[e for e in graph.edges() if e not in curved])
        self._draw_curved_arcs(graph, pos, curved)
        self._draw_edge_labels(graph, pos, curved)
        self.draw()

    @staticmethod
    def _opposite_arcs(graph):
        """The arcs (u, v) of a directed graph whose opposite arc (v, u) exists as well: they are drawn as curves (CURVED)."""
        return {(u, v) for u, v in graph.edges() if u != v and graph.has_edge(v, u)} if graph.is_directed() else set()

    def _draw_curved_arcs(self, graph, pos, arcs, **options):
        """Draws the arcs as curves (CURVED) with arrows that end at the border of the nodes (node_size 2000); options:
        e.g. their colour and width."""
        if arcs:
            nx.draw_networkx_edges(graph, pos, edgelist=list(arcs), ax=self.axes, node_size=2000, arrows=True,
                                   connectionstyle=CURVED, **options)

    def _draw_edge_labels(self, graph, pos, curved):
        """The lengths of the edges and arcs at 0.3 of their way; on the curved arcs along the curve."""
        edge_labels = nx.get_edge_attributes(graph, "weight")
        nx.draw_networkx_edge_labels(graph, pos, ax=self.axes, label_pos=0.3,
                                     edge_labels={e: w for e, w in edge_labels.items() if e not in curved})
        if curved:
            nx.draw_networkx_edge_labels(graph, pos, ax=self.axes, label_pos=0.3, node_size=2000, connectionstyle=CURVED,
                                         edge_labels={e: w for e, w in edge_labels.items() if e in curved})

    '''def plot_solution_node(self, graph, node_index, pos):
        self.axes.clear()
        labels = {}
        for node in graph.nodes():
            weight = graph.nodes[node].get("weight", "")
            labels[node] = f"{node}\n({weight})"
        nx.draw(graph, pos, ax=self.axes, labels=labels, node_color='skyblue',
                node_size=2000, font_size=15, arrows=True)
        nx.draw_networkx_nodes(graph, pos, nodelist=[node_index], ax=self.axes,
                            node_color='red', node_size=2200)
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, ax=self.axes, edge_labels=edge_labels, label_pos=0.3)
        self.draw()'''
    
    def plot_solution_node(self, graph, solutions, pos):
        """
        Plots a graph and highlights optimal solutions.

        Expected solution format:
        - Integer i:
          highlight node i, where i is 0-based

        - Tuple (i, j):
          highlight the complete edge/arc from i to j

        - Tuple ((i, j), t):
          highlight the point on edge/arc i -> j at fraction t

        - Tuple ((i, j), (t1, t2)):
          highlight the interval from fraction t1 to fraction t2 on edge/arc i -> j (a whole arc, from 0 to 1, of a
          directed graph: as red arrow, on the curve if its opposite arc exists)
        """

        self.axes.clear()

        if graph is None:
            self.draw()
            return

        if pos is None:
            pos = nx.spring_layout(graph)

        # Normalize: allow both one single solution and a list of solutions
        if solutions is None:
            solutions = []
        elif not isinstance(solutions, list):
            solutions = [solutions]

        is_directed = graph.is_directed()

        # Labels with optional node weights
        labels = {}
        for node in graph.nodes():
            weight = graph.nodes[node].get("weight", "")
            if weight == "":
                labels[node] = str(node)
            else:
                labels[node] = f"{node}\n({weight})"

        # Draw base graph (two opposite arcs as curves)
        curved = self._opposite_arcs(graph)
        nx.draw(
            graph,
            pos,
            ax=self.axes,
            labels=labels,
            node_color="skyblue",
            node_size=2000,
            font_size=15,
            arrows=is_directed,
            edgelist=[e for e in graph.edges() if e not in curved]
        )
        self._draw_curved_arcs(graph, pos, curved)

        highlighted_nodes = []
        highlighted_edges = []
        highlighted_arcs = []           # whole arcs of a directed graph
        highlighted_points = []
        highlighted_intervals = []

        for solution in solutions:

            # Case 1: Integer i -> highlight node i
            if self._is_int_like(solution):
                node = int(solution)

                if node in graph.nodes():
                    highlighted_nodes.append(node)

                continue

            if not isinstance(solution, tuple) or len(solution) != 2:
                continue

            first, second = solution

            # Case 2: Tuple (i, j) -> highlight complete edge/arc and both endpoint nodes
            if (
                self._is_int_like(first)
                and self._is_int_like(second)
            ):
                u = int(first)
                v = int(second)

                if self._edge_exists(graph, u, v):
                    highlighted_edges.append((u, v))
                    highlighted_nodes.extend([u, v])

                continue

            # Cases 3 and 4: Tuple ((i, j), t) or ((i, j), (t1, t2))
            if (
                isinstance(first, tuple)
                and len(first) == 2
                and self._is_int_like(first[0])
                and self._is_int_like(first[1])
            ):
                u = int(first[0])
                v = int(first[1])

                if u not in pos or v not in pos:
                    continue

                if not self._edge_exists(graph, u, v):
                    continue

                # Case 4: Tuple ((i, j), (t1, t2)) -> highlight interval
                if isinstance(second, tuple) and len(second) == 2:
                    t1, t2 = second

                    if not self._is_real_like(t1) or not self._is_real_like(t2):
                        continue

                    if is_directed and abs(t1) < 1e-9 and abs(t2 - 1) < 1e-9:      # a whole arc
                        highlighted_arcs.append((u, v))
                        continue

                    p1 = self._point_on_edge(pos, u, v, t1)
                    p2 = self._point_on_edge(pos, u, v, t2)

                    highlighted_intervals.append((p1, p2))

                # Case 3: Tuple ((i, j), t) -> highlight point on edge
                elif self._is_real_like(second):
                    point = self._point_on_edge(pos, u, v, second)
                    highlighted_points.append(point)

        # Highlight complete edges/arcs (an arrow size only for directed networks: on undirected ones
        # networkx draws plain lines and warns about the arrow size)
        if highlighted_edges:
            arrow_options = {"arrows": True, "arrowsize": 25} if is_directed else {"arrows": False}
            nx.draw_networkx_edges(
                graph,
                pos,
                edgelist=highlighted_edges,
                ax=self.axes,
                edge_color="red",
                width=5,
                **arrow_options
            )

        # Highlight whole arcs: red arrows, on the curve of two opposite arcs
        straight_arcs = [arc for arc in highlighted_arcs if arc not in curved]
        if straight_arcs:
            nx.draw_networkx_edges(graph, pos, edgelist=straight_arcs, ax=self.axes, node_size=2000, arrows=True,
                                   arrowsize=25, edge_color="red", width=5)
        self._draw_curved_arcs(graph, pos, [arc for arc in highlighted_arcs if arc in curved], arrowsize=25,
                               edge_color="red", width=5)

        # Highlight intervals on edges/arcs
        for p1, p2 in highlighted_intervals:
            self.axes.plot(
                [p1[0], p2[0]],
                [p1[1], p2[1]],
                color="red",
                linewidth=6,
                solid_capstyle="round",
                zorder=5
            )

        # Highlight points on edges/arcs
        if highlighted_points:
            x_values, y_values = zip(*highlighted_points)
            self.axes.scatter(
                x_values,
                y_values,
                color="red",
                s=250,
                edgecolors="black",
                zorder=6
            )

        # Highlight nodes
        if highlighted_nodes:
            nx.draw_networkx_nodes(
                graph,
                pos,
                nodelist=highlighted_nodes,
                ax=self.axes,
                node_color="red",
                node_size=2200
            )

        # Redraw labels, otherwise highlighted nodes may cover text
        nx.draw_networkx_labels(
            graph,
            pos,
            labels=labels,
            ax=self.axes,
            font_size=15
        )

        # Edge labels
        self._draw_edge_labels(graph, pos, curved)

        self.axes.axis("off")
        self.draw()

    def plot_data(self, data):
        """
        Plots data points on the canvas.
        :param data: A list of tuples, each representing a point (x, y).
        """
        if data == []:
            return
        self.axes.clear()
        # Unpack x and y values from the data points.
        x, y = zip(*[(d[0], d[1]) for d in data])
        self.axes.scatter(x, y, color='blue')
        self.axes.set_title("Data Points")
        self.draw()

    def plot_solution(self, solution):
        """
        Plots solution on the canvas.

        New format:
            [0, (x, y)]              -> point
            [1, (x1, y1), (x2, y2)]  -> line segment
            [2, (x1, y1), (x2, y2)]  -> rectangle

        Old formats:
            (x, y)                   -> point
            [(x, y)]                 -> point
            [(x1, y1), (x2, y2)]     -> several points
        """

        if solution is None or solution == []:
            return

        def is_point(obj):
            return (
                isinstance(obj, (tuple, list))
                and len(obj) >= 2
                and isinstance(obj[0], Real)
                and isinstance(obj[1], Real)
            )

        # New format only if:
        # solution[0] is 0/1/2 AND solution[1] is really a point
        is_new_format = (
            isinstance(solution, (list, tuple))
            and len(solution) >= 2
            and solution[0] in (0, 1, 2)
            and is_point(solution[1])
        )

        if is_new_format:
            solution_type = solution[0]
            p1 = solution[1]
            p2 = solution[2] if len(solution) > 2 else None

        else:
            # Old format: one point as (x, y)
            if is_point(solution):
                solution_type = 0
                p1 = solution
                p2 = None

            # Old format: one or multiple points as [(x, y), ...]
            elif (
                isinstance(solution, list)
                and len(solution) >= 1
                and all(is_point(p) for p in solution)
            ):
                x, y = zip(*solution)
                self.axes.scatter(x, y, color="red", zorder=5)
                self.axes.set_title("Solution")
                self.draw()
                return

            else:
                return

        if solution_type == 0:
            x, y = p1
            self.axes.scatter([x], [y], color="red", zorder=5)

        elif solution_type == 1:
            if p2 is None or not is_point(p2):
                return

            x1, y1 = p1
            x2, y2 = p2

            self.axes.plot([x1, x2], [y1, y2], color="red", linewidth=3, zorder=4)
            self.axes.scatter([x1, x2], [y1, y2], color="red", zorder=5)

        elif solution_type == 2:
            if p2 is None or not is_point(p2):
                return

            x1, y1 = p1
            x2, y2 = p2

            left = min(x1, x2)
            bottom = min(y1, y2)
            width = abs(x2 - x1)
            height = abs(y2 - y1)

            rect = Rectangle(
                (left, bottom),
                width,
                height,
                edgecolor="red",
                facecolor="red",
                alpha=0.25,
                linewidth=2,
                zorder=3
            )

            self.axes.add_patch(rect)
            self.axes.scatter([x1, x2], [y1, y2], color="red", zorder=5)

        else:
            return

        self.axes.set_title("Solution")
        self.draw()

    def plot_districts(self, areas, result=None):
        """
        Draws the basic areas of a districting problem, numbered 1, 2, ... with their activity, and, with a result
        of a districting algorithm, the districts: the areas in the colour of their district, the convex hull of
        every district (filled lightly) with its name D1, D2, ... and the lines L1, L2, ... of the partition (dashed,
        the part inside the convex hull of the areas they divided).

        :param areas: [(x, y, w), ...]
        :param result: None, or {"districts": [[areas of D1 (1-based)], ...], "hulls": [[corners], ...],
                       "lines": [((x1, y1), (x2, y2)), ...]} (see education/algorithms/recursive_partitioning.py)
        """
        self.axes.clear()
        if not areas:
            self.axes.set_aspect("auto")        # the default view has fixed limits
            self.show_default_axes()
            return
        colours = matplotlib.colormaps["tab10" if result is None or len(result["districts"]) <= 10 else "tab20"]
        district_of = {}
        if result is not None:
            for j, district in enumerate(result["districts"]):
                for i in district:
                    district_of[i] = j
        for i, (x, y, w) in enumerate(areas, start=1):
            colour = colours(district_of[i] % colours.N) if i in district_of else "blue"
            self.axes.scatter([x], [y], color=colour, zorder=5)
            self.axes.annotate(f"{i} ({w:g})", (x, y), textcoords="offset points", xytext=(4, 4), fontsize=9, zorder=6)
        if result is not None:
            for j, (district, hull) in enumerate(zip(result["districts"], result["hulls"])):
                colour = colours(j % colours.N)
                if len(hull) >= 3:
                    self.axes.add_patch(Polygon(hull, closed=True, facecolor=colour, edgecolor=colour, alpha=0.2,
                                                linewidth=2, zorder=2))
                elif len(hull) == 2:
                    self.axes.plot(*zip(*hull), color=colour, alpha=0.4, linewidth=6, solid_capstyle="round", zorder=2)
                centre = (sum(areas[i - 1][0] for i in district) / len(district),
                          sum(areas[i - 1][1] for i in district) / len(district))
                self.axes.annotate(f"D{j + 1}", centre, textcoords="offset points", xytext=(0, -14), ha="center",
                                   fontsize=11, fontweight="bold", color=colour, zorder=6)
            for number, (start, end) in enumerate(result["lines"], start=1):
                self.axes.plot([start[0], end[0]], [start[1], end[1]], color="black", linestyle="--", linewidth=1.5,
                               zorder=4)
                self.axes.annotate(f"L{number}", ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2),
                                   textcoords="offset points", xytext=(3, -10), fontsize=9, zorder=6)
        self.axes.set_aspect("equal", adjustable="datalim")
        self.axes.grid(True)
        self.axes.set_title("Districts" if result is not None else "Basic Areas")
        self.draw()

    def show_default_axes(self):
        """
        Clears the canvas and draws a simple default view,
        e.g. some x/y-limits and an empty title, so that
        we have a 'coordinate system' look instead of a blank space.
        """
        self.axes.clear()
        self.axes.set_xlim(-10, 10)
        self.axes.set_ylim(-10, 10)
        self.axes.set_title("Empty Graph - Default View")
        self.axes.grid(True)
        self.draw()

    def show_network_default_axes(self):
        self.axes.clear()
        self.axes.set_title("Empty Graph - Default View")
        self.axes.grid(False)
        self.axes.axis("off")
        self.draw()
    
    def plot_pareto_front(self, front, mine=None):
        """
        Draws the Pareto front of two weight vectors (front: AdditionalMethods.pareto_front) in the objective function
        space: the Pareto optimal vertices as red points, the Pareto optimal parts of edges as red lines whose open ends
        are hollow circles (a part with constant values, e.g. a whole arc, as a red square), the other vertices as grey
        points; next to every point its vertex or edge (locations with the same values share a label). mine: the values
        (f1, f2) of the user's own solution (Applied Mode, "My Solution"), a purple star.
        """
        vertices, parts, others = front
        axes, labels = self.axes, {}        # labels: position -> ([texts], colour)

        def label(position, text, colour):
            key = (round(position[0], 9), round(position[1], 9))
            texts, old = labels.get(key, ([], colour))
            labels[key] = (texts + [text], "red" if "red" in (old, colour) else colour)

        axes.clear()
        axes.axis("on")
        for k, (x, y) in others:
            axes.plot(x, y, "o", color="0.7", zorder=1)
            label((x, y), str(k), "0.45")
        for (a, b), points in parts:
            xs, ys = zip(*points)
            if len(points) == 1:
                axes.plot(xs, ys, "s", color="red", zorder=3)
            else:
                axes.plot(xs, ys, "-", color="red", linewidth=2, zorder=2)
                axes.plot([xs[0], xs[-1]], [ys[0], ys[-1]], "o", markerfacecolor="white", markeredgecolor="red", zorder=3)
            middle = points[len(points) // 2] if len(points) != 2 else ((xs[0] + xs[1]) / 2, (ys[0] + ys[1]) / 2)
            label(middle, f"({a}, {b})", "red")
        for k, (x, y) in vertices:
            axes.plot(x, y, "o", color="red", zorder=4)
            label((x, y), str(k), "red")
        for (x, y), (texts, colour) in labels.items():
            axes.annotate(", ".join(texts), (x, y), textcoords="offset points", xytext=(5, 5), fontsize=9, color=colour)
        if mine is not None:
            axes.plot(*mine, "*", color="#8E44AD", markersize=16, markeredgecolor="white", zorder=5)
            axes.annotate("My solution", mine, textcoords="offset points", xytext=(8, -14), fontsize=9, color="#8E44AD")
        axes.set_xlabel("f\u00b9 (weight vector 1)")
        axes.set_ylabel("f\u00b2 (weight vector 2)")
        axes.set_title("Pareto front (red); the other vertices in grey")
        axes.grid(True, alpha=0.3)
        axes.margins(0.12)
        self.figure.set_layout_engine("constrained")     # the axis labels stay inside a small canvas (also after a resize)
        self.draw_idle()        # drawn when shown (the front is often plotted while it is hidden)

    '''________________Hilfs-Funktionen________________'''
    def _is_int_like(self, value):
        return isinstance(value, Integral) and not isinstance(value, bool)

    def _is_real_like(self, value):
        return isinstance(value, Real) and not isinstance(value, bool)

    def _point_on_edge(self, pos, u, v, t):
        """
        Returns the point at fraction t on edge u -> v.
        t=0 means node u, t=1 means node v.
        """
        t = max(0.0, min(1.0, float(t)))

        x_u, y_u = pos[u]
        x_v, y_v = pos[v]

        x = x_u + t * (x_v - x_u)
        y = y_u + t * (y_v - y_u)

        return x, y

    def _edge_exists(self, graph, u, v):
        """
        For directed graphs, only u -> v is valid.
        For undirected graphs, u-v and v-u are equivalent.
        """
        if graph.has_edge(u, v):
            return True

        if not graph.is_directed() and graph.has_edge(v, u):
            return True

        return False


class ParetoFrontView(QWidget):
    """
    The Pareto front of two weight vectors on the network pages of both modes: the plot (PlotCanvas.plot_pareto_front)
    and below it "Zoom to front" (ticked: the view around the Pareto optimal points and parts, the grey vertices outside
    it are counted in the label; unticked: the view around all vertices) and a hint, which shows f1 and f2 under the
    mouse. With the mouse: the wheel (or two fingers on a trackpad) zooms around the mouse, dragging moves the view, a
    double-click goes back to the view of "Zoom to front".
    """
    HINT = "Wheel: zoom · drag: move · double-click: back"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.canvas = PlotCanvas(self, width=5, height=4)
        self.zoom = QCheckBox("Zoom to front")
        self.zoom.setChecked(True)
        self.zoom.toggled.connect(self.set_view)
        self.hint = QLabel(self.HINT)
        self.front, self.mine, self.drag = None, None, None
        for event, slot in (("scroll_event", self.wheel), ("button_press_event", self.press),
                            ("motion_notify_event", self.move), ("button_release_event", self.release),
                            ("axes_leave_event", lambda event: self.hint.setText(self.HINT))):
            self.canvas.mpl_connect(event, slot)
        row = QHBoxLayout()
        row.addWidget(self.zoom)
        row.addStretch()
        row.addWidget(self.hint)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas, 1)
        layout.addLayout(row)

    def plot(self, front, mine=None):
        """Draws the front (AdditionalMethods.pareto_front) in the view that "Zoom to front" chooses; mine: the values
        (f1, f2) of the user's own solution (Applied Mode), shown in either view."""
        self.front, self.mine = front, mine
        self.canvas.plot_pareto_front(front, mine)
        self.set_view()

    def set_view(self):
        """The axes around the front (Zoom to front) or around all vertices."""
        if self.front is None:
            return
        vertices, parts, others = self.front
        shown = [point for _, point in vertices] + [point for _, points in parts for point in points]
        if not self.zoom.isChecked():
            shown += [point for _, point in others]
        if self.mine is not None:
            shown.append(self.mine)
        axes = self.canvas.axes
        for k, set_limits in ((0, axes.set_xlim), (1, axes.set_ylim)):
            low, high = min(point[k] for point in shown), max(point[k] for point in shown)
            margin = (high - low) * 0.12 or max(abs(high) * 0.05, 1.0)       # one value only: a margin around it
            set_limits(low - margin, high + margin)
        (x1, x2), (y1, y2) = axes.get_xlim(), axes.get_ylim()
        outside = sum(not (x1 <= x <= x2 and y1 <= y <= y2) for _, (x, y) in others)
        self.zoom.setText(f"Zoom to front ({outside} outside)" if outside else "Zoom to front")
        self.zoom.setToolTip("Ticked: the view around the Pareto front" + (f"; {outside} grey "
                             f"{'vertex lies' if outside == 1 else 'vertices lie'} outside it" if outside else "")
                             + ".\nUnticked: the view around all vertices.")
        self.canvas.draw_idle()

    def wheel(self, event):
        """Mouse wheel or trackpad: zooms around the mouse (up: in), in small steps for a trackpad."""
        if event.inaxes is None or self.front is None:
            return
        factor = 1.2 ** -event.step
        axes = self.canvas.axes
        for get, set_limits, centre in ((axes.get_xlim, axes.set_xlim, event.xdata), (axes.get_ylim, axes.set_ylim, event.ydata)):
            low, high = get()
            set_limits(centre - (centre - low) * factor, centre + (high - centre) * factor)
        self.canvas.draw_idle()

    def press(self, event):
        """Double-click: back to the view of "Zoom to front"; press: starts moving the view."""
        if event.inaxes is None or self.front is None:
            return
        if event.dblclick:
            self.drag = None
            self.set_view()
        elif event.button == 1:
            axes = self.canvas.axes
            self.drag = (event.x, event.y, axes.get_xlim(), axes.get_ylim())

    def move(self, event):
        """Shows f1 and f2 under the mouse; while the button is held, the view follows the mouse."""
        if event.inaxes is not None and event.xdata is not None:
            self.hint.setText(f"f\u00b9 = {event.xdata:.4g}, f\u00b2 = {event.ydata:.4g}")
        if self.drag is None:
            return
        x0, y0, (x1, x2), (y1, y2) = self.drag
        box = self.canvas.axes.bbox
        dx, dy = (event.x - x0) * (x2 - x1) / box.width, (event.y - y0) * (y2 - y1) / box.height
        self.canvas.axes.set_xlim(x1 - dx, x2 - dx)
        self.canvas.axes.set_ylim(y1 - dy, y2 - dy)
        self.canvas.draw_idle()

    def release(self, event):
        self.drag = None
