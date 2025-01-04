import logging

class adapter():

    def __init__(self,**constants):
        self.config = constants['config'] 
        # create logger
        self.logger = logging.getLogger(self.config['project']['identifier'])
        self.logger.setLevel(logging.DEBUG)
        self.processable = ['log']
        
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(levelname)s:     %(message)s  <%(asctime)s|%(name)s>')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(ch)

    def loader(self, *services, **constants):
        pass

    async def can(self, *services, **constants):
        if constants['name'] in self.processable: return True
        else: return False

    async def post(self, *services, **constants):
        
        type_msg = constants['type'] if 'type' in constants else 'None'
        #message =  f"{constants['value']:{" "}{'<'}{100}}"
        message = constants['msg']

        match type_msg:
            case 'debug':
                self.logger.debug(message)
            case 'info':
                self.logger.info(message)
            case 'error':
                self.logger.error(message)
            case 'warning':
                self.logger.warning(message)
            case 'critical':
                self.logger.critical(message)
            case _:
                self.logger.info(message)

    async def read(self, *services, **constants):
        pass