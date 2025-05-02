modules = {'flow':'framework.service.flow'}

import js
from js import ace,console
import pyodide

@flow.asynchronous(managers=('messenger','presenter'))
async def editor(messenger,presenter,**constants):
    target = constants.get('target','')
    field = constants.get('field','editor')
    file = constants.get('path','')
    
    # Mappatura delle estensioni ai moduli di modalità di ACE
    mode_mapping = {
        'py': 'ace/mode/python',
        'xml': 'ace/mode/xml',
        'js': 'ace/mode/javascript',
        'html': 'ace/mode/html',
        'css': 'ace/mode/css',
        'json': 'ace/mode/json',
        'txt': 'ace/mode/text',
        'toml': 'ace/mode/toml',
        'yaml': 'ace/mode/yaml',
        'yml': 'ace/mode/yaml',
        'md': 'ace/mode/markdown',
        'java': 'ace/mode/java',
        'c': 'ace/mode/c_cpp',
        'cpp': 'ace/mode/c_cpp',
        'h': 'ace/mode/c_cpp',
        'hpp': 'ace/mode/c_cpp',
        'cs': 'ace/mode/csharp',
        'php': 'ace/mode/php',
        'rb': 'ace/mode/ruby',
        'go': 'ace/mode/golang',
        'rs': 'ace/mode/rust',
        'sh': 'ace/mode/sh',
        'sql': 'ace/mode/sql',
        'swift': 'ace/mode/swift',
        'ts': 'ace/mode/typescript',
        'tsx': 'ace/mode/typescript',
        'vue': 'ace/mode/vue',
        'scss': 'ace/mode/scss',
        'less': 'ace/mode/less',
        'ini': 'ace/mode/ini',
        'bat': 'ace/mode/batchfile',
        'dockerfile': 'ace/mode/dockerfile',
        'makefile': 'ace/mode/makefile',
        'perl': 'ace/mode/perl',
        'pl': 'ace/mode/perl',
        'lua': 'ace/mode/lua',
        # Aggiungi altre estensioni se necessario
    }
    
    # Estrai l'estensione del file
    mode = mode_mapping.get(file.split('.')[-1], 'ace/mode/text')
    

    # Inizializza l'editor ACE sull'elemento
    ace_editor = ace.edit(field+target, {
        # Imposta la modalità dinamicamente
    })
    
    ace_editor.setTheme("ace/theme/github")
    ace_editor.session.setMode(mode)

    component = await presenter.component(name=target)
    component[field] = ace_editor

    
    def printEditorDetails():
        print('printEditorDetails')
        '''cursorPosition = ace_editor.getCursorPosition()

        cursorPosition = ace_editor.getCursorPosition()

        # Ottieni il numero di spazi per l'indentazione
        tabSize = ace_editor.session.getTabSize()

        # Ottieni il formato di carattere di a capo
        # "unix" (LF) o "windows" (CRLF)
        newLineMode = ace_editor.session.getNewLineMode()  

        # Ottieni il contenuto della riga attuale
        currentLine = ace_editor.session.getLine(cursorPosition.row)

        # Conta gli spazi iniziali della riga attuale
        #leadingSpaces = currentLine.match('/^\s*/')[0].length

        # Stampa le informazioni
        console.log("Riga: " + (cursorPosition.row + 1))
        console.log("Colonna: " + (cursorPosition.column + 1))
        console.log("Numero di spazi per indentazione: " + tabSize)
        console.log("Tipo di carattere di a capo: " + newLineMode)
        #console.log("Spazi effettivi sulla riga corrente: " + leadingSpaces)'''
    try:
        #cursor = ace_editor.getCursorPosition()
        #print(cursor)
        #aaa = pyodide.create_proxy(ttt)
        #component['proxy'] = aaa
        #component['editor'].addEventListener('click',presenter.info)
        #ace_editor.session.selection.on("changeCursor",component['proxy'])
        pass
    except Exception as e:
        print(e)
        console.log(e)
    
    