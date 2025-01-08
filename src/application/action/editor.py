flow = language.load_module(area="framework",service='service',adapter='flow')
import js
from js import ace,console
import pyodide

@flow.asynchronous(managers=('messenger','presenter'))
async def editor(messenger,presenter,**constants):
    target = constants.get('target','')
    file = constants.get('identifier','')
    print('file',file)
    # Mappatura delle estensioni ai moduli di modalità di ACE
    mode_mapping = {
        'py': 'ace/mode/python',
        'xml': 'ace/mode/xml',
        'js': 'ace/mode/javascript',
        'html': 'ace/mode/html',
        'css': 'ace/mode/css',
        'json': 'ace/mode/json',
        # Aggiungi altre estensioni se necessario
    }

    # Estrai l'estensione del file
    file_extension = file.split('.')[-1].lower() if '.' in file else ''

    # Determina la modalità in base all'estensione
    mode = mode_mapping.get(file_extension, 'text')  # Usa 'text' come fallback

    # Inizializza l'editor ACE sull'elemento
    ace_editor = ace.edit(target, {
        # Imposta la modalità dinamicamente
    })
    print(mode)
    ace_editor.setTheme("ace/theme/github")
    ace_editor.session.setMode(mode)

    component = await presenter.component(name=target.replace('block-editor-', ''))
    component['editor'] = ace_editor

    
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
    
    