import logging, yaml, os
from automations.triggers.socket_trigger import SocketTrigger
from modules.models import Chat

#TODO Bot(Manager)
class Bot(object):    
    def __init__(self, manager):
        self.manager = manager
        self.is_started = False
        self.queues = {}
        
        
    async def __build_queues(self):
        queues = self.config["queues"]
        if not queues:
            #TODO default configuration
            raise ValueError("queues not found in config")
        
        for queue in queues:
            queue_name = queue["name"]
            greeting_message = queue["greetings_message"]

            self.manager.get_queue(queue_name)
        
    
    async def start(self):
        self.is_started = True
        logging.debug("bot started")
        
        #await self.__build_queues(self, )
        # do things that bot have to do 
        
        ## cria o trigger para esperar por novas mensagens
        trigger = SocketTrigger("listen_recieved_messages", "received-message", self.check_message)
        self.message_recieved_trigger = await self.manager.add_trigger(trigger)

        return
    
    async def check_message(self, event, data):
        #checa se ja existe um chat com quem enviou a mensagem 
        sender = data["response"]["sender"]
        sender_phone = sender["id"].split("@")[0] # remove @c.us from phone
        sender_name = sender["name"]
        
        chat = await self.manager.get_chat(sender_phone)
        if not chat:
            chat = Chat(phone=sender_phone,name=sender_name, is_contact=True, queue=None)
            
        await self.manager.db_client.add_chat(chat)
        
        if not chat.queue:
            
            #first attendance     
            await self.first_contact(chat)
            
        
    async def first_contact(self, chat):
        #send greetings message
        self.manager.send_message(chat.phone, chat.queue.greeting_message)
        
    async def stop(self):
        self.is_started = False