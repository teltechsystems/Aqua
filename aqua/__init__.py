from encoders import GeneralEncoder
from services import Service, DbService

import json

# Asynchronous Queries Uniformly Aggregated
class Aqua(object):
    def __init__(self, producer_socket, result_socket):
        self.producer_socket = producer_socket
        self.result_socket = result_socket

    def create_wave(self, services, search_params):
        pending_services = [x for x in services]

        for service in services:
            self.producer_socket.send(service + ' ' + json.dumps(search_params))

        search_results = {}

        while len(pending_services) > 0:
            service, results = self.get_result_message()

            search_results[service] = results

            pending_services.pop(pending_services.index(service))

        return search_results

    def dumps(self, obj):
        return json.dumps(obj, cls=GeneralEncoder)

    def get_producer_message(self):
        return self.get_socket_message(self.producer_socket)

    def get_result_message(self):
        return self.get_socket_message(self.result_socket)

    def get_socket_message(self, socket):
        topic, message = socket.recv().split(' ', 1)

        return topic, json.loads(message)

    def ride_wave(self):
        raise NotImplemented("...")

    def ride_waves(self):
        while True:
            self.ride_wave(*self.get_producer_message())