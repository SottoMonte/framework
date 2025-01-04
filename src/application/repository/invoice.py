import application.model.client as client

#Table/Path
location = {'ERP': 'SCRM_Fatture', 'SAP': 'BusinessPartners','CACHE':'cache'}

scheme = (
    ('id',('Integer', 'primary_key')),
    ('name',('String')),
    ('subject_type',('String')),
    ('first_name',('String')),
    ('last_name',('String')),
    ('address1',('String')),
    ('city',('String')),
    ('prov',('String')),
    ('zip',('String')),
    ('piva',('String')),
    ('cf',('String')),
    ('phone',('String')),
    ('cell',('String')),
    ('email',('String')),
    ('payment_method',('String')),
    ('codice_sdi',('String')),
    ('codice_cig',('String')),
    ('legal_representative',('String')),
    ('iban',('String')),
    ('legal_representative_cf',('String')),
    #('birth_date',('DateTime')),
    ('birth_town',('String')),
    ('birth_province',('String')),
)

SAP = {
    'identifier':['CardCode','value.*.CardCode'],
    'name':['CardName','value.*.CardName'],
    'person.first':['ContactEmployees.0.FirstName','value.*.ContactEmployees.0.FirstName'],
}

ERP = {
    'identifier':'id',
    'name':'name',
    'person.first':'first_name',
}

keys = {'ERP': ERP, 'SAP': SAP}

values = {
    'identifier':[
        {
        'MODEL':lambda n: f"C{int(n):08d}" if type(n) == type('') else [f"C{int(item):08d}" for item in n],
        'ERP': lambda s: int(''.join(filter(str.isdigit, s))) if type(s) == type('') else [int(''.join(filter(str.isdigit, item))) for item in s], 
        'SAP': lambda n: f"C{int(n):08d}" if type(n) == type('') else [f"C{int(item):08d}" for item in n]
        },
    ],
    'person.gender':[
        {'MODEL':'male','ERP': 'm', 'SAP': 'gt_Male'},
        {'MODEL':'female','ERP': 'f', 'SAP': 'gt_Female'},
    ],
    '':[
        {'MODEL':'company','ERP': 'soggetto_giuridico', 'SAP': 'Rappresentante legale'},
        {'MODEL':'client','ERP': 'persona_fisica', 'SAP': 'Cliente'},
        {'MODEL':'RID','ERP': 'RID', 'SAP': 'SDDCORE01'},
        {'MODEL':'BOL','ERP': 'BOL', 'SAP': ' BOLCLI'},
        {'MODEL':'DIR','ERP': 'DIR', 'SAP': 'BOCLI'},
        {'MODEL':'client','ERP': 'Contacts::Customer', 'SAP': 'cCustomer'},
        {'MODEL':'agent','ERP': 'Contacts::Agent', 'SAP': 'cAgent'},
    ],
}