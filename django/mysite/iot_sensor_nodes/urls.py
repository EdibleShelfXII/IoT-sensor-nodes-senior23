from django.urls import path

from . import views

urlpatterns = [
    # ex: /iot_sensor_nodes/
    path('', views.index, name='index'),
    # ex: /iot_sensor_nodes/hubs/
    path('hubs/', views.hubs, name='hubs'),
    # ex: /iot_sensor_nodes/hubs/1/
    path('hubs/<int:hub_id>/', views.nodes, name='nodes'),
    # ex: /iot_sensor_nodes/hubs/nodes/1
    path('hubs/<int:hub_id>/nodes/<int:node_id>/', views.data, name='data'),
    # ex: /iot_sensor_nodes/hubs/1/nodes/1/chart
    path('hubs/<int:hub_id>/nodes/<int:node_id>/chart', views.chart, name='chart'),
    # ex: /iot_sensor_nodes/hubs/1/graphs
    path('hubs/<int:hub_id>/graphs/', views.graphs, name='graphs'),
    

]