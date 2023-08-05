from pulseapi import *
from math import sqrt, atan2, cos, sin, fabs, tan
from math import pi
import numpy as np


def getproportionpoint(point, segment, length, dx, dy):
    factor = segment / length
    return [point[0] - dx * factor,
            point[1] - dy * factor]


def get_length(dx, dy):
    """
    Вычисление длины вектора в плоскости ХУ
    :param dx: Вектор Х
    :param dy: Вектор У
    :return: Длину вектора
    """
    return sqrt(dx * dx + dy * dy)


def calculate_start_and_end_angle(p1, p, p2, radius):
    """
    Нахождение угла начала дуги, ее размах, центр вписанной окружности, радиус вписанной окружности
    https://stackoverflow.com/questions/24771828/algorithm-for-creating-rounded-corners-in-a-polygon/24780108

    :param p1: Координаты предыдущей точки [x,y,z] в СИ
    :param p: Координаты настоящей точки [x,y,z] в СИ
    :param p2: Координаты следующей точки [x,y,z] в СИ
    :param radius: Радиус скругления дуги R в СИ
    :return: startAngle, sweepAngle, circlePoint, radius
    """
    # Вектор 1
    dx1 = p[0] - p1[0]
    dy1 = p[1] - p1[1]

    # Вектор 2
    dx2 = p[0] - p2[0]
    dy2 = p[1] - p2[1]

    # Угол между двумя векторами
    angle = atan2(dy1, dx1) - atan2(dy2, dx2)
    assert angle != 0, 'Не правильно заданы точки: расстояние между ними слишком мало'

    assert radius > 0, "Радиус должен быть больше нуля"
    # Длина отрезка от угла до точки касания вписанной окружности радиусом r
    segment = radius / fabs(tan(angle / 2))

    # Находит минимальную длину векторов,чтобы построить равнобедренный треугольник
    length1 = get_length(dx1, dy1)
    length2 = get_length(dx2, dy2)
    length = min(length1, length2)

    assert length > 0, "Не правильно заданы точки: расстояние между ними слишком мало"
    # Проверка на правильность задания радиуса,если задали описанную окружность,то меняем радиуса на максимально вписанной окружности
    if segment > length:
        segment = length
        radius = length * fabs(tan(angle))

    # Точки пересечения рассчитываются по соотношению координаты вектора, длины вектора и длины сегмента.
    c1 = getproportionpoint(p, segment, length1, dx1, dy1)
    c2 = getproportionpoint(p, segment, length2, dx2, dy2)

    # Расчет центра окружности
    dx = p[0] * 2 - c1[0] - c2[0]
    dy = p[1] * 2 - c1[1] - c2[1]
    L = get_length(dx, dy)
    d = get_length(segment, radius)
    circlePoint = getproportionpoint(p, d, L, dx, dy)

    # Рачет начального и конечного угла дуги
    startAngle = atan2((c1[1] - circlePoint[1]), (c1[0] - circlePoint[0]))
    endAngle = atan2((c2[1] - circlePoint[1]), (c2[0] - circlePoint[0]))

    # Размах дуги
    sweepAngle = endAngle - startAngle

    # Проверки на правильность задания угла размаха дуги
    if sweepAngle <= -pi:
        sweepAngle = -(sweepAngle + pi)
    if sweepAngle >= pi:
        sweepAngle = pi - sweepAngle

    return startAngle, sweepAngle, circlePoint, radius


def convert_position2list(position):
    return [list(position[0].to_dict()['point'].values()),
            list(position[0].to_dict()['rotation'].values())]


def points_of_rounding(startAngle, sweepAngle, radius, circlePoint, target):
    sign = np.sign(sweepAngle)
    points = []
    degreeFactor = 180 / pi
    r = int(fabs(sweepAngle * degreeFactor))

    procent = 15

    step = int(r / 100 * procent)
    for i in range(0, r, step):
        pointx = circlePoint[0] + cos(startAngle + sign * i / degreeFactor) * radius
        pointy = circlePoint[1] + sin(startAngle + sign * i / degreeFactor) * radius
        points.append(position([pointx, pointy, convert_position2list(target)[0][2]], convert_position2list(target)[1],
                               target[0].to_dict()['actions']))

    return points


def rounding_motion(target_list):
    """
    Вычисляет список точек траектории с учетом скругления углов
    :param target_list:
    :return:
    """

    new_target_list = []
    radius_prev = 0
    for i in range(len(target_list)):

        if len(target_list[i]) == 2 and target_list[i][1][0] != 0:

            startAngle, sweepAngle, circlePoint, radius = calculate_start_and_end_angle(
                convert_position2list(target_list[i - 1])[0],
                convert_position2list(target_list[i])[0],
                convert_position2list(target_list[i + 1])[0], target_list[i][1][0])

            dx1 = convert_position2list(target_list[i])[0][0] - convert_position2list(target_list[i - 1])[0][0]
            dy1 = convert_position2list(target_list[i])[0][1] - convert_position2list(target_list[i - 1])[0][1]

            dx2 = convert_position2list(target_list[i])[0][0] - convert_position2list(target_list[i + 1])[0][0]
            dy2 = convert_position2list(target_list[i])[0][1] - convert_position2list(target_list[i + 1])[0][1]
            length1 = get_length(dx1, dy1)
            length2 = get_length(dx2, dy2)
            length = min(length1, length2)

            if radius + radius_prev > length:
                radius = length - radius_prev
                print(f'Радиус заменен на макимально возможный в {i + 1} точке - {radius}')

                if radius == 0:
                    new_target_list.append(target_list[i][0])

                else:
                    new_target_list.extend(
                        points_of_rounding(startAngle, sweepAngle, radius, circlePoint, target_list[i]))

            else:
                new_target_list.extend(points_of_rounding(startAngle, sweepAngle, radius, circlePoint, target_list[i]))

            radius_prev = radius

        else:
            new_target_list.append(target_list[i][0])
            radius_prev = 0
    return new_target_list
