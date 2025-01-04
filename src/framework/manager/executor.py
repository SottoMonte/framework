'''Una classe chiamata Executor dovrebbe avere responsabilità ben definite, legate all'esecuzione di azioni, task, o comandi. Ecco cosa dovrebbe fare e gestire:
Responsabilità principali di una classe Executor

    Gestione dell'esecuzione di task:
        Accettare uno o più task (operazioni o funzioni) da eseguire.
        Fornire un'interfaccia chiara per invocare ed eseguire questi task.

    Concorrenza e threading:
        In contesti multi-thread, gestire l'esecuzione parallela o asincrona dei task.
        Fornire meccanismi per sincronizzare o coordinare i thread, se necessario.

    Gestione dello stato di esecuzione:
        Monitorare se i task sono in esecuzione, completati o falliti.
        Segnalare eventuali errori o eccezioni durante l'esecuzione.

    Priorità e scheduling (opzionale):
        Includere logiche per dare priorità ai task.
        Programmare l'esecuzione di task in base a condizioni o tempistiche specifiche.

    Astrazione dell'esecuzione:
        Nascondere la complessità del processo di esecuzione. Chi utilizza la classe dovrebbe solo passare i task senza preoccuparsi dei dettagli implementativi.

Metodi chiave che un Executor potrebbe avere:

    submit(task: Callable): Future
    Per accettare un task ed eseguirlo, restituendo un oggetto che rappresenta il risultato futuro (utile per task asincroni).

    execute(task: Callable): void
    Esegue immediatamente il task senza restituire alcun risultato.

    shutdown(): void
    Ferma l'esecuzione di ulteriori task e chiude le risorse associate.

    isRunning(): boolean
    Controlla se ci sono task in esecuzione.

    getResult(taskId: int): Object
    Restituisce il risultato di un task completato.

Casi d'uso comuni

    Esecuzione asincrona:
        Eseguire funzioni o task in background, restituendo risultati quando sono pronti.
        Esempio: gestire richieste di rete o calcoli lunghi senza bloccare l'interfaccia utente.

    Parallelizzazione:
        Suddividere un lavoro complesso in più parti e gestirne l'esecuzione su diversi thread o processi.

    Gestione comandi:
        Eseguire comandi o azioni definiti dall'utente o da altre parti del sistema.

    Workflow orchestrator:
        Coordinare l'esecuzione sequenziale o parallela di task, gestendo dipendenze e risultati.
'''

class executor():

    def __init__(self,**constants):
        self.sessions = dict()
        self.providers = constants['providers']

    async def act(self,**constants):
        action = constants.get('action','')
        module = await language.get_module(f'application/action/{action}.py',language)
        act = getattr(module,action)
        _ = await act(**constants)