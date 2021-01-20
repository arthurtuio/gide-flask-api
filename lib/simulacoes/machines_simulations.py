import numpy as np
import random
from datetime import datetime


def _waveform_value_generator():
    """
    Retorna um valor aletatorio de uma senoide
    """
    x = np.linspace(1, 10)  # Tamanho da lista = 50
    random_sinoid_list = np.sin(x) + np.random.normal(scale=0.1, size=len(x))

    random_index = random.randrange(len(random_sinoid_list))
    value = random_sinoid_list[random_index]

    return round(value, 2)


def motor_1():
    return {
        "current": _waveform_value_generator(),
        "voltage": round(_waveform_value_generator()*10, 2),
        "datetime": datetime.now(),
    }


def motor_2():
    return {
        "current": _waveform_value_generator(),
        "voltage": round(_waveform_value_generator()*10, 2),
        "datetime": datetime.now(),
    }


if __name__ == '__main__':
    print(motor_1())
