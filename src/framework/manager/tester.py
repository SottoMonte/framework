''' 
Una classe chiamata “trainer” può avere diverse funzioni a seconda del contesto in cui viene utilizzata. Ecco alcune possibilità:

Addestramento di agenti: In ambito appredimento automatico o di addestramento di agenti, un “trainer” potrebbe lavorare con NN, ML o IA per insegnare loro comandi, comportamenti desiderati o abilità specifiche.
'''
import unittest
import os
import framework.service.language as language

class tester():

    def __init__(self,**constants):
        self.sessions = dict()
        self.providers = constants['providers']

    def discover_tests(self):
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

    def run(self,**constants):
        print("run test")
        suite = self.discover_tests()
        runner = unittest.TextTestRunner()
        runner.run(suite)