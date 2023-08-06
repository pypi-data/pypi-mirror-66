from typing import List

from pyterum.socket_conn import SocketConn
from pyterum.kill_message import KillMessage
from pyterum import env
from pyterum.logger import logger

class FragmenterInput(SocketConn):

    def __init__(self, address:str=None):
        address = env.FRAGMENTER_INPUT if address == None else address
        super().__init__(address, retry_policy={"consume": 0})

        logger.info(f"Initializing FragmenterInput...")
        self.connect()
        self.produce = None
        self._consumer = super().consumer()

    # Yields None if the message is the kill message, indicating that there will be no more messages
    def consumer(self) -> List[str]:
        while True:
            output = next(self._consumer)
            try:
                KillMessage.from_json(output)
                output = None
            except (KeyError, TypeError):
                pass

            yield output


class FragmenterOutput(SocketConn):

    def __init__(self, address:str=None):
        address = env.FRAGMENTER_OUTPUT if address == None else address
        super().__init__(address, retry_policy={"produce": 0})

        logger.info(f"Initializing FragmenterOutput...")
        self.connect()
        self.consumer = None

    def produce(self, data:List[str]):
        super().produce(data)

    # To send that the fragmenter is done
    def produce_done(self):
        super().produce(KillMessage())