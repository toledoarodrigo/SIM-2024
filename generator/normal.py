from numpy import pi
from numpy import sqrt
from numpy import log
from numpy import cos
from numpy import sin
from numpy import exp

from generator.random import CustomRandom


class Normal():
    def __init__(self, mean, std):
        self.mean = float(mean)
        self.deviation = float(std)
        self.random_generator = CustomRandom()
        self.number_queue = []

    def get_next_number(self):
        if len(self.number_queue) == 0:
            self.number_queue = self.generate_number()
        return self.number_queue.pop()

    def generate_number(self):
        x1 = self.random_generator.random()
        x2 = self.random_generator.random()
        n1 = (sqrt(-2*log(x1))*cos(2*pi*x2))*self.deviation + self.mean
        n2 = (sqrt(-2*log(x1))*sin(2*pi*x2))*self.deviation + self.mean
        return [n2, n1]

    def get_expected_frequency(self, interval, sample_size, **kwargs):
        interval_size = (interval[1] - interval[0])
        class_mark = (interval[0] + interval[1])/2
        return (1/(self.deviation*sqrt(2*pi))*exp((-0.5)*((class_mark-self.mean)/self.deviation)**2))*interval_size*sample_size
