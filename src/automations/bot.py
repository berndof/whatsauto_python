

class Bot(object):
    def __init__(self, manager):
        self.manager = manager
        self.is_started = False
    
    async def start(self):
        self.is_started = True
        # do things that bot have to do 
        
        ## TODO 
        
        ## TODO implement queues
        
        
        return
    
    async def stop(self):
        self.is_started = False