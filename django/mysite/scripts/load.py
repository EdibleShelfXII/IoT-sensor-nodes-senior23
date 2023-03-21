import requests
import numpy as np
import pandas as pd
import json

from polls.models import Hub, Node, Data

hub_name = "test"

api_url = "http://localhost:23336/data/all"

response = requests.get(api_url)

data = json.loads(response.text)

df = pd.DataFrame.from_dict(data)

print(df)

Data.objects.create(node="test0", temperature = df.loc[0, ['temperature']].item(), humidity = df.loc[0, ['relative_humidity']].item())
