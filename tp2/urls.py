from django.urls import path

from tp2.views import get_create_series
from tp2.views import get_series_results

app_name = "tp2"

urlpatterns = [
    path('home/', get_create_series, name='generate_series'),
    path('resulst/', get_series_results, name='get_results')
]
