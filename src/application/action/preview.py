modules = {'flow':'framework.service.flow'}

import js
@flow.asynchronous(managers=('messenger','presenter'))
async def preview(messenger,presenter,**constants):
    id = constants.get('id','')
    code = constants.get('code','')
    component = await presenter.component(name=id)
    editor = await presenter.component(name=code)
    test_value = editor['block-editor-'].getValue()
    print(component,test_value)
    view = await presenter.rebuild(id=id,view=component.get('view',''),data={'storekeeper':{'text':test_value}})