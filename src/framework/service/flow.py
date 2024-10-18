import asyncio
from kink import inject,di

'''def CALL_WHEN(FN,TIME:str,*arg,**kwargs):
    def zzz(fn,constants):
        asyncio.get_event_loop().create_task(fn(*arg,**constants))
    timestamp = datetime.datetime.now()
    print(timestamp.time().hour,timestamp.time().minute)
    if (TIME != "") | (TIME == "NOW"):
            
        if TIME == "NOW": tt = timestamp.time()
        else: tt = datetime.datetime.strptime(TIME, '%H:%M')
            
        total = 0
        h =  tt.hour - timestamp.time().hour 
        m = tt.minute - timestamp.time().minute
        print(h,m)
        if h >= 0:
            total += h *3600    
            if m >= 0:
                total += m *60
                print(total)
                current_time = asyncio.get_event_loop().time() + total
                asyncio.get_event_loop().call_at(current_time,zzz,FN,kwargs)
            else:
                print("---------------------- SCADUTO!")
        else:
            print("----------------------  SCADUTO!")
    else:
        print("----------------------  SCADUTO!")'''


#asynchronous
def async_function(**constants):
    inject = [] 
    #filesystem,messenger = di['filesystem'],di['messenger']
    if 'ports' in constants:
        for port in  constants['ports']:
            #print(port,constants)
            #path = {'persistence':'infrastructure.persistence.redis','presentation':'presentation.gui.flutter','messenger':'infrastructure.persistence.redis'}
            #module_port = importlib.import_module(path[port], package=None)
            #print(port)
            inject.append(di[port])
    
    def decorator(function):
        async def wrapper(*arg, **kwargs):
            output = None
            #print(f"[FLOW(START::{function.__name__}):]",inject,arg,kwargs)
            #di['messenger'].post(message=f"start::{function.__name__} , inject={inject},args={arg},kwargs={kwargs}")
            # Arguments
            '''if 'args' in constants:
                for arg_in in constants['args']:
                    #if arg_in not in kwargs: di['messenger'].post(type='error',message='ERROR: miss -> '+arg_in)
                    print(function.__name__,'==Errore==>',arg_in)'''
            #await asyncio.sleep(2)
            #output = await function(*arg, **kwargs)
            if 'at' in constants:
                #CALL_WHEN(function,constants['at'],*arg,**kwargs)
                pass
            else:
                test = list(arg) + inject
                output = await function(*test,**kwargs)
                #print('->',output)
            '''try:
                #output = await function(*arg, **kwargs)
                if 'at' in constants:
                    CALL_WHEN(function,constants['at'],*arg,**kwargs)
                else:
                    output = await function(*arg,**inject,**kwargs)
            except Exception as e:
                e_type = type(e).__name__
                e_file = e.__traceback__.tb_frame.f_code.co_filename
                e_line = e.__traceback__.tb_lineno

                e_message = str(e)

                print(f'exception type: {e_type}')

                print(f'exception function: {function}')

                print(f'exception filename: {e_file}')

                print(f'exception line number: {e_line}')

                print(f'exception message: {e_message}')'''
            #fs = await filesystem.tree(path='/home/asd/accent')
            #print(f"[FLOW(END::{function.__name__}):] return ->",type(output))
            #di['messenger'].post(message=f"end::{function.__name__} , payload={type(output)}")
            #await messenger.signal(keys='c',app={'broker':None},value="ciao")
            return output
        return wrapper
    return decorator

#synchronous
def function(**constants):
    inject = dict()
    test =[] 
    cc = constants
    if 'ports' in constants:
        for port in  constants['ports']:
            #print(port,constants)
            #path = {'persistence':'infrastructure.persistence.redis','presentation':'presentation.gui.flutter','messenger':'infrastructure.persistence.redis'}
            #module_port = importlib.import_module(path[port], package=None)
            #print(port)
            test.append(di[port])
    def decorator(function):
        def wrapper(*arg, **kwargs):
            '''if 'args' in cc:
                for ttx in  cc['args']:
                    module_entitie = importlib.import_module('domain.model.'+ttx, package=None)
                    ihh = getattr(module_entitie,ttx)
                    storekeeper = di['storekeeper']
                    kwargs = storekeeper.builder(ihh,kwargs)'''
                    #print(gg)
            output = None
            #di['messenger'].post(message=f"start::{function.__name__} , inject={inject},args={arg},kwargs={kwargs}")
            #await asyncio.sleep(2)
            try:
                output = function(*test,*arg,**inject,**kwargs)
            except Exception as e:
                e_type = type(e).__name__
                e_file = e.__traceback__.tb_frame.f_code.co_filename
                e_line = e.__traceback__.tb_lineno

                e_message = str(e)

                print(f'exception type: {e_type}')

                print(f'exception filename: {e_file}')

                print(f'exception line number: {e_line}')

                print(f'exception message: {e_message}')
            #di['messenger'].post(message=f"end::{function.__name__} , payload={type(output)}")
            return output
        return wrapper
    return decorator