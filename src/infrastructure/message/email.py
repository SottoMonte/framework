import framework.port.message as port
import logging

class log(port.port):

    def __init__(self,**constants):
        self.config = constants['config'] 
        # create logger
        self.logger = logging.getLogger('simple_example')
        self.logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s | %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(ch)

    def loader(self,**constants):
        pass

    def post(self,**constants):
        self.logger.debug(constants['message'])
        #logger.info('info message')
        #logger.warning('warn message')
        #logger.error('error message')
        #logger.critical('critical message')

    async def speakA(self,**constants):
        self.logger.debug(constants['message'])
        #logger.info('info message')
        #logger.warning('warn message')
        #logger.error('error message')
        #logger.critical('critical message')

    async def hear(self,**constants):
        pass