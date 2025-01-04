''' 
In ambito informatico, una classe chiamata “defender” potrebbe avere il compito di garantire la sicurezza e la protezione dei sistemi, delle reti e dei dati. Ecco alcune possibili responsabilità:

Sicurezza informatica: Un “defender” dovrebbe monitorare e prevenire attacchi informatici, come virus, malware, phishing e intrusioni. Questo potrebbe includere l’implementazione di firewall, antivirus, sistemi di rilevamento delle intrusioni e politiche di accesso.
Gestione delle vulnerabilità: Il “defender” dovrebbe identificare e risolvere le vulnerabilità nei sistemi e nelle applicazioni. Questo potrebbe comportare la gestione degli aggiornamenti, la scansione dei punti deboli e la correzione di falle di sicurezza.
Risposta agli incidenti: In caso di violazioni o attacchi, il “defender” dovrebbe reagire tempestivamente per mitigare i danni. Questo potrebbe includere l’analisi forense, la quarantena di sistemi compromessi e la ripristino dei servizi.
Politiche di sicurezza: Il “defender” potrebbe contribuire alla definizione e all’applicazione delle politiche di sicurezza dell’organizzazione, garantendo la conformità alle normative e alle procedure interne12.
'''

#Authentication | Authorization | Accounting

from secrets import token_urlsafe

class defender():

    def __init__(self,**constants):
        self.sessions = dict()
        self.providers = constants['providers']

    async def authenticate(self,**constants):
        for backend in self.providers:
            token = await backend.authenticate(**constants)
            print('token',token)
            if token != None:
                self.sessions[constants['identifier']] = {'token':token,'ip':constants.get('ip','')}
                return token
        '''if constants['username'] in self.users and constants['password'] == self.users[constants['username']]:
            token = token_urlsafe(16)
            self.sessions[constants['identifier']] = token
            return token
        else:
            return '#' '''

    async def authenticated(self,**constants):
        #print(self.sessions,constants['session'])
        if constants['session'] in self.sessions:
            return True
        else:
            return False

    async def authorize(self,**constants):
        for key in self.sessions:
            session = self.sessions[key]
            if session.get('ip') == constants.get('ip',''):
                return True
        return False

    async def whoami(self,**constants):
        for key in self.sessions:
            session = self.sessions[key]
            if session.get('ip') == constants.get('ip',''):
                return key
        return None

    async def detection(self,**constants):
        return True
    
    async def protection(self,**constants):
        return True