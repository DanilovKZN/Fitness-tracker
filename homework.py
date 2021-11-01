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
        distance = (self.action * self.LEN_STEP) / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = Training.get_distance(self) / self.duration

        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных килокалорий."""
        pass

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

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)
        self.coeff_calorie_1 = 18
        self.coeff_calorie_2 = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = ((self.coeff_calorie_1
                           * Training.get_mean_speed(self)
                           - self.coeff_calorie_2) * self.weight
                          / self.M_IN_KM * (self.duration
                                            * self.M_IN_HOUR))
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.coeff_calorie_1 = 0.035
        self.coeff_calorie_2 = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = ((self.coeff_calorie_1 * self.weight
                           + (Training.get_mean_speed(self) ** 2
                              // self.height)
                           * self.coeff_calorie_2 * self.weight)
                          * (self.duration * self.M_IN_HOUR))
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.coeff_calorie_1 = 1.1
        self.coeff_calorie_2 = 2.0

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
        spent_calories = ((Swimming.get_mean_speed(self)
                           + self.coeff_calorie_1)
                          * self.coeff_calorie_2 * self.weight)
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


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 50]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    available_values = {'SWM': 5, 'RUN': 3, 'WLK': 4}
    for workout_type, data in packages:
        if (workout_type in available_values
                and available_values[workout_type]
                == len(data)):
            training = read_package(workout_type, data)
            main(training)
