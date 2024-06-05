import logging, yaml, os
import models
from config import ENV, DEV_PHONE

#TODO Bot(Manager)
class Bot(object):    
    
    chats_choosing_queue = []
    
    def __init__(self, manager):
        self.manager = manager
    
    async def __createTestQueues(self):
        queues = {
            1: ("queue1", "Bem vindo ao queue 1"),
            2: ("queue2", "Bem vindo ao queue 2"),
            3: ("queue3", "Bem vindo ao queue 3")
        }
        
        for index, (name, greetings_message) in queues.items():
            await models.Queue.get_or_create(name=name, greetings_message=greetings_message, index=index)
            
        
    async def startListenMessages(self):
        await self.__createTestQueues()
        await self.manager.wpp_socket_client.add_trigger("received-message", self.onMessage)
    
    async def onMessage(self, event, data):
        #checa se ja existe um chat com quem enviou a mensagem 
        sender = data["response"]["sender"]        
        message = data["response"]["content"]
        
        sender_phone = sender["id"].split("@")[0] # remove @c.us from phone
        sender_name = sender["name"]
        
        if ENV == "dev" and int(sender_phone) != DEV_PHONE:
            logging.debug(f"ignoring message from {sender_phone} because it is not dev phone")
            return 

        chat, exists = await models.Chat.get_or_create(phone=sender_phone, name=sender_name)
        
        if not chat.queue and chat in self.chats_choosing_queue:
            print(message)
            
            queues = await models.Queue.all()
            
            for queue in queues:
                if message == str(queue.index) or message == queue.name:
                    chat.queue = queue
                    await self.manager.sendMessage(chat, queue.greetings_message)
                    self.chats_choosing_queue.remove(chat)
                    return
            
            await self.manager.sendMessage(chat, "Fila inválida, por favor digite o indice ou o nome da fila")
            await self.first_contact(chat)

        if not chat.queue and chat not in self.chats_choosing_queue:
            await self.first_contact(chat)
            
        if chat.queue and not chat.waitign_queue_response:
            print("cheguei aqui, refatore pra tras")
            pass
        

            
        
    
    async def first_contact(self, chat):
        
        async def __getFirstContactMessage(chat):
            message = "Bem vindo ao chat, selecione uma fila para iniciar o atendimento"
            queues = await models.Queue.all()
            print(queues)        
            
            for queue in queues:
                message += f"\n{queue.index} - {queue.name}"

            return message
        
        message = await __getFirstContactMessage(chat)
        await self.manager.sendMessage(chat, message)
        if chat not in self.chats_choosing_queue:
            self.chats_choosing_queue.append(chat)
    
    