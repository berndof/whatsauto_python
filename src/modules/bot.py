import logging

class Chat(object): #TODO add more data
    def __init__(self, phone) -> None:
        logging.info(f"Chat {phone} created")
        self.phone = phone
        self.queue = None
        self.waitign_queue_response = False

    def __eq__(self, other):
        return self.phone == other.phone
        
class Queue(object):
    def __init__(self, name, first_message) -> None:
        logging.info(f"Queue {name} created")
        self.name = name
        self.first_message = first_message

class Bot(object):
    def __init__(self, manager, environment) -> None:
        self.manager = manager
        self.env = environment
        self.dev_phone = "554999564665"
        self.queues = self.__build_queues()
        self.chats = []
        
    def __build_queues(self):
        return [Queue("teste", "ola bem vindo a fila teste"), Queue("testando", "ola bem vindo a fila testando")]
        
    def get_greetings_message(self):
        
        message = f"ola, bem vindo a central de atendimento, selecione uma fila\n"
        for i, queue in enumerate(self.queues):
            message += f"{i+1} - {queue.name}\n" 
        return message
    
    async def on_message(self, message):
        await self.start_message_triage(message)
    
    async def start_message_triage(self, message):
        content = message["content"]
        sender = message["sender"];
        sender_phone = sender["id"].split("@")[0]
        print(sender_phone, content)
        
        if self.env == "dev" and sender_phone != self.dev_phone:
            logging.debug("ignoring message from other phone on dev environment")
            return 
        
        chat = next((chat for chat in self.chats if chat.phone == sender_phone), None)

        if chat is None:
            # Create a new chat object if it doesn't exist
            chat = Chat(sender_phone)
            self.chats.append(chat)
            
        logging.info(f"Processing message from {sender_phone}")


        
        """ if chat in self.chats:
            logging.info(f"Chat {sender_phone} already exists")
            chat = self.chats[self.chats.index(chat)]
        else:
            logging.info(f"Chat {sender_phone} added")
            self.chats.append(chat)
    
        if not chat.queue:
            if chat.waitign_queue_response:
                if content in ["1", "2"]: ## if message is a queue index
                    chat.waitign_queue_response = False
                    chat.queue = self.queues[int(content)-1]
                    self.manager.send_message(self.chat.queue.first_message, self.chat.phone)

                    
            await self.send_select_queue_message(chat)
        else:
            print("chat already have a queue") """
        

    
    async def send_select_queue_message(self, chat:Chat):
        logging.info(f"Sending select queue message to chat {chat.phone}")
        
        select_queue_message = self.get_greetings_message()
        self.chat.waitign_queue_response = True
        
        await self.manager.send_message(select_queue_message, chat.phone)