import asyncio
import sys
import unittest
import os 

flow = language.load_module(area="framework",service='service',adapter='flow')
loader = language.load_module(area="framework",service='service',adapter='loader')

loader.bootstrap_adapter()


def discover_tests():
    # Pattern personalizzato per i test
    test_dir = './src'
    test_suite = unittest.TestSuite()
    
    # Scorri tutte le sottocartelle e i file
    for root, dirs, files in os.walk(test_dir):
        for file in files:
            if file.endswith('.test.py'):
                # Crea il nome del modulo di test per ciascun file trovato
                module_name = os.path.splitext(file)[0]
                module_path = os.path.join(root, file)
                
                # Importa il modulo di test dinamicamente
                try:
                    module = language.get_module_os(module_path,language)
                    # Aggiungi i test dal modulo
                    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(module))
                except ImportError as e:
                    print(f"Errore nell'importazione del modulo: {module_path}, {e}")
    return test_suite

@flow.function(ports=('presentation',))
def test(presentation=[],**constants):
    
    try:
        print("run test")
        #unittest.main()
        suite = discover_tests()
        runner = unittest.TextTestRunner()
        runner.run(suite)
    except Exception as e:
        print("errore generico",e)
    except KeyboardInterrupt:
        print("Ctrl + C")

@flow.function(ports=('presentation',))
def application(presentation=[],**constants):
    app = constants
    
    eventloop = asyncio.new_event_loop()
    asyncio.set_event_loop(eventloop)
    
    try:
        test()
        for x in presentation:
            x.loader(loop=eventloop)
        
        eventloop.run_forever()
    except Exception as e:
        print("errore generico",e)
    except KeyboardInterrupt:
        print("Ctrl + C")