from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # ex: /polls/hubs/
    path('hubs/', views.hubs, name='hubs'),
    # ex: /polls/testing/
    #path('testing/', views.testing, name='testing'),
    # ex: /polls/hubs/1/
    path('hubs/<int:hub_id>/', views.nodes, name='nodes'),
    # ex: /polls/hubs/nodes/1
    path('hubs/<int:hub_id>/nodes/<int:node_id>/', views.data, name='data'),
    # ex: /polls/hubs/1/nodes/1/chart
    path('hubs/<int:hub_id>/nodes/<int:node_id>/chart', views.chart, name='chart'),
    # ex: /polls/hubs/1/graphs
    path('hubs/<int:hub_id>/graphs/', views.graphs, name='graphs'),
    

]