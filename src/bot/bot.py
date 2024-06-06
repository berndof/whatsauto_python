import logging, yaml, os
import models
from config import ENV, DEV_PHONE
from typing import Tuple

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
        await self.manager.wppSocketClient.add_trigger("received-message", self.onMessage)

    async def onMessage(self, event, data):
        #checa se ja existe um chat com quem enviou a mensagem
        print("passei aqui")
        async def extractResponseData(data) -> Tuple[Tuple, str]:
            sender = {"phone": data["response"]["sender"]["id"].split("@")[0],
                        "name": data["response"]["sender"]["name"]}
            message = data["response"]["content"]
            return sender, message

        sender, message = await extractResponseData(data)

        if ENV == "dev" and int(sender["phone"]) != DEV_PHONE:
            logging.debug(f"ignoring message from {sender["phone"]} because it is not dev phone")
            return

        chat, exists = await models.Chat.get_or_create(phone=sender["phone"], name=sender["phone"])

        #return await self.check_chat(message, chat)

        if not chat.queue and chat not in self.chats_choosing_queue:
            await self.first_contact(chat)

        if chat.queue and not chat.waitign_queue_response:
            print("cheguei aqui, refatore pra tras")
            pass

    async def ifChatIsChoosingQueue(self, message, chat):

        if not chat.queue and chat in self.chats_choosing_queue:
            queues = await models.Queue.all()

            for queue in queues:
                if message == str(queue.index) or message == queue.name:
                    chat.queue = queue
                    await self.manager.sendMessage(chat, queue.greetings_message)
                    self.chats_choosing_queue.remove(chat)
                    return

            await self.manager.sendMessage(chat, "Fila inválida, por favor digite o indice ou o nome da fila")
            await self.first_contact(chat)





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

