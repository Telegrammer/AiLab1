from PyQt5.QtCore import QPoint, QRect, Qt
from PyQt5.QtGui import QPainter, QPixmap, QPen, QBrush
from PyQt5.QtWidgets import QWidget

from graph.models import TreeModel
from graph.view import TreeResearchView
from graph.presenters.vertex import Vertex
from utils import rotate_point, rotate_arrow


class GraphResearchPresenter(QWidget, TreeResearchView):

    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.__painter: QPainter = QPainter(self)

        self.__tree: TreeModel = TreeModel()
        self.__vertexes: dict[str, Vertex] = {}

        self.removeEdgeButton.setEnabled(False)
        self.findWayButton.setEnabled(False)
        self.addEdgeButton.clicked.connect(self.add_edge)
        self.edgeList.itemSelectionChanged.connect(
            lambda: self.__focus_change([self.removeEdgeButton], [])
        )
        self.startVertexInput.currentTextChanged.connect(
            lambda: self.findWayButton.setEnabled(bool(self.startVertexInput.currentText()))
        )

        self.removeEdgeButton.clicked.connect(self.remove_edge)

    def resizeEvent(self, event):
        self.paintEvent(event)

    def paintEvent(self, event):
        self.__painter.begin(self)
        self.draw_tree(self.__painter)
        self.__painter.end()

    def add_edge(self):
        start_vertex, end_vertex = (self.firstVertexLineEdit.text(), self.secondVertexLineEdit.text())

        if not self.__tree.have_edge(start_vertex, end_vertex) and start_vertex != end_vertex:
            self.__tree.add_edge(start_vertex, end_vertex)

            self.__vertexes[start_vertex] = Vertex(self, value=start_vertex, position=QPoint())
            self.__vertexes[end_vertex] = Vertex(self, value=end_vertex, position=QPoint())

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
                self.startVertexInput.removeItem(self.startVertexInput.findText(node) )
            if self.endVertexInput.findText(node) != -1:
                self.endVertexInput.removeItem(self.endVertexInput.findText(node))

        self.update()

    def draw_tree(self, qp: QPainter):
        center = QPoint(self.graphViewWidget.width() // 2, self.graphViewWidget.height() // 2)
        current_pos: QPoint = QPoint(self.graphViewWidget.width() // 2, 100)

        pen = QPen(Qt.black, 2, Qt.SolidLine)
        brush = QBrush(Qt.white)
        qp.setPen(pen)
        qp.setBrush(brush)

        nodes_list: list[str] = self.__vertexes.keys()

        for node in nodes_list:
            self.__vertexes[node].set_position(current_pos)
            self.__vertexes[node].draw(qp)
            current_pos = rotate_point(current_pos, 360 / len(nodes_list), center)

        brush = QBrush(Qt.red)
        qp.setBrush(brush)
        for node in nodes_list:
            if not self.__tree.have_children(node):
                continue
            children = self.__tree.get_node_info(node)
            for child in children:
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
