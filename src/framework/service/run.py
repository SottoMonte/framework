import asyncio
import sys

loader = language.load_main(language,area="framework",service='service',adapter='loader')

#modules = {'loader': 'framework.service.loader','language': 'framework.service.language'}

def build():
    pass

#@flow.synchronous(managers=('tester',))
def application(tester=None, **constants):
    try:
        if tester and '--test' in constants.get('args',[]):
            tester.run()
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        event_loop.create_task(loader.bootstrap())
        event_loop.run_forever()
    except KeyboardInterrupt:
        # Interruzione manuale con Ctrl+C
        #asyncio.create_task(messenger.post(msg="Interruzione da tastiera (Ctrl + C)."))
        pass
    except Exception as e:
        # Gestione di altre eccezioni con nome file, modulo e numero di riga
        exc_type, exc_value, exc_traceback = sys.exc_info()
        last_frame = exc_traceback.tb_frame
        filename = last_frame.f_code.co_filename
        module = last_frame.f_code.co_name
        line_number = exc_traceback.tb_lineno
        print(f"RUN -Errore generico: {e}")
        print(f"File: {filename}, Modulo: {module}, Linea: {line_number}")
    finally:
        # Chiusura del loop
        '''if event_loop.is_running():
            event_loop.stop()
        event_loop.close()'''
        #logging.info(msg="Event loop chiuso.")
        pass