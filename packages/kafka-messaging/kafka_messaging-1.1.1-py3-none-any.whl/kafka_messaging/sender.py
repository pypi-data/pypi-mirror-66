"""A Sender is a configurable instance of a Confluent Kafka's
Producer's abstraction. Any data type that can be serialized by pickle
can be sent with a Sender """
import os
import pickle

from confluent_kafka import Producer

class Sender:
    """Sender capable of sending serialized messages of almost any kind
    through a Confluent Kafka Producer. Note that, due to inbuilt
    Kafka's limitations with message sizes, some messages may require
    customized configurations to be successfully sent.

    Methods
    -------
    send(topic: str, **message)
        Sends a message to topic.
    """

    def __init__(self, ip: str="localhost", port: int=9092, **configs):
        """
        ip : str, optional
            IP of the Kafka server where messages will be sent to
            (default is localhost)
        port : int, optional
            Port of the Kafka server where messages will be sent to
            (default is 9092)
        **config : dict, optional
            Additional configurations for the Kafka Producer
        """
        producer_config = {'bootstrap.servers': str(ip) + ':' + str(port)}
        for key in configs.keys():
            producer_config[key] = configs[key]
        self.producer = Producer(producer_config)

    def send(self, topic: str, **message):
        """Sends, to the specified topic, a message. If the message is
        empty, nothing will be sent.

        Parameters
        ----------
        topic : str
            Kafka topic to which the message will be sent
        message : dict, optional
            Message to be sent
        """
        self.producer.produce(topic, pickle.dumps(message))
        self.producer.flush()
