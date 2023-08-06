""" A ListenerPool simplifies the synchronization of multiple Listener
instances and doubles as an interface to execute custom methods
everytime the Listeners are synchronized. """
import os
import re
import sys
import time
from threading import Thread

from .listener import Listener


def listener_cpp_thread(listener: Listener):
    """Calls the listening loop of the received Listener. Expects to be
    receiving messages from a C++ Producer """
    listener.listen_cpp()

def listener_thread(listener: Listener):
    """Calls the listening loop of the received Listener. """
    listener.listen()


class ListenerPool:
    """Manages multiple Listeners in different threads, handling their
    sincronization and allowing new methods to be bound.

    Bound methods will be executed when the threads are synchronized.

    Syncronization conditions can also be customized.

    Methods
    -------
    bind(method)
        Binds a method to be executed after syncronization
    set_sync_condition(method)
        Sets sync condition as specified method
    is_synced()
        Returns True if the sync condition is met and False otherwise
    start()
        Starts the verification of synchronization of Listeners and
        execution of bound methods
    get_syncer_thread()
        Returns the thread that verifies the synchronization of
        Listeners
    get_topic_names(regex : str) -> list : Static
        Returns all active topics' names that correspond to regex
    """

    def __init__(self, topic_regex: str, cpp: bool=False):
        """
        topic_regex : str
            Regex string. All topics that satisfy this regex will be
            listened to.
        cpp : bool, optional
            If True, expects listeners to be receiving messages from
            a C++ source code. Else, expects regular python messages.
        """
        self.listener_threads = []
        self.listeners = {}
        topic_names = self.get_topic_names(topic_regex)
        thread_func = listener_thread
        if cpp:
            thread_func = listener_cpp_thread
        for topic in topic_names:
            self.listeners[topic] = Listener(topic=topic)
            t = Thread(target=thread_func, args=[self.listeners[topic]], daemon=True)
            self.listener_threads.append(t)
        self.bound_methods = []
        self.sync_condition = self._base_sync_condition
        self.syncer_thread = Thread(target=self._sync_and_execute, daemon=True)

    def _base_sync_condition(self, listeners: dict):
        """Fallback synchronization method """
        return True

    def _sync_and_execute(self):
        """Waits for Listeners to be synced according to synchronization
        condition set with set_sync_condition().
        
        Loops until there are no more bound methods.
        """
        total_time = 0.0
        time_decay_rate = 0.9
        start_time = time.time()
        while len(self.bound_methods) > 0:
            if self.is_synced():
                time_interval = time.time() - start_time
                start_time = time.time()
                total_time = time_decay_rate * total_time\
                             + (1.0 - time_decay_rate) * time_interval
                fps = 1.0/total_time
                for method in self.bound_methods:
                    if method(self.listeners, fps=fps):
                        self.bound_methods.remove(method)

    def bind(self, method):
        """Binds method to be executed after synchronization in the main
        loop. Bound methods must be able to receive the 'fps' argument.
        
        Parameters
        ----------
        method : function
            Method to be bound. Bound methods always receive as
            arguments all listeners. When bound method returns True, it
            is removed from the bound methods list. 
        """
        self.bound_methods.append(method)

    def set_sync_condition(self, sync_method):
        """Sets sync condition as the specified method

        Parameters
        ----------
        sync_method : function
            Function that receives all Listeners as argument and must
            return a boolean value indicating if the Listeners are
            synced.
        """
        self.sync_condition = sync_method
    
    def is_synced(self) -> bool:
        """Returns if the synchronization condition is fulfilled or not,
        given the state of all Listener instances.
        """
        return self.sync_condition(self.listeners)

    def start(self):
        """ Starts the listen() loop in all Listener instances and
        starts the syncer_thread that waits for Listeners to be
        synchronized and executes all bound methods in an ongoing loop
        until there are no more bound methods.

        Raises
        ------
        Exception
            If there are no bound methods when this method is called.
        """
        if len(self.bound_methods) == 0:
            raise Exception("ListenerPool can't be started with no bound methods")
        else:
            for thread in self.listener_threads:
                thread.start()
            self.syncer_thread.start()

    def get_syncer_thread(self) -> Thread:
        """ Returns the thread that runs the loop that waits for
        synchronization and then executes all bound methods.

        Returns
        -------
        syncer_thread : Thread
        """
        return self.syncer_thread

    @staticmethod
    def get_topic_names(regex: str) -> list:
        """Returns all Kafka topics that correspond to received regex
        
        Returns
        -------
        topics : List[str]
            A list of strings of topic names that satify the regex
        """
        topic_names = Listener.get_active_topics()
        return [topic for topic in topic_names if re.search(regex, topic)]
