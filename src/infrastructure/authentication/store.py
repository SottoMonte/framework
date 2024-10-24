import framework.service.flow as flow

class adapter:
    def __init__(self, **constants):
        self.config = constants['config']

    @flow.async_function(ports=('storekeeper',))
    async def authenticate(self,storekeeper,**data):
        try:
            transaction = await storekeeper.get(model='user',equal=data)

            if transaction['state']:
                return None
            else:
                return None
        except Exception as e:
            return None
        