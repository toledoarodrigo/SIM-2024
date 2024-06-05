from generator.random import CustomRandom


class Uniforme():
    def __init__(self, a, b, **kwargs):
        self.lower_limit = float(a)
        self.upper_limit = float(b)
        self.random_generator = CustomRandom()

    def get_next_number(self):
        return self.generate_number()

    def get_next_event(self):
        random = self.random_generator.random()
        generated_time = self.generate_number(random)
        return {
            'random': random,
            'generated_time': generated_time
        }

    def generate_number(self, random=None):
        # Returns the next number generated
        # Do not use 1 when getting the RND
        if random is None:
            random = self.random_generator.random()
        return self.lower_limit + random * \
            (self.upper_limit - self.lower_limit)

    def get_expected_frequency(self, interval, sample_size, **kwargs):
        intervals_amount = kwargs['intervals_amount']
        return sample_size / intervals_amount
