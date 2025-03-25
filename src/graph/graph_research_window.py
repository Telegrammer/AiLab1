from PyQt5.QtCore import QPoint, QLine
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QTransform, QFont, QImage

from graph.models import TreeModel
from graph.view import TreeResearchView
from utils import rotate_point


class GraphResearchPresenter(QWidget, TreeResearchView):

    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.__painter: QPainter = QPainter()
        self.__painter.setFont(QFont("Arial black", 20))

        self.__tree = TreeModel()
        self.removeEdgeButton.setEnabled(False)
        self.addEdgeButton.clicked.connect(self.add_edge)
        self.edgeList.itemSelectionChanged.connect(
            lambda: self.__focus_change([self.removeEdgeButton], [])
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
            self.edgeList.addItem(f"({start_vertex}, {end_vertex})")
            self.__tree.add_edge(start_vertex, end_vertex)
        self.firstVertexLineEdit.setText("")
        self.secondVertexLineEdit.setText("")
        self.update()

    def remove_edge(self):
        start_vertex, end_vertex = self.edgeList.currentItem().text()[1: -1].split(", ")
        self.edgeList.takeItem(self.edgeList.currentRow())
        self.edgeList.clearSelection()
        self.removeEdgeButton.setEnabled(False)
        self.__tree.remove_edge(start_vertex, end_vertex)
        self.update()

    def draw_tree(self, qp: QPainter):

        icon = QImage("./ui/media/arrow_head_small.png")
        center = QPoint(self.graphViewWidget.width() // 2, self.graphViewWidget.height() // 2)
        current_pos: QPoint = QPoint()
        current_pos.setX(self.graphViewWidget.width() // 2)
        current_pos.setY(100)

        nodes: dict[str, QPoint] = {node: QPoint() for node in self.__tree.get_nodes()}
        nodes_list: list[str] = nodes.keys()

        for node in nodes_list:
            nodes[node].setX(current_pos.x())
            nodes[node].setY(current_pos.y())
            current_pos = rotate_point(current_pos, 360 / len(nodes), center)

        for node in nodes_list:
            start_pos: QPoint = nodes[node]
            if not self.__tree.have_children(node):
                continue
            children = self.__tree.get_node_info(node)
            for child in children:
                end_pos: QPoint = nodes[child]
                qp.drawLine(start_pos, end_pos)
                qp.drawImage(end_pos, icon)

        current_pos: QPoint = QPoint()
        current_pos.setX(self.graphViewWidget.width() // 2)
        current_pos.setY(100)

        for node in nodes_list:
            qp.drawText(current_pos, node)
            current_pos = rotate_point(current_pos, 360 / len(nodes), center)

    @staticmethod
    def __focus_change(focused_widgets: list[QWidget], unfocused_widgets: list[QWidget]):
        for widget in focused_widgets:
            widget.setEnabled(True)
        for widget in unfocused_widgets:
            widget.setEnabled(False)
