# Policy: fast|slow|dynamic 'web o nativo' - local|
from kink import di


''' 
In ambito informatico, una classe chiamata “presenter” può avere diverse funzioni a seconda del contesto in cui viene utilizzata. Ecco alcune possibilità:

Presenter in architettura MVC (Model-View-Controller): In un’applicazione basata su architettura MVC, il “presenter” è responsabile di gestire la logica di presentazione tra il modello (dati) e la vista (interfaccia utente). Si occupa di formattare i dati per la visualizzazione, gestire gli eventi dell’interfaccia e coordinare le interazioni tra modello e vista.
Presenter in framework di sviluppo web: Nei framework web come Angular, React o Vue.js, il “presenter” (o “container component”) è una componente che gestisce lo stato e la logica di presentazione per una parte specifica dell’interfaccia utente. Ad esempio, un “presenter” potrebbe gestire la logica di autenticazione, la gestione di form o la comunicazione con i servizi backend.
Presenter nelle presentazioni multimediali: In applicazioni o librerie per la creazione di presentazioni (come PowerPoint o Keynote), un “presenter” potrebbe gestire la sequenza degli elementi, gli effetti di transizione e l’interazione con l’utente durante la presentazione.
Presenter in strumenti di visualizzazione dei dati: In applicazioni che visualizzano dati complessi (come grafici, tabelle o dashboard), un “presenter” potrebbe organizzare e presentare i dati in modo chiaro e significativo per l’utente.
'''

class presenter():
    ports = ['presentation']

    def __call__(self,**constants):
        if 'adapter' in constants:
            return di['presentation'][0].tree_view[constants['id']]
           # return await self.services[0].read(file=constants['url'])
        pass

    async def builder(self,**constants):
        if 'module' in constants:
            return await di['persistence'].read(file=constants['module'])
        pass

    async def description(self,**constants):
        if 'module' in constants:
            return await di['persistence'].read(file=constants['module'])
        pass

    async def benchmark(self,**constants):
        if 'module' in constants:
            return await di['persistence'].read(file=constants['module'])
        pass

    async def effort(self,**constants):
        if 'module' in constants:
            return await di['persistence'].read(file=constants['module'])
        pass