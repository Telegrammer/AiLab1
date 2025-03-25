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