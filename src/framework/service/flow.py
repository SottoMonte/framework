import asyncio
from kink import inject,di
import sys

def asynchronous(**constants):
    inject = [] 
    if 'managers' in constants:
        for manager in  constants['managers']:
            inject.append(di[manager])
    
    def decorator(function):
        async def wrapper(*args, **kwargs):
            for key in constants.get('model',{}):
                print(kwargs)
                
                kwargs = await language.builder(key,kwargs,{},'filtered',language)
                print(kwargs)
            # Arguments
            test = list(args) + inject
            if 'inputs' in constants:
                output = await function(*test,**kwargs)
            else:
                output = await function(*test,**kwargs)
            if 'outputs' in constants:pass
            else: return output
        return wrapper
    return decorator

def synchronous(**constants):
    inject = []
    
    # Prepara i manager se specificati nei constants
    if 'managers' in constants:
        for manager in constants['managers']:
            if manager in di:
                inject.append(di[manager])

    def decorator(function):
        def wrapper(*args, **kwargs):
            try:
                # Combina gli argomenti passati alla funzione con gli oggetti iniettati
                test = list(args) + inject
                output = function(*test, **kwargs)
                return output
            except Exception as e:
                # Ottieni i dettagli dell'eccezione senza traceback
                exc_type, exc_value, exc_traceback = sys.exc_info()
                tb = exc_traceback
                while tb.tb_next:  # Naviga fino all'ultimo frame del traceback
                    tb = tb.tb_next
                filename = tb.tb_frame.f_code.co_filename
                module_name = tb.tb_frame.f_code.co_name
                line_number = tb.tb_lineno

                # Log dell'errore dettagliato
                print(f"Errore generico: {e}")
                print(f"File: {filename}")
                print(f"Modulo: {module_name}")
                print(f"Linea: {line_number}")
                # Rilancia l'eccezione per ulteriori gestioni, se necessario
                raise
        return wrapper
    return decorator