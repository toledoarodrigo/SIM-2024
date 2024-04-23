from django.shortcuts import render

from generator.uniforme import Uniforme
from generator.exp import Exponencial
from generator.normal import Normal

from tp2.handler import Handler
from tp2.handler import GraphHandler
from tp2.handler import FrequencyHandler


def get_create_series(request):
    return render(request, 'tp2/index.html', {})


UNIFORM = 'uniform'
NORMAL = 'normal'
EXPONENTIAL = 'exponential'

DISTRIBUTION_MAPPING = {
    UNIFORM: Uniforme,
    NORMAL: Normal,
    EXPONENTIAL: Exponencial,
}


def get_series_results(request):
    data = request.POST
    distribution_generator_class = DISTRIBUTION_MAPPING[
        data.get("distribution")]
    distribution_arguments = [*data.getlist(f"{data.get('distribution')}_args")]
    distribution_generator = Handler.instantiate_distribution_generator(
        distribution_generator_class, *distribution_arguments)
    handler = Handler(
        distribution_generator,
        int(data['sample_size']),
    )
    handler.run()

    number_set = handler._state

    freq_handler = FrequencyHandler(
        int(data['intervals_amount']), number_set,
        handler.min_value, handler.max_value, distribution_generator,
        int(data['sample_size']))
    freq_handler.build_sets()
    freq_handler.count_items()

    graph_handler = GraphHandler(number_set, int(data['intervals_amount']))
    graph = graph_handler.generate_historgram()

    import json
    return render(request, 'tp2/results.html', {
        'history': handler._state,
        'history_str': json.dumps(handler._state),
        'labels': freq_handler.labels,
        'frequencies': freq_handler.frequencies,
        'graph': graph
    })
