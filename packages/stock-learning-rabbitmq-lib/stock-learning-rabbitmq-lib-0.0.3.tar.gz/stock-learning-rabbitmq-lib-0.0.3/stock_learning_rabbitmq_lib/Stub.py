

class Stub:
    def __init__(self, server, queue):
        self._server = server
        self._queue = queue

    def _send(self, handler, content):
        self._server.send_message(self._queue, handler, content)