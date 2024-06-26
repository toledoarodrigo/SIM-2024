from django.urls import path

from tp4 import views

app_name = "tp4"

urlpatterns = [
    path('', views.get_input_data, name='generate_series'),
    path('results/', views.simulate, name='simulate'),
    path('euler/', views.get_tp5_input_data, name='generate_series_tp5'),
    path('euler_results/', views.simulate_tp5, name='simulate_tp5')
]
