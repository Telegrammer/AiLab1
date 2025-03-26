from PyQt5.QtCore import QPoint, QRect, Qt
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtWidgets import QWidget

from graph.models import TreeModel
from graph.models.search_algorithms import SearchAlgorithm, SearchBFS
from graph.presenters.vertex import Vertex
from graph.view import TreeResearchView
from utils import rotate_point


class GraphResearchPresenter(QWidget, TreeResearchView):

    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.__painter: QPainter = QPainter(self)

        self.__tree: TreeModel = TreeModel()
        self.__vertexes: dict[str, Vertex] = {}
        self.__found_way: list[str] = []
        self.__algorithms: dict[str, SearchAlgorithm] = {
            "В ширину": SearchBFS(),
            "В глубину": SearchBFS()
        }

        self.__current_algorithm: SearchAlgorithm = self.__algorithms[self.graphAlgorithmComboBox.currentText()]

        self.removeEdgeButton.setEnabled(False)
        self.findWayButton.setEnabled(False)
        self.addEdgeButton.clicked.connect(self.add_edge)
        self.edgeList.itemSelectionChanged.connect(
            lambda: self.__focus_change([self.removeEdgeButton], [])
        )
        self.startVertexInput.currentTextChanged.connect(
            lambda: self.findWayButton.setEnabled(bool(self.startVertexInput.currentText()))
        )

        self.graphAlgorithmComboBox.currentTextChanged.connect(

            lambda: self.set_algorithm(self.__algorithms[self.graphAlgorithmComboBox.currentText()])
        )
        self.findWayButton.clicked.connect(self.set_way)

        self.removeEdgeButton.clicked.connect(self.remove_edge)

    def resizeEvent(self, event):
        self.paintEvent(event)

    def paintEvent(self, event):
        self.__painter.begin(self)
        self.draw_tree(self.__painter)
        self.__painter.end()

    def set_algorithm(self, name: str):
        self.__current_algorithm = name

    def set_way(self):
        steps_count, way = self.__current_algorithm.search(self.__tree, self.startVertexInput.currentText(),
                                                           self.endVertexInput.currentText())
        self.stepsCountLabel.setText(f"Количество шагов: {steps_count}")
        self.foundWayLabel.setText(" -> ".join(way))
        self.__found_way = way
        self.update()

    def add_edge(self):
        start_vertex, end_vertex = (self.firstVertexLineEdit.text(), self.secondVertexLineEdit.text())

        if not self.__tree.have_edge(start_vertex, end_vertex) and start_vertex != end_vertex:
            self.__tree.add_edge(start_vertex, end_vertex)

            self.__vertexes[start_vertex] = Vertex(self.graphViewWidget, value=start_vertex, position=QPoint())
            self.__vertexes[end_vertex] = Vertex(self.graphViewWidget, value=end_vertex, position=QPoint())

            self.edgeList.addItem(f"({start_vertex}, {end_vertex})")

            if self.startVertexInput.findText(start_vertex) == -1:
                self.startVertexInput.addItem(start_vertex)

            if self.startVertexInput.findText(end_vertex) == -1:
                self.startVertexInput.addItem(end_vertex)

            if self.endVertexInput.findText(start_vertex) == -1:
                self.endVertexInput.addItem(start_vertex)

            if self.endVertexInput.findText(end_vertex) == -1:
                self.endVertexInput.addItem(end_vertex)

        self.firstVertexLineEdit.setText("")
        self.secondVertexLineEdit.setText("")
        self.update()

    def remove_edge(self):
        start_vertex, end_vertex = self.edgeList.currentItem().text()[1: -1].split(", ")
        self.edgeList.takeItem(self.edgeList.currentRow())
        self.edgeList.clearSelection()
        self.removeEdgeButton.setEnabled(False)
        deleted_nodes: list[str] = self.__tree.remove_edge(start_vertex, end_vertex)
        for node in deleted_nodes:
            self.__vertexes.pop(node)

            if self.startVertexInput.findText(node) != -1:
                self.startVertexInput.removeItem(self.startVertexInput.findText(node))
            if self.endVertexInput.findText(node) != -1:
                self.endVertexInput.removeItem(self.endVertexInput.findText(node))

        self.__found_way = []
        self.stepsCountLabel.setText("Количество шагов:")
        self.update()

    def draw_tree(self, qp: QPainter):
        center = QPoint(self.graphViewWidget.width() // 2, self.graphViewWidget.height() // 2)
        current_pos: QPoint = QPoint(self.graphViewWidget.width() // 2, 100)

        default_pen = QPen(Qt.black, 2, Qt.SolidLine)
        default_vertex_brush = QBrush(Qt.white)

        qp.setPen(default_pen)
        qp.setBrush(default_vertex_brush)

        nodes_list: list[str] = self.__vertexes.keys()

        # draw vertexes
        way_brush = QBrush(Qt.darkGreen)
        for node in nodes_list:
            if node in self.__found_way:
                qp.setBrush(way_brush)
            else:
                qp.setBrush(default_vertex_brush)

            self.__vertexes[node].set_position(current_pos)
            self.__vertexes[node].draw(qp)
            current_pos = rotate_point(current_pos, 360 / len(nodes_list), center)

        # draw_edges
        default_edge_brush = QBrush(Qt.red)
        way_edge_brush = QBrush(Qt.green)
        way_edge_pen = QPen(Qt.darkGreen, 2, Qt.SolidLine)
        qp.setBrush(default_edge_brush)
        for node in nodes_list:
            if not self.__tree.have_children(node):
                continue
            children = self.__tree.get_node_info(node)
            print(self.__found_way)
            for child in children:
                try:
                    if node in self.__found_way and self.__found_way[self.__found_way.index(node) + 1] == child:
                        qp.setBrush(way_edge_brush)
                        qp.setPen(way_edge_pen)
                    else:
                        qp.setBrush(default_edge_brush)
                        qp.setPen(default_pen)
                except IndexError:
                    qp.setBrush(default_edge_brush)
                    qp.setPen(default_pen)

                start_pos = self.__vertexes[node].find_closest_join(self.__vertexes[child].get_center())
                end_pos: QPoint = self.__vertexes[child].find_closest_join(start_pos)
                qp.drawLine(start_pos, end_pos)
                qp.drawEllipse(QRect(end_pos.x() - 4, end_pos.y() - 4, 8, 8))

    @staticmethod
    def __focus_change(focused_widgets: list[QWidget], unfocused_widgets: list[QWidget]):
        for widget in focused_widgets:
            widget.setEnabled(True)
        for widget in unfocused_widgets:
            widget.setEnabled(False)
