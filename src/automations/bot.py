from automations.triggers.socket_trigger import SocketTrigger
import logging

class Bot(object):
    def __init__(self, manager):
        self.manager = manager
        self.is_started = False
    
    async def start(self):
        self.is_started = True
        logging.debug("bot started")
        # do things that bot have to do 
        
        ## TODO 
        
        ## TODO implement queues
        ## cria o trigger para esperar por novas mensagens
        trigger = SocketTrigger("listen_recieved_messages", "received-message", self.check_message)
        self.listen_recieved_messages_trigger = await self.manager.add_trigger(trigger)
        
        return
    
    def check_message(self, event, data):
        print ("sync trigger triggered")
        print(event, data)
        return
        
    async def stop(self):
        self.is_started = False