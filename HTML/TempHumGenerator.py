import json
import random
import decimal

def main():

    def generateTemp():
        temp = float(decimal.Decimal(random.randrange(600,800))/10)
        #print(temp)
        return str(temp)

    def generateHumidity():
        humd = float(decimal.Decimal(random.randrange(000,1000))/10)
        #print(humd)
        return str(humd) 

    def generateNode():
        node = random.randrange(1,3)
        return str(node)

    sensorData = {"adr": generateNode(), "temp" : generateTemp(), "humd":generateHumidity()}

    JSON_STRING = json.dumps(sensorData, separators= (',',':'))

    return JSON_STRING

main()