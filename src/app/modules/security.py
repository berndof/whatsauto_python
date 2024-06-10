import bcrypt, logging
import models

class Security(object):

    def hash_password(password):
        logging.debug("hashing password")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def check_password(self, password, hashed_password):
        logging.debug("checking password")
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)  # pass the bytes object directly

    async def authenticate(self, username, password):
        user = await models.User.get_or_none(username=username)
        if not user:
            return None
        if not self.check_password(password, user.password):
            return None
        return user