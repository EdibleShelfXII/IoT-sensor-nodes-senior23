import requests
import pandas as pd
import json
from django.utils import dateparse

from django_extensions.management.jobs import QuarterHourlyJob

from polls.models import Hub, Node, Data

def update_db_from_api(): 
    hubs = Hub.objects.all()

    for hub_object in hubs:
        #hub_name = i.name
        #hub_object = Hub.objects.get(name=hub_name)
        api_url = f"http://{hub_object.address}:{hub_object.port}/data/all"

        try:
            response = requests.get(api_url, timeout=10)

            data = json.loads(response.text)

            df = pd.DataFrame.from_dict(data)

            print(df)

            nodes = Node.objects.filter(hub=hub_object)

            for node_object in nodes:
                adr = node_object.address
                try:
                    Data.objects.create(node=node_object, temperature=df.loc[adr, ['temperature']].item(), humidity=df.loc[adr, ['relative_humidity']].item(), pub_date=dateparse.parse_datetime(df.loc[adr, ['date_time']].item()))

                except Exception as e:
                    print('error inserting')


        except requests.exceptions.RequestException as e:
            print(f'Connection Error at url: {api_url}, associated with Hub: {hub_object.name}')

    pass