__author__ = 'agrigoryev'
import queue
import threading

class Layer:
    def __init__(self, name="Unnamed",  underlying_layer=None):
        """Override the on_upstream_message(self, message)"""
        assert isinstance(underlying_layer, Layer) or underlying_layer is None
        self.underlying_layer = underlying_layer

        self.name = name
        self.stack = None
        self.upstream_queue = queue.Queue()
        self.downstream_queue = queue.Queue()
        # start
        WaitingProcess(self.downstream_queue, self.on_downstream_message).start()
        if underlying_layer is not None:
            WaitingProcess(self.underlying_layer.upstream_queue, self.on_upstream_message).start()
        # starting thread
        threading.Thread(target=self.run).start()

    def set_stack(self, stack):
        """setting stack"""
        self.stack = stack

    def on_upstream_message(self, message):
        """Override me. Provides dummy functionality on default."""
        self.to_lower(message)

    def on_downstream_message(self, message):
        """Override me. Provides dummy functionality on default."""
        self.to_upper(message)

    def to_upper(self, message):
        """Override me. Provides dummy functionality on default."""
        self.upstream_queue.put(message)

    def to_lower(self, message):
        """Override me. Provides dummy functionality on default."""
        self.underlying_layer.downstream_queue.put(message)

    def run(self):
        """Override me. Provides dummy functionality on default."""
        pass


class WaitingProcess(threading.Thread):
    """Creates thread that waits message from the queue and then running the defined function"""
    def __init__(self, queue_to_wait, callback_func):
        threading.Thread.__init__(self)
        self.func = callback_func
        self.queue = queue_to_wait
        self.daemon = True


    def run(self):
        """Infinitely waiting for message from the queue.
           If queue is deleted, stops waiting and finishes thread."""
        while True:
            try:
                message = self.queue.get()
                self.func(message)
            except queue.Empty:
                # nothing in the queue. Do nothing
                pass
            except AttributeError:
                # Queue does not exist
                # Stop waiting
                return