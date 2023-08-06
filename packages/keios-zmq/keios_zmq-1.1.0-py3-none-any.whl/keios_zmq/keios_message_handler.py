from typing import Callable, List

from keios_zmq.keios_message import KeiosMessage
from keios_zmq.log_provider import LogProvider
from abc import ABC, abstractmethod

class KeiosMessageHandler(ABC):
    log = LogProvider.get_logger(__name__)

    @abstractmethod
    def handle(self, messages: List[KeiosMessage]):
        pass

    def execute(self, messages: List[KeiosMessage]):
        if(self.isHealthCheckMessage(messages[0])):
            return self.buildHealthCheckResponse(messages[0])
        else:
            return self.handle(messages)

    def isHealthCheckMessage(self, message: KeiosMessage):
        if message.header.get("type")=="HCheck":
            return True
        else:
            return False

    def buildHealthCheckResponse(self, message: KeiosMessage) -> List[KeiosMessage]:
        return [KeiosMessage({'type': 'HCheck'}, bytes("pong", encoding="utf-8"))]
