import asyncio
import sys

flow = language.load_module(area="framework",service='service',adapter='flow')
loader = language.load_module(area="framework",service='service',adapter='loader')

loader.bootstrap_adapter()

@flow.asynchronous(managers=('presentation','messenger'))
async def main(presentation=None,messenger=None, **constants):
    event_loop = asyncio.get_event_loop()
    await messenger.post(msg="Caricamento degli elementi della presentazione.")
    for item in presentation:
        await messenger.post(msg=f"Caricamento dell'elemento: {item}")
        if hasattr(item, "loader"):
            item.loader(loop=event_loop)
        else:
            await messenger.post(msg=f"L'elemento {item} non ha un metodo 'loader'.")
        

@flow.synchronous(managers=('tester',))
def application(tester=None, **constants):
    try:
        if tester:
            tester.run()
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        event_loop.create_task(main())
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
        print(f"Errore generico: {e}")
        print(f"File: {filename}, Modulo: {module}, Linea: {line_number}")
    finally:
        # Chiusura del loop
        '''if event_loop.is_running():
            event_loop.stop()
        event_loop.close()'''
        #logging.info(msg="Event loop chiuso.")
        pass