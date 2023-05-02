from django.shortcuts import render
from django.http import Http404

from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView

from .models import Hub, Node, Data

from iot_sensor_nodes import cron


def index(request):
    latest_hub_list = Hub.objects
    context = {'latest_hub_list': latest_hub_list}
    return render(request, 'iot_sensor_nodes/index.html')

def hubs(request):
    latest_hub_list = Hub.objects.all()
    template = loader.get_template('iot_sensor_nodes/hubs.html')
    context = {'mymembers' : latest_hub_list,}
    return HttpResponse(template.render(context, request))

def nodes(request, hub_id):
    latest_node_list = Node.objects.filter(hub=hub_id)
    template = loader.get_template('iot_sensor_nodes/nodes.html')
    context = { 'mymembers' : latest_node_list,
                'hub_id' : hub_id,
                }
    return HttpResponse(template.render(context, request))

def data(request, hub_id, node_id):
    latest_data_list = Data.objects.filter(node=node_id).order_by('-pub_date')[:10]
    which_node = Node.objects.filter(id=node_id)
    which_hub = Node.objects.filter(id=hub_id)

    template = loader.get_template('iot_sensor_nodes/data.html')
    context = { 'mymembers' : latest_data_list,
                'node' : which_node,
                'hub' : which_hub,
                }
    return HttpResponse(template.render(context, request))

def graphs(request, hub_id):
    labels = []
    data = []


    latest_node_list = Node.objects.filter(hub=hub_id).order_by('address')
    node_0_data_list = latest_node_list.filter(address=0)
    node_1_data_list = latest_node_list.filter(address=1)
    node_2_data_list = latest_node_list.filter(address=2)
    node_3_data_list = latest_node_list.filter(address=3)
    node_4_data_list = latest_node_list.filter(address=4)
    node_5_data_list = latest_node_list.filter(address=5)
    node_6_data_list = latest_node_list.filter(address=6)
    node_7_data_list = latest_node_list.filter(address=7)
    template = loader.get_template('iot_sensor_nodes/graphs.html')
    context = { 'list0' : node_0_data_list,
                'list1' : node_1_data_list,
                'list2' : node_2_data_list,
                'list3' : node_3_data_list,
                'list4' : node_4_data_list,
                'list5' : node_5_data_list,
                'list6' : node_6_data_list,
                'list7' : node_7_data_list,
                }
    return HttpResponse(template.render(context, request))

def chart(request, hub_id, node_id):
    labels = []
    data = []
    humd = []
    latest_data_list = Data.objects.filter(node=node_id).order_by('-pub_date')[:10]
    which_node = Node.objects.get(id=node_id)
    which_hub = Hub.objects.get(id=hub_id)
    hub_name = which_hub.get_name
    hub_location = which_hub.get_location
    node_name = which_node.get_name
    node_address = which_node.get_address


    hub_dict = {'hub_id' : hub_id,
                'hub_name' : hub_name,
                'hub_location' : hub_location,
                }
    
    node_dict = {'node_id' : node_id,
                 'node_name' : node_name,
                 'node_address' : node_address,
                 }

    for dataPoint in latest_data_list:
        labels.append(dataPoint.pub_date.strftime("%Y-%m-%dT%H:%M:%SZ")) #(YYYY-MM-DDTHH:MM:SSZ)
        data.append(dataPoint.temperature)
        humd.append(dataPoint.humidity)

    template = loader.get_template('iot_sensor_nodes/graphs.html')
    context = { 'labels' : labels,
                'data' : data,
                'humidity' : humd,
                'node' : which_node.address,
                'hub' :  f'"{which_hub.name}"',
                }
    return HttpResponse(template.render(context, request))

        
    


