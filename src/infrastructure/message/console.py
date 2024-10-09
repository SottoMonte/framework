#import application.port.message as port
#import logging

class adapter():

    def __init__(self,**constants):
        #self.config = constants['config'] 
        pass

    def loader(self,**constants):
        pass

    async def post(self,**constants):
        print(constants)

    async def hear(self,**constants):
        pass