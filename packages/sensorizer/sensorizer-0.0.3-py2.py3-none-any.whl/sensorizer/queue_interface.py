import dataclasses
import json
from typing import List
from azure.eventhub import EventData, EventHubClient
from fastavro import writer, parse_schema

from sensorizer.data_classes import TimeserieRecord


class QueueInterface:
    counter: int

    def send(self, events: List[TimeserieRecord]):
        pass

    def batch_send(self, events: List[TimeserieRecord]):
        pass


class QueueEventHub(QueueInterface):
    def __init__(self, address, user, key):
        self.address = address
        self.user = user
        self.key = key
        self.counter = 0
        self.client_batch = EventHubClient(
            self.address, debug=False, username=self.user, password=self.key
        )
        self.sender = self.client_batch.add_sender()
        self.client_batch.run()

    def batch_send(self, events: List[TimeserieRecord]):
        self.counter += len(events)
        data = EventData(batch=[json.dumps(dataclasses.asdict(e)) for e in events if e])
        self.sender.transfer(data)
        self.sender.wait()

    def send(self, events: List[TimeserieRecord]):
        return self.batch_send(events)


class QueueLocalAvro(QueueInterface):
    filepath: str = ""
    counter: int = 0

    def __init__(self, filepath: str):
        self.filepath = filepath

    def batch_send(self, events: List[TimeserieRecord]):
        self.send(events)

    def send(self, events: List[TimeserieRecord]):
        schema = {
            "doc": "A sensor document",
            "name": "Sensor",
            "namespace": "equinor",
            "type": "record",
            "fields": [
                {"name": "plant", "type": "string"},
                {"name": "tag", "type": "string"},
                {"name": "value", "type": "float"},
                {"name": "timestamp", "type": "float"},
            ],
        }
        parsed_schema = parse_schema(schema)
        self.counter += len(events)
        # Writing
        with open(f"{self.filepath}", "a+b") as out:
            writer(
                out,
                parsed_schema,
                [
                    {
                        "tag": e.tag,
                        "plant": e.plant,
                        "value": e.value,
                        "timestamp": e.ts,
                    }
                    for e in events
                    if e
                ],
                codec="deflate",
            )
