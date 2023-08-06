from QueueNameConstants import API_QUEUE_NAME
from Stub import Stub


class ScrapperStub(Stub):
    
    def __init__(self, server):
        super().__init__(server, API_QUEUE_NAME)

    def sync_infomoney_ibovespa(self, content):
        self._send('sync-infomoney-ibovespa', content)
