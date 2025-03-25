import math

from PyQt5.QtCore import QPoint, QSize, QRect
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtWidgets import QPushButton, QWidget

from utils import rotate_point


class Vertex(QWidget):

    def __init__(self,
                 parent: QWidget,
                 value: str,
                 position: QPoint,
                 size: int = 30,
                 joint_count: int = 4):

        QWidget.__init__(self, parent)
        self.__value: str = value
        self.__joint_count: int = joint_count
        self.setFixedSize(QSize(size, size))
        self.__center: QPoint = QPoint()
        self.__joint_points: list[QPoint] = []
        self.set_position(position)


    def set_position(self, pos: QPoint) -> None:
        self.setGeometry(QRect(pos.x(), pos.y(), self.width(), self.height()))
        joint_pos: QPoint = QPoint(self.x() + self.width() // 2, self.y())
        self.__center: QPoint = QPoint(self.x() + self.width() // 2, self.y() + self.height() // 2)
        self.__joint_points: list[QPoint] = []
        for _ in range(self.__joint_count):
            self.__joint_points.append(joint_pos)
            joint_pos = rotate_point(joint_pos, 360 / self.__joint_count, self.__center)

    def find_closest_join(self, outer_position: QPoint) -> QPoint:

        closest_joint: QPoint = None
        min_distance: int = -1

        for joint in self.__joint_points:
            distance: int = math.hypot(joint.x() - outer_position.x(), joint.y() - outer_position.y())
            if not (min_distance == -1 or distance < min_distance):
                continue
            closest_joint = joint
            min_distance = distance

        return closest_joint

    def get_center(self) -> QPoint:
        return self.__center

    def draw(self, qp: QPainter):
        qp.drawEllipse(QRect(self.x(), self.y(), self.width(), self.height()))
        qp.drawText(self.__center.x() - 3, self.__center.y(), self.__value)