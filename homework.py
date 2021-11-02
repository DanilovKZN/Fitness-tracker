"""Реализация фитнес трекера"""


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        message = (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.')
        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    M_IN_HOUR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных килокалорий."""
        raise NotImplementedError(
            'get_spent_calories определяется в наследниках.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())

        return info


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1 = 18
    COEFF_CALORIE_2 = 20

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = ((self.COEFF_CALORIE_1
                           * self.get_mean_speed()
                           - self.COEFF_CALORIE_2) * self.weight
                          / self.M_IN_KM * (self.duration
                                            * self.M_IN_HOUR))
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_1 = 0.035
    COEFF_CALORIE_2 = 0.029

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = ((self.COEFF_CALORIE_1 * self.weight
                           + (self.get_mean_speed() ** 2
                              // self.height)
                           * self.COEFF_CALORIE_2 * self.weight)
                          * (self.duration * self.M_IN_HOUR))
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    COEFF_CALORIE_1 = 1.1
    COEFF_CALORIE_2 = 2.0

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = (self.action * self.LEN_STEP) / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = ((self.get_mean_speed()
                           + self.COEFF_CALORIE_1)
                          * self.COEFF_CALORIE_2 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков,
       проверить корректность, создать обьекты."""
    possible_values = {'SWM': Swimming,
                       'RUN': Running,
                       'WLK': SportsWalking}
    if workout_type in possible_values:
        result_output = possible_values[workout_type](*data)
        return result_output


def main(training: Training) -> None:
    """Главная функция."""
    info_message = training.show_training_info()
    print(info_message.get_message())


def search_errors_in_values(name: str, list_with_var: list) -> bool:
    """Функция поиска некорректных значений"""
    NORMAL_WIDGHT_5_YERS_OLD_CHILDREN_KG = 14
    MAX_WIDGHT_PEOPLE_KG = 160
    MIN_HEIGHT_CM = 50
    MAX_HEIGHT_CM = 250
    result = True
    available_values = {'SWM': 5, 'RUN': 3, 'WLK': 4}
    # Если ключ или количесто элементов ключа не совпадают
    if (name not in available_values
            or available_values[name]
            != len(data)):
        result = False
    # Если имеется тип не int или float, а так же отрицательное значение
    for i in list_with_var:
        if not (isinstance(i, int) or isinstance(i, float)) or i < 0:
            result = False
    # Если имеется некорректная переменная по весу
    if (list_with_var[2] < NORMAL_WIDGHT_5_YERS_OLD_CHILDREN_KG
            or list_with_var[2] > MAX_WIDGHT_PEOPLE_KG):
        result = False
    # Если имеется некорректная переменная по росту
    if name == 'WLK' and (list_with_var[3] < MIN_HEIGHT_CM
                          or list_with_var[3] > MAX_HEIGHT_CM):
        result = False
    return result


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 5, 80, 25, 50]),
        ('RUN', [5000, 1, 70]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    available_values = {'SWM': 5, 'RUN': 3, 'WLK': 4}
    for workout_type, data in packages:
        if (search_errors_in_values(workout_type, data)):
            training = read_package(workout_type, data)
            main(training)
        else:
            print("Возникла ошибка, проверьте, пожалуйста,"
                  "корректность введенных данных и повторите попытку."
                  "В противном случае еще раз ознакомьтесь с руководством"
                  "пользователя.")
