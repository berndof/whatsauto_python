import logging


class Bot(object):
    def __init__(self, manager, environment) -> None:
        self.manager = manager
        self.env = environment
        self.dev_phone = "554999564665"
        
        self.queue = []
    
    def get_greetings_message(self):
        return "olá bem vindo a central de atendimento\n selecione uma das opções abaixo\n - 1 teste \n - 2 testando"
    
    async def on_message(self, message):
        await self.start_message_triage(message)
    
    async def start_message_triage(self, message):
        content = message["content"]
        sender = message["sender"];
        sender_phone = sender["id"].split("@")[0]
        print(sender_phone)
        
        if self.env == "dev" and sender_phone != self.dev_phone:
            logging.debug("ignoring message from other phone on dev environment")
            return 
        
        #checar se ja existe um atendimento em processo 
        existis_ticket = False #TODO
        
        #criar um objeto de chat com o sender
        #TODO 
        await self.manager.send_message(self.get_greetings_message(), sender_phone)
        
        
        pass