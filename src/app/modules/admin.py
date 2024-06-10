from app.modules.security import Security
import models, logging
from config import BOT_PHONE

class Admin(object):

    async def create_superuser(username, password)    :
        password_hash = Security.hash_password(password)

        chat, exists = await models.Chat.get_or_create(phone=BOT_PHONE, name="MY_CHAT")

        user = await models.User.get_or_none(username=username)

        if not user:
            user = await models.User.create(username=username, password=password_hash, is_admin=True)
            logging.debug("creating superuser")


        user.chat = chat
        await user.save()

        queues = await models.Queue.all()
        print(f"queues:{queues}")

        for queue in queues:
            await queue.supervised_by.add(user)

        return user
