
repository = (
    {'name': 'id', 'type': 'integer', 'default': 0,'force_type':'str'},
    {'name': 'name', 'type': 'string', 'default': None,'required': True, 'regex': r'^[a-zA-Z0-9_-]+$'},
    {'name': 'branch', 'type': 'string', 'default': 'main', 'regex': r'^[a-zA-Z0-9_-]+$'},
    {'name': 'description', 'type': 'string', 'default': '', 'regex': r'^[a-zA-Z0-9_ -]*$'},
    {'name': 'private', 'type': 'bool', 'default': False,},
    {'name': 'owner', 'type': 'string', 'default': '0000', 'regex': r'^[a-zA-Z0-9_-]+$'},
    {'name': 'location', 'type': 'string', 'default': '0000', 'regex': r'^[a-zA-Z0-9_-]+$'},
    {'name': 'updated', 'type': 'string', 'default': '000', 'regex': r'^[a-zA-Z0-9_-]+$'},
    {'name': 'created', 'type': 'string', 'default': '0000', 'regex': r'^[a-zA-Z0-9_-]+$'},
    {'name': 'tree', 'type': 'list', 'default': []},
    {'name': 'sha', 'type': 'string', 'default': ''},
)