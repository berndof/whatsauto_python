from config import SESSION_NAME, TOKEN_FILE_PATH, SECRET_KEY
import logging, os, aiofiles, asyncio

class WPPSession(object):
    def __init__(self) -> None:

        self.token = self.__load_token()
        self.status = self.__load_status()
        self.name = SESSION_NAME

        logging.debug(f"session {self.name} status: {self.status}, token: {self.token} created")

    def __load_token(self) -> str | None:
        if os.path.exists(TOKEN_FILE_PATH):
            with open(TOKEN_FILE_PATH, "r") as f:
                data = f.read()
                token, name = data.split(":")
                if name == SESSION_NAME:
                    return token
                else:
                    return None

    def __load_status(self) -> str:
        if self.token:
            return "CREATED"
        else:
            return "CLOSED"

    async def __store_token(self, token) -> None:
        async with aiofiles.open(TOKEN_FILE_PATH, "w") as f:
            await f.write(f"{token}:{self.name}")
            self.token = token
            return

    async def __get_token(self):
        endpoint = f"{self.name}/{SECRET_KEY}/generate-token"
        response = await self.wppApiClient.makeRequest("POST", endpoint)
        return response["token"]

    async def __get_status(self):
        endpoint = f"{self.name}/status-session"
        headers = {"Authorization": f"Bearer {self.token}"}
        return await self.wppApiClient.makeRequest("GET", endpoint, headers)

    async def start(self, services) -> None:
        self.wppApiClient = services.wppApiClient
        self.wppSocketClient = services.wppSocketClient

        if not self.token:
            token = await self.__get_token()
            await self.__store_token(token)

        endpoint = f"{self.name}/start-session"
        headers = {"Authorization": f"Bearer {self.token}"}
        response =  await self.wppApiClient.makeRequest("POST", endpoint, headers)

        logging.debug(f"session {self.name} status: {response['status']}")

        if response["status"] == "CONNECTED":
            self.status = "CONNECTED"
            return True

        self.status = "WAITING"
        return await self.__wait_qr_scan()

    async def __wait_qr_scan(self):
        while self.status == "WAITING":
            response = await self.__get_status()
            status = response["status"]
            if status == "QRCODE":
                qr_data = response["urlcode"] #TODO send qr_data for build qr code
                    #scan on wppconnect-server terminal session

                logging.debug(f"qr_data: {qr_data}")

                self.status = "WAITING_SCAN"
                break

            await asyncio.sleep(1) #wait 1 sec to check session status again

            #add trigger
            async def on_session_loged(event, data):
                self.status = "CONNECTED"
                return

            await self.wppSocketClient.add_trigger("session-logged", on_catch=on_session_loged)

            while self.session.status != "CONNECTED":
                logging.debug("waiting for session loged")
                ...

            return True







