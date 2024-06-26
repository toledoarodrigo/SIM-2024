from generator.random import CustomRandom

from decimal import Decimal


class Euler():
    @staticmethod
    def generate_table(y, t, step, callback, stop_recursion_callback, items=[], **kwargs):
        y0 = kwargs['y0']
        dy = callback(t, y, y0=y0)
        hdy = (step * dy)
        next_y = step * dy + y
        should_stop = stop_recursion_callback(t, y)
        result_item = {"time": t, "y": y, 'dy': dy, 'hdy': hdy, 'y1': next_y}
        if should_stop:
            return items + [result_item]

        next_t = t + step
        return [result_item] + Euler.generate_table(
            next_y, next_t, step, callback, stop_recursion_callback, items, **kwargs)


def maintenance_dy(x, y, y0=0, **kwargs):
    return -68 - Decimal((y*y)/y0)


def stop_maintenance_recursion(x, y):
    return y <= 0


class MaintenanceTimeGenerator():
    def __init__(self, h, **kwargs):
        self.euler_tables = {
            '1000': Euler.generate_table(1000, 0, Decimal(h), maintenance_dy, stop_maintenance_recursion, y0=1000),
            '1500': Euler.generate_table(1500, 0, Decimal(h), maintenance_dy, stop_maintenance_recursion, y0=1500),
            '2000': Euler.generate_table(2000, 0, Decimal(h), maintenance_dy, stop_maintenance_recursion, y0=2000)
        }
        self.probabilities = [1/3, 2/3, 1]
        self.labels = list(self.euler_tables.keys())
        self.generator = CustomRandom()

    def get_number_from_random(self, random):
        for i in range(3):
            probability = self.probabilities[i]
            if random < probability:
                return self.labels[i]

    @staticmethod
    def get_from_table(table):
        return float(table[-1].get('time'))

    def get_next_event(self):
        random = self.generator.random()
        y0 = self.get_number_from_random(random)
        table = self.euler_tables[f'{y0}']
        generated_time = self.get_from_table(table)
        return {
            'random': random,
            'A0': y0,
            'generated_time': generated_time
        }
