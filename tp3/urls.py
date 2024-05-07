from django.urls import path

from tp3.views import get_input_data
from tp3.views import simulate

app_name = "tp3"

urlpatterns = [
    path('', get_input_data, name='generate_series'),
    path('results/', simulate, name='simulate')
]
