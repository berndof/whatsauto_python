import logging
import inspect

class SocketTrigger(object):
    def __init__(self, name:str, event_to_catch:str, on_catch:callable) -> None:
        self.name = name
        self.event_to_catch = event_to_catch
        self.on_catch = on_catch
        
    def __repr__(self) -> str:
        return f"{self.name} waiting for {self.event_to_catch} event"
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __dict__(self):
        return {"name": self.name, "event_to_catch": self.event_to_catch, "on_catch": self.on_catch} 
        
    async def set(self, event, data): 
        if inspect.iscoroutinefunction(self.on_catch):
            await self.async_set(event, data)
        else:
            self.sync_set(event, data)
        return 
    
    async def async_set(self, event, data):
        logging.info(f"trigger {self.name} set | async")
        await self.on_catch(event, data)
        return
    
    def sync_set(self, event, data):
        logging.info(f"trigger {self.name} set | sync")
        self.on_catch(event, data)
        return 


#events 
# mensagem-enviada
# received-message
