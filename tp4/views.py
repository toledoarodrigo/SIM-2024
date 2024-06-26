import json
from django.shortcuts import render

from generator.exp import Exponencial
from generator.normal import Normal
from generator.uniforme import Uniforme
from generator.utils import history_callback
from tp4.simulator import InscriptionSimulation
from tp4.utils import MaintenanceTimeGenerator


def get_input_data(request):
    return render(request, 'tp4/index.html', {})


def simulate(request):
    data = request.POST

    inscription_lower_limit = data.get('inscription-lower-limit')
    inscription_upper_limit = data.get('inscription-upper-limit')

    arrivals_mean = data.get('arrivals-mean')

    maintenance_lower_limit = data.get('maintenance-lower-limit')
    maintenance_upper_limit = data.get('maintenance-upper-limit')

    return_mean = data.get('return-mean')
    return_deviation = data.get('return-deviation')

    inscription_time_generator = Uniforme(
        inscription_lower_limit, inscription_upper_limit)
    arrivals_generator = Exponencial(
        mean=arrivals_mean, frequency=""
    )
    maintenance_generator = Uniforme(
        maintenance_lower_limit, maintenance_upper_limit)
    return_generator = Normal(
        return_mean,
        return_deviation
    )

    time_target = int(data.get('time'))
    show_from = int(data.get('show-from'))
    show_count = int(data.get('show-count'))

    simulation = InscriptionSimulation(
        history_callback, inscription_time_generator, arrivals_generator,
        maintenance_generator, return_generator
    )
    history = simulation.run(time_target, show_from, show_count)

    return render(request, 'tp4/results.html', {
        'history': json.dumps(history)
    })


def get_tp5_input_data(request):
    return render(request, 'tp5/index.html', {})


def simulate_tp5(request):
    data = request.POST

    inscription_lower_limit = data.get('inscription-lower-limit')
    inscription_upper_limit = data.get('inscription-upper-limit')

    arrivals_mean = data.get('arrivals-mean')

    maintenance_step = data.get('maintenance-step')

    return_mean = data.get('return-mean')
    return_deviation = data.get('return-deviation')

    inscription_time_generator = Uniforme(
        inscription_lower_limit, inscription_upper_limit)
    arrivals_generator = Exponencial(
        mean=arrivals_mean, frequency=""
    )

    maintenance_generator = MaintenanceTimeGenerator(maintenance_step)

    return_generator = Normal(
        return_mean,
        return_deviation
    )

    time_target = int(data.get('time'))
    show_from = int(data.get('show-from'))
    show_count = int(data.get('show-count'))

    simulation = InscriptionSimulation(
        history_callback, inscription_time_generator, arrivals_generator,
        maintenance_generator, return_generator
    )
    history = simulation.run(time_target, show_from, show_count)

    return render(request, 'tp5/results.html', {
        'history': json.dumps(history),
        'euler_tables': maintenance_generator.euler_tables
    })
