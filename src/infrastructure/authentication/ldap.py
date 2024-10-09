from ldap3 import Server, Connection, ALL

class adapter:
    def __init__(self, ldap_server):
        self.server = Server(ldap_server, get_info=ALL)
        self.list = [] 

    def authenticate(self,**data):

        conn = Connection(self.server, user=data['user'], password=data['password'])
        if conn.bind():
            conn.unbind()
            return True
        else:
            return False