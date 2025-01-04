import aiohttp

class adapter:
    def __init__(self, **constants):
        self.config = constants['config']
        

    async def authenticate(self,**data):
        """Obtain the request token from github.
        Given the client id, client secret and request issued out by GitHub, this method
        should give back an access token
        Parameters
        ----------
        CLIENT_ID: str
            A string representing the client id issued out by github
        CLIENT_SECRET: str
            A string representing the client secret issued out by github
        request_token: str
            A string representing the request token issued out by github
        Throws
        ------
        ValueError:
            if CLIENT_ID or CLIENT_SECRET or request_token is empty or not a string
        Returns
        -------
        access_token: str
            A string representing the access token issued out by github
        """

        url = f'https://github.com/login/oauth/access_token?client_id={self.config["id"]}&client_secret={self.config["secret"]}&code={data["code"]}'
        headers = {
            'accept': 'application/json'
        }
        print(url)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers) as response:
                print(response.status,response.json())
                if response.status == 200:
                    data = await response.json()
                    return data['access_token']
                else:
                    return None