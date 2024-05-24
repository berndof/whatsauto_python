from modules.api_client import ApiClient

class Manager():
    def __init__(self):
        self.API_URL = "http://10.4.0.5:21465/api"
        self.SECRET_KEY = "Sccint002"
        
        self.api_client = ApiClient(self.API_URL)

    async def create_session(self, session_name):
        #check if session already exists
        #TODO
        exist_session = False
        
        #do api call to create session
        if not exist_session:
            endpoint = f"{session_name}/{self.SECRET_KEY}/generate-token"
            response = await self.api_client.make_request("POST", endpoint)

            print(response)

            if response:
                token = response["token"]
                return token

        print(response)