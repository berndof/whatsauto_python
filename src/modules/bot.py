import logging, yaml, os
from modules.models import Chat

#TODO Bot(Manager)
class Bot(object):    
    def __init__(self, manager):
        self.manager = manager
        self.is_started = False        
        
    async def start(self):
        self.is_started = True
        logging.debug("started Bot")
        # do things that bot have to do 
        
        ## cria o trigger para esperar por novas mensagens
        self.manager.wpp_socket_client.add_trigger("recieved_message", self.check_message)
        return
    
    async def check_message(self, event, data):
        #checa se ja existe um chat com quem enviou a mensagem 
        sender = data["response"]["sender"]
        sender_phone = sender["id"].split("@")[0] # remove @c.us from phone
        sender_name = sender["name"]
        
        chat = await self.manager.db(sender_phone)
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