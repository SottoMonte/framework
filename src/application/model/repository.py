
repository = (
    {'name': 'id', 'type': 'integer', 'default': None, 'regex': r'^[a-zA-Z0-9_-]+$'},
    {'name': 'name', 'type': 'string', 'default': None,'required': True, 'regex': r'^[a-zA-Z0-9_-]+$'},
    {'name': 'branch', 'type': 'string', 'default': 'main', 'regex': r'^[a-zA-Z0-9_-]+$'},
    {'name': 'description', 'type': 'string', 'default': None, 'regex': r'^[a-zA-Z0-9_-]+$'},
    {'name': 'private', 'type': 'string', 'default': 'private', 'regex': r'^[a-zA-Z0-9_-]+$'},
    {'name': 'owner', 'type': 'string', 'default': None,'required': True, 'regex': r'^[a-zA-Z0-9_-]+$'},
    {'name': 'location', 'type': 'string', 'default': None, 'regex': r'^[a-zA-Z0-9_-]+$'},
    {'name': 'updated_at', 'type': 'string', 'default': None, 'regex': r'^[a-zA-Z0-9_-]+$'},
    {'name': 'created_at', 'type': 'string', 'default': None, 'regex': r'^[a-zA-Z0-9_-]+$'},
    {'name': 'tree', 'type': 'list', 'default': dict()},
    {'name': 'sha', 'type': 'string', 'default': ''},
)