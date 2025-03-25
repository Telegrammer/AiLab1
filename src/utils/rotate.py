import math

from PyQt5.QtCore import QPoint


def rotate_point(point: QPoint, angle_degrees: float, center: QPoint) -> QPoint:

    # Конвертируем градусы в радианы
    angle_rad = math.radians(angle_degrees)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    # Смещаем точку относительно центра вращения
    x_rel = point.x() - center.x()
    y_rel = point.y() - center.y()

    # Применяем матрицу поворота
    new_x = x_rel * cos_a - y_rel * sin_a
    new_y = x_rel * sin_a + y_rel * cos_a

    # Возвращаем смещение обратно и округляем до целых
    return QPoint(
        round(new_x + center.x()),
        round(new_y + center.y())
    )


def rotate_arrow(begin: QPoint, destination: QPoint):
    x1, y1 = begin.x(), begin.y()
    x2, y2 = destination.x(), destination.y()
    a = y2 - y1
    c = x2 - x1
    b = math.sqrt(a ** 2 + c ** 2)

    angle = 0
    if a == 0 and b == c:
        angle = 0
    elif c == 0 and -a == b:
        angle = 90
    elif a == 0 and b == -c:
        angle = 180
    elif c == 0 and a == b:
        angle = 270
    elif a < 0 and b > 0:
        angle = math.degrees(math.acos((b * b + c * c - a * a) / (2.0 * b * c)))
    else:
        angle = 360 - math.degrees(math.acos((b * b + c * c - a * a) / (2.0 * b * c)))

    return angle