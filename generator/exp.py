from numpy import log
from numpy import exp

from generator.random import CustomRandom


class Exponencial():
    @property
    def mean(self):
        if self._mean is not None:
            return self._mean
        return 1/self.frequency

    @property
    def frequency(self):
        if self._frequency is not None:
            return self._frequency
        return 1/self.mean

    def __init__(self, mean=None, frequency=None):
        assert (mean is not None and frequency is None) \
            or (frequency is not None and mean is None)
        self._mean = int(mean) if mean is not None else None
        self._frequency = int(frequency) if frequency is not None else None
        self.random_generator = CustomRandom()

    def get_next_number(self):
        return self.generate_number()

    def generate_number(self):
        return (-1/self.frequency)*log(1-self.random_generator.random())

    def get_expected_frequency(self, interval, sample_size, **kwargs):
        interval_size = (interval[1] - interval[0])
        class_mark = (interval[0] + interval[1])/2
        lambda_value = 1 / self.mean
        return lambda_value * exp(
            -lambda_value*class_mark)*interval_size*sample_size
