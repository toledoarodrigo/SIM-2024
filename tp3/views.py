import json
from copy import deepcopy

from django.shortcuts import render

from generator.random import CustomRandom


def get_input_data(request):
    return render(request, 'tp3/index.html', {})


class Distribution():
    def __init__(self, probabilities, labels, is_normalized=False):
        if is_normalized is False:
            probabilities = list(map(
                lambda item: int(item)/100, probabilities))
        if is_normalized:
            probabilities = list(map(
                lambda item: float(item), probabilities))
        aggregated_prob = 0
        self.probabilities = []
        for probability in probabilities:
            aggregated_prob += probability
            self.probabilities.append(aggregated_prob)
        self.labels = labels
        self.generator = CustomRandom()

    def get_number_from_random(self, random):
        for i in range(len(self.probabilities)):
            probability = self.probabilities[i]
            if random < probability:
                return self.labels[i]

    def get_number_and_random(self):
        random = self.generator.random()
        number = self.get_number_from_random(random)
        return number, random


class StateItem():
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class StockSimulation():
    def __init__(
        self, history_callback, stock_cost, request_cost, missing_cost,
        initial_stock, request_amount, request_breakpoint,
        clients_distribution, delay_distribution, useless_stock_distribution
    ):
        self.history_callback = history_callback
        self.stock_cost = stock_cost
        self.request_cost = request_cost
        self.missing_cost = missing_cost
        self.request_amount = request_amount
        self.request_breakpoint = request_breakpoint
        self.clients_distribution = clients_distribution
        self.delay_distribution = delay_distribution
        self.useless_stock_distribution = useless_stock_distribution
        self.history = []
        initial_state = StateItem(**{
            'week': 0,
            'random_clients': None,
            'clients': None,
            'random_delivery_delay': None,
            'delivery_delay': None,
            'next_delivery': None,
            'random_useless_stock': None,
            'useless_amount': None,
            'used_delivery_stock': None,
            'stock': initial_stock,
            'missing_items': 0,
            'requested_restock_count': 0,
            'stock_request_cost': 0,
            'maintenance_cost': 0,
            'missing_stock_cost': 0,
            'aggregated_stock_request_cost': 0,
            'aggregated_maintenance_cost': 0,
            'aggregated_missing_stock_cost': 0,
            'aggregated_total_costs': 0,
        })
        self._state = [initial_state]

    def update_state(self, next_state):
        self._state.pop()
        self._state.insert(0, next_state)

    def run(self, target_time, show_from, show_count):
        for i in range(target_time):
            prev_state = self._state[0]
            next_state = deepcopy(prev_state)

            next_state.week = i + 1
            clients, random_clients = \
                self.clients_distribution.get_number_and_random()
            next_state.random_clients = random_clients
            next_state.clients = clients

            if (next_state.week == prev_state.next_delivery):
                useless_items, useless_items_random = \
                    self.useless_stock_distribution.get_number_and_random()
                next_state.useless_amount = useless_items
                next_state.random_useless_stock = useless_items_random
                next_state.used_delivery_stock = \
                    self.request_amount - useless_items
                next_state.stock += next_state.used_delivery_stock
            elif (
                prev_state.next_delivery is not None and
                next_state.week > prev_state.next_delivery
            ):
                next_state.useless_amount = None
                next_state.random_useless_stock = None
                next_state.used_delivery_stock = None
                next_state.next_delivery = None
                next_state.delivery_delay = None

            if (next_state.stock < clients):
                next_state.missing_items = clients - next_state.stock
                next_state.stock = 0
            else:
                next_state.missing_items = 0
                next_state.stock = next_state.stock - clients

            next_state.stock_request_cost = 0
            if (
                next_state.stock <= self.request_breakpoint and
                next_state.next_delivery is None
            ):
                delivery_delay, delivery_delay_random = \
                    self.delay_distribution.get_number_and_random()
                next_state.delivery_delay_random = delivery_delay_random
                next_state.delivery_delay = delivery_delay
                next_state.next_delivery = next_state.week + delivery_delay
                next_state.requested_restock_count += 1
                next_state.stock_request_cost = self.request_cost

            next_state.maintenance_cost = next_state.stock * self.stock_cost
            next_state.missing_stock_cost = \
                next_state.missing_items * self.missing_cost

            next_state.aggregated_missing_stock_cost += \
                self.missing_cost * next_state.missing_items
            next_state.aggregated_maintenance_cost += \
                self.stock_cost * next_state.stock
            next_state.aggregated_stock_request_cost = \
                self.request_cost * next_state.requested_restock_count

            next_state.aggregated_total_costs = \
                next_state.aggregated_missing_stock_cost \
                + next_state.aggregated_maintenance_cost \
                + next_state.aggregated_stock_request_cost

            history_item = self.history_callback(
                next_state, show_from, show_count, target_time)
            if history_item is not None:
                self.history.append(history_item.__dict__)

            self.update_state(next_state)
        return self.history


def history_callback(current_state, show_from, show_count, target_time):
    show_limit = show_from + show_count
    if current_state.week >= show_from and current_state.week <= show_limit:
        return current_state
    if target_time == current_state.week:
        return current_state
    return None


def simulate(request):
    data = request.POST
    clients_arguments = data.getlist('clients-amounts')
    delay_time = data.getlist('delay')

    stock_cost = int(data.get('stock-cost'))
    request_cost = int(data.get('request-cost'))
    missing_cost = int(data.get('missing-cost'))

    initial_stock = int(data.get('initial-stock'))
    request_amount = int(data.get('request-amount'))
    request_breakpoint = int(data.get('request-breakpoint'))

    time_target = int(data.get('time'))
    show_from = int(data.get('show-from'))
    show_count = int(data.get('show-count'))
    clients_distribution = Distribution(
        clients_arguments,
        [0, 1, 2, 3])
    delay_distribution = Distribution(
        delay_time,
        [1, 2, 3],
        is_normalized=True)
    useless_stock_distribution = Distribution(
        ['0.6', '0.3', '0.1'],
        [0, 1, 2],
        is_normalized=True)

    simulation = StockSimulation(
        history_callback, stock_cost, request_cost, missing_cost,
        initial_stock, request_amount, request_breakpoint,
        clients_distribution, delay_distribution, useless_stock_distribution
    )
    history = simulation.run(time_target, show_from, show_count)

    return render(request, 'tp3/results.html', {
        'history': json.dumps(history)
    })
