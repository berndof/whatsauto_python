import logging
import models
from config import ENV, DEV_PHONE, BOT_PHONE
from typing import Tuple

#TODO Bot(Manager)
class Bot(object):

    chats_choosing_queue = []

    def __init__(self, services):
        self.services = services
        self.queueController = QueueController(self)

    async def startListenMessages(self):
        await self.services.wppSocketClient.add_trigger("received-message", self.onMessage)

    async def onMessage(self, event, data):
        #checa se ja existe um chat com quem enviou a mensagem
        print("passei aqui")
        def extractResponseData(data) -> Tuple[Tuple, str]:
            sender = {"phone": data["response"]["sender"]["id"].split("@")[0],
                        "name": data["response"]["sender"]["name"]}
            message = data["response"]["content"]
            return sender, message

        sender, message = extractResponseData(data)

        if ENV == "dev" and int(sender["phone"]) != DEV_PHONE:
            logging.debug(f"ignoring message from {sender["phone"]} because it is not dev phone")
            return

        sender_chat, exists = await models.Chat.get_or_create(phone=sender["phone"], name=sender["name"])

        if sender_chat.queue:
            await self.queueController.notifyMembers(message, sender_chat)

        elif not await self.chatIsChoosingQueue(sender_chat):
            await self.makeContact(sender_chat)
        else:
            await self.chatIsAnsweringQueue(sender_chat, message)

    async def chatIsChoosingQueue(self, chat):
        if not chat.queue and chat not in self.chats_choosing_queue:
            return False
        elif chat in self.chats_choosing_queue:
            return True

    async def chatIsAnsweringQueue(self, chat, message):
        queues = await models.Queue.all()

        for queue in queues:
            if message == str(queue.index):

                chat.queue = queue
                await chat.save()
                await self.sendMessage (queue.greetings_message, chat=chat)
                self.chats_choosing_queue.remove(chat)

                return True

        await self.sendMessage("Fila inválida, por favor digite o índice da fila desejada", chat=chat)
        await self.makeContact(chat)

    async def makeContact(self, chat):

        async def __getFirstContactMessage(chat):
            message = "Bem vindo ao chat, selecione uma fila para iniciar o atendimento"
            queues = await models.Queue.all()
            print(queues)

            for queue in queues:
                message += f"\n{queue.index} - {queue.name}"

            return message

        message = await __getFirstContactMessage(chat)
        await self.sendMessage(message, chat=chat)
        if chat not in self.chats_choosing_queue:
            self.chats_choosing_queue.append(chat)

    async def sendMessage(self, message, chat=None, phone=None):
        endpoint = f"{self.services.wppSession.name}/send-message"
        if chat:
            phone = chat.phone

        if ENV == "dev" and phone != DEV_PHONE and phone != BOT_PHONE:
            logging.debug(f"ignoring message from {phone} because it is not dev phone")
            return

        body = {
            "phone": f"{phone}",
            "message": f"{message}"
        }

        headers = {
            'accept': '*/*',
            'Authorization': f'Bearer {self.services.wppSession.token}',
            'Content-Type': 'application/json'
        }

        return await self.services.wppApiClient.makeRequest("POST", endpoint, headers, body)

class QueueController(object):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def sendToAllMember(self, message):
        pass

    async def notifyMembers(self, message, sender_chat):
        chat = await models.Chat.get(phone=sender_chat.phone).prefetch_related("user" ,"queue", "queue__supervised_by")

        notification_message = f"Enviado por: {chat.name}\n{message}\n at:TODO Timestamp"

        print(chat.queue.name , "¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨")

        users_watching_queue = await chat.queue.supervised_by.all().prefetch_related("queuesUnderSupervision", "chat")
        logging.info(f"notifying {chat.queue.name} about {message}")
        for user in users_watching_queue:
            await self.bot.sendMessage(notification_message, chat=user.chat)

