flow = language.load_module(area="framework",service='service',adapter='flow')
import js
from js import ace,console
import pyodide

@flow.asynchronous(managers=('messenger','presenter'))
async def editor(messenger,presenter,**constants):
    target = constants.get('target','')
    
    
    # Inizializza l'editor ACE sull'elemento
    ace_editor = ace.edit(target, {
        "mode": "ace/mode/python",
        "theme": "ace/theme/github",
        "autoScrollEditorIntoView": True,
        "minLines": 10,
        "maxLines": 30,
        "wrap": True,
        "useWorker": True
    })

    component = await presenter.component(name=target.replace('block-editor-',''))
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
    
    