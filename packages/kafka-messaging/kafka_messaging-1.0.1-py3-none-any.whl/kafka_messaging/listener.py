"""A Listener is a configurable instance of a Confluent Kafka's
Consumer's abstraction. Any data type that can be deserialized by pickle
can be listened by with a Listener. """
import os
import pickle
from threading import Lock

from confluent_kafka import Consumer


class Listener:
    """Listener capable of receiving, through a Kafka Consumer, messages
    serialized using pickle.
    
    Received messages are stored locally when the listen() method is
    called, and their information is mantained until it is recovered by
    using the get_info() method.

    Note that any new message keys will be permanently added to a new
    dictionary field of this Listener until the clean() method is
    called, so be thoughtful of excessive memory usage.

    Methods
    -------
    subscribe(topic: str)
        Subscribes to topic(s)
    listen()
        Listen for new messages in a loop
    listen_cpp()
        Listen for new messages, sent from CPPKafka, in a loop.
    stop()
        Stops listen()'s loop
    has_info(key: str)
        Returns if Listener has information stored with specified key
    get_info(key: str)
        Returns and consumes information stored with specified key
    clean()
        Cleans the information keys
    get_active_topics(**configs) : Static
        Returns active topics of a Consumer with a customizable
        configuration
    """

    def __init__(self, topic: str=None, ip: str="localhost", port: int=9092, **configs):
        """
        topic : str or list, optional
            Topic(s) the consumer will be subscribed to. If none is set,
            doesn't initially subscribe to any topic.
        ip : str, optional
            IP of the Kafka server where messages will be sent to
            (default is localhost)
        port : int, optional
            Port of the Kafka server where messages will be sent to
            (default is 9092)
        **config : dict, optional
            Additional configurations for the Kafka Consumer
        """
        self.lock = Lock()
        self.stop_thread = False
        self.message = {}
        producer_config = {'bootstrap.servers': str(ip) + ':' + str(port), 'group.id': 'mygroup',
                           'auto.offset.reset': 'latest'}
        for key in configs.keys():
            producer_config[key] = configs[key]
        self.consumer = Consumer(producer_config)
        if topic:
            self.subscribe(topic)
    
    def subscribe(self, topic: str):
        """Subscribes listener to a topic. 
        
        Parameters
        ----------
        topic : str or list
            Kafka topic(s) from which the message will be listened from
        """
        if isinstance(topic, str):
            self.consumer.subscribe([topic])
        elif isinstance(topic, list):
            self.consumer.subscribe(topic)

    def listen_for_message(self):
        """Returns messages recieved by this Listener's Consumer """
        return self.consumer.poll(1.0)

    def listen(self):
        """Listens for information incoming from topic specified in
        initiation. """
        while not self.stop_thread:
            msg = self.listen_for_message()
            if msg is not None:
                self.deserialize(msg.value())

    def listen_cpp(self):
        """Listen for information coming from a Producer in C++.
        
        Expects messages to be not serialized by pickle, but be
        equivalently separated in Kafka's message keys. """
        while not self.stop_thread:
            msg = self.listen_for_message()
            if msg is not None:
                key = str(msg.key(), "utf-8").stip('\0')
                self.message[key] = msg.value()
    
    def stop(self):
        """ Stops listen()'s loop """
        self.stop_thread = True

    def deserialize(self, message):
        """Deserializes message """
        deserialized = pickle.loads(message)
        for key in deserialized.keys():
            self.message[key] = deserialized[key]
    
    def has_info(self, key: str):
        """Returns if this Listener has a message stored with the
        specified key. In case the key is not found or it's contents in
        the message dictionary is None, returns False. """
        return (key in self.message) and (self.message[key] is not None)

    def get_info(self, key: str):
        """Returns the message with the specified key stored in this
        Listener and sets it to None afterwards. """
        response = None
        self.lock.acquire()
        if self.has_info(key):
            response = self.message[key]
            self.message[key] = None
        self.lock.release()
        return response

    def clean(self):
        """Cleans the message variable of all it's keys and values,
        setting it to an empty dictionary """
        self.lock.acquire()
        self.message = {}
        self.lock.release()

    @staticmethod
    def get_active_topics(**configs):
        """ Returns all active topics from a Kafka Consumer
        
        Parameters
        ----------
        **config : dict, optional
            Additional configurations for the Kafka Consumer
        """
        producer_config = {'bootstrap.servers': 'localhost:9092', 'group.id': 'mygroup',
                           'auto.offset.reset': 'latest'}
        for key in configs.keys():
            producer_config[key] = configs[key]
        consumer = Consumer(producer_config)
        return consumer.list_topics().topics.keys()
