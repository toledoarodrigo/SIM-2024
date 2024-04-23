from generator.random import CustomRandom


class Uniforme():
    def __init__(self, a, b, **kwargs):
        self.lower_limit = int(a)
        self.upper_limit = int(b)
        self.random_generator = CustomRandom()

    def get_next_number(self):
        return self.generate_number()

    def generate_number(self):
        # Returns the next number generated
        # Do not use 1 when getting the RND
        return self.lower_limit + self.random_generator.random() * \
            (self.upper_limit - self.lower_limit)

    def get_expected_frequency(self, interval, sample_size, **kwargs):
        intervals_amount = kwargs['intervals_amount']
        return sample_size / intervals_amount
