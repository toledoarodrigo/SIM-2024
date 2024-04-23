import base64
import io

from numpy import round


class Handler():
    @staticmethod
    def instantiate_distribution_generator(generator_class, *args, **kwargs):
        return generator_class(*args, **kwargs)

    def __init__(self, random_generator, size):
        # Needs as an argument the random generator for the
        # selected distribution type
        self.generator = random_generator
        self.size = size
        self._state = []

    def get_number(self):
        return round(self.generator.get_next_number(), decimals=4)

    def run(self):
        self._state = []
        self.max_value = None
        self.min_value = None
        for iteration in range(self.size):
            random = self.get_number()
            if self.max_value is None or random > self.max_value:
                self.max_value = random
            if self.min_value is None or random < self.min_value:
                self.min_value = random
            state_item = random
            self._state.append(state_item)
        return self._state


class FrequencyHandler():
    @property
    def labels(self):
        return self.sets_definition

    @property
    def frequencies(self):
        freqs = []
        for i in range(len(self.steps_frequency)):
            intervals = self.sets_definition[i]
            expected_freq = self.number_generator.get_expected_frequency(
                intervals, self.sample_size, intervals_amount=self.step_amount)
            item = (
                intervals,
                (
                   expected_freq,
                   self.steps_frequency[i]
                )
            )
            freqs.append(item)
        return freqs

    def __init__(
            self, step_amount, number_set, min_value, max_value,
            number_generator, sample_size):
        self.step_amount = step_amount
        self.steps_frequency = [0] * self.step_amount
        self.number_set = number_set
        self.min_value = min_value
        self.max_value = max_value
        self.number_generator = number_generator
        self.sample_size = sample_size

    @staticmethod
    def get_step_size(min, max, step_amount):
        return (max - min) / step_amount

    def build_sets(self):
        step_size = self.get_step_size(
            self.min_value, self.max_value, self.step_amount)
        lower_limit = self.min_value
        upper_limit = lower_limit + step_size
        self.sets_definition = []
        while upper_limit <= self.max_value:
            step = (lower_limit, upper_limit)
            self.sets_definition.append(step)
            lower_limit = upper_limit
            upper_limit = lower_limit + step_size

    def count_items(self):
        for number in self.number_set:
            for i in range(len(self.sets_definition)):
                (lower, upper) = self.sets_definition[i]
                if upper <= number:
                    continue
                # Is lower than the upper limit, count one for this set
                self.steps_frequency[i] += 1


class GraphHandler():
    def __init__(self, number_set, step_amount):
        self.number_set = number_set
        self.step_amount = step_amount

    def generate_historgram(self):
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        fig.set_figwidth(15)
        counts, bins, patches = plt.hist(self.number_set, self.step_amount)
        ax.set_xticks(bins, [f'{x:.4f}' for x in bins], rotation=60)
        plt.bar_label(patches)
        bytes_stream = io.BytesIO()
        plt.subplots_adjust(bottom=0.15)
        plt.savefig(bytes_stream, format='png')
        plt.close()
        return base64.b64encode(bytes_stream.getvalue()).decode()
