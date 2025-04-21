import subprocess
import datetime
import importlib
import os

class adapter(message.port):

    def __init__(self, **constants):
        self.config = constants['config']
        self.connection = self.loader()
        self.processable = dict()

    async def act(self, playbook_path, inventory_file=None, extra_vars=None):
        """
        Metodo per eseguire un playbook Ansible utilizzando subprocess.

        :param playbook_path: Il percorso del playbook Ansible.
        :param inventory_file: (Opzionale) Il file di inventario per Ansible.
        :param extra_vars: (Opzionale) Variabili extra da passare al playbook.
        :return: Il risultato dell'esecuzione del playbook.
        """
        command = ['ansible-playbook', playbook_path]

        if inventory_file:
            command.extend(['-i', inventory_file])

        if extra_vars:
            for key, value in extra_vars.items():
                command.extend(['--extra-vars', f"{key}={value}"])

        try:
            # Esegui il playbook utilizzando subprocess
            result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            # Gestisci errori in caso di fallimento dell'esecuzione
            return f"Errore durante l'esecuzione del playbook: {e.stderr}"