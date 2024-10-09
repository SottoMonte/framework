''' 
In ambito informatico, una classe chiamata “defender” potrebbe avere il compito di garantire la sicurezza e la protezione dei sistemi, delle reti e dei dati. Ecco alcune possibili responsabilità:

Sicurezza informatica: Un “defender” dovrebbe monitorare e prevenire attacchi informatici, come virus, malware, phishing e intrusioni. Questo potrebbe includere l’implementazione di firewall, antivirus, sistemi di rilevamento delle intrusioni e politiche di accesso.
Gestione delle vulnerabilità: Il “defender” dovrebbe identificare e risolvere le vulnerabilità nei sistemi e nelle applicazioni. Questo potrebbe comportare la gestione degli aggiornamenti, la scansione dei punti deboli e la correzione di falle di sicurezza.
Risposta agli incidenti: In caso di violazioni o attacchi, il “defender” dovrebbe reagire tempestivamente per mitigare i danni. Questo potrebbe includere l’analisi forense, la quarantena di sistemi compromessi e la ripristino dei servizi.
Politiche di sicurezza: Il “defender” potrebbe contribuire alla definizione e all’applicazione delle politiche di sicurezza dell’organizzazione, garantendo la conformità alle normative e alle procedure interne12.
'''

from abc import ABC, abstractmethod

class defender(ABC):

    def __init__(self,**constants):
        pass

    async def scan(self,**constants):
        pass

    async def authorization(self,**constants):
        pass