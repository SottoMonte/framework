import application.model.identifier as identifier
import application.model.time as time
import application.model.user as user
import application.model.string as string
import application.model.natural as natural
import application.model.event as event
import application.model.boolean as boolean
import application.model.result as result

'''
ID della Transazione: Un identificatore unico per la transazione.
Timestamp: La data e l’ora in cui la transazione è stata avviata.
Utente: L’utente che ha avviato la transazione.
Tipo di Operazione: Il tipo di operazione eseguita (ad esempio, inserimento, aggiornamento, cancellazione).
Stato della Transazione: Lo stato corrente della transazione (ad esempio, in corso, completata, annullata).
Dettagli delle Operazioni: Le specifiche operazioni eseguite durante la transazione, come le query SQL.
Log delle Modifiche: Un registro delle modifiche apportate ai dati durante la transazione.
Durata: Il tempo totale impiegato per completare la transazione.'''

repository = (
    {'name':'id','type':dict(),'default':{},'iterable':True,},
    {'name':'name','type':dict(),'iterable':True,'default':{}},
    {'name':'description','type':dict(),'iterable':True,'default':{}},
    {'name':'owner','type':dict(),'iterable':True,'default':{}},
    {'name':'location','type':dict(),'iterable':True,'default':{}},
    {'name':'visibility','type':dict(),'iterable':True,'default':{}},
    {'name':'stars','type':dict(),'iterable':True,'default':{}},
)