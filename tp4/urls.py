from django.urls import path

from tp4 import views

app_name = "tp4"

urlpatterns = [
    path('', views.get_input_data, name='generate_series'),
    path('results/', views.simulate, name='simulate')
]
