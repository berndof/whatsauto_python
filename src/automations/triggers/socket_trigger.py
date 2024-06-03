import logging

class SocketTrigger(object):
    def __init__(self, name:str, event_to_catch:str, on_catch:callable) -> None:
        self.name = name
        self.event_to_catch = event_to_catch
        self.on_catch = on_catch
        
    def __str__(self) -> str:
        return self.name
    
    def set(self, event, data):
        logging.info(f"trigger {self.name} set")
        self.on_catch(event, data)
        return


#events 
# mensagem-enviada
# received-message