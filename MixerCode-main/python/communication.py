import logging
from cmd import CMD
import threading
from pythonosc import dispatcher
from pythonosc import osc_server, udp_client, osc_message_builder
import asyncio

class Comms:
    def __init__(self):
        self.logger = logging.getLogger("logger.main")
        self.mainDispatcher = dispatcher.Dispatcher()
        self.server = osc_server.AsyncIOOSCUDPServer(("0.0.0.0", 8000), self.mainDispatcher, asyncio.get_event_loop())
        self.logger.info(f"Starting server on 0.0.0.0:8000")
        self.server.serve()
        self.logger.info(f"Started server, setting up client side")
        ip = input("Enter the IP: ")
        port = input("Enter the port")
        try:
            self.client = udp_client.SimpleUDPClient(ip, int(port))
        except TypeError:
            self.logger.critical("INVALID INPUT RECEIVED, QUITTING")
            quit("Ending")
    
    def registerListener(self, func_object, cmd:CMD):
        if cmd:
            self.logger.debug(f"Added listener to {cmd}")
            self.mainDispatcher.map(str(CMD), func_object)
        else:
            self.logger.error(f"The command {cmd} is not registered as an input")
            
    def sendMessage(self, cmd, value=None):
        if not cmd:
            self.client.send_message(cmd.value, value)
            