import requests


class Influxdb:
    def __init__(self, influxurl):
        self.influxurl = influxurl

    def data_to_influx(self,data):
        requests.post(self.influxurl, data)
