import application.model.password as password
import application.model.name as name
import application.model.string as string
'''
# User
(code:natural)
(username)
(roles:array[enum])
(permissions:array[enum])
(active:boolean)
'''

'''user = (
    (('company','person'), None),
    (('name',), 'state'),#username
    (('password',), 'state'),
)'''

user = (
    {'model':name.name},
    {'model':password.password},
    {'name':'role','model':string.string},
)