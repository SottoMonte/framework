import application.model.client as client



values = {
    'identifier':[
        {'MODEL':lambda n: f"C{int(n):08d}" if type(n) == type('') else [f"C{int(item):08d}" for item in n],
         'ERP': lambda s: int(''.join(filter(str.isdigit, s))) if type(s) == type('') else [int(''.join(filter(str.isdigit, item))) for item in s], 
         'SAP': lambda n: f"C{int(n):08d}" if type(n) == type('') else [f"C{int(item):08d}" for item in n]},
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

#Table/Path
location = {'ERP': 'SCRM_Customers', 'SAP': 'BusinessPartners','CACHE':'cache'}

keys_test = (
    {'MODEL':'identifier','ERP': 'id', 'SAP': ['CardCode','value.*.CardCode']},
    #{'MODEL':'type','ERP': 'name', 'SAP': 'CardType'},
    {'MODEL':'name','ERP': 'name', 'SAP': ['CardName','value.*.CardName']},
    {'MODEL':'person.first','ERP': 'first_name', 'SAP': ['ContactEmployees.0.FirstName','value.*.ContactEmployees.0.FirstName']},
    {'MODEL':'person.last','ERP': 'last_name', 'SAP': ['ContactEmployees.0.LastName','value.*.ContactEmployees.0.LastName']},
    {'MODEL':'person.gender','ERP': 'sex', 'SAP': ['ContactEmployees.0.Gender','value.*.ContactEmployees.0.Gender']},
    {'MODEL':'person.note','ERP': 'note', 'SAP': ['ContactEmployees.0.Name','value.*.ContactEmployees.0.Name']},
    {'MODEL':'person.cf','ERP': 'cf', 'SAP': ['AdditionalID','ContactEmployees.0.U_ORK_CFLegalRapresentative','value.*.AdditionalID']},#['AdditionalID','U_ORK_CFLegalRapresentative']
    {'MODEL':'person.city','ERP': 'birth_town', 'SAP': ['ContactEmployees.0.CityOfBirth','value.*.ContactEmployees.0.CityOfBirth']},
    {'MODEL':'person.date','ERP': 'birth_date', 'SAP': ['ContactEmployees.0.DateOfBirth','value.*.ContactEmployees.0.DateOfBirth']},
    {'MODEL':'person.province','ERP': 'birth_province', 'SAP': ['ContactEmployees.0.PlaceOfBirth','value.*.ContactEmployees.0.PlaceOfBirth']},
    {'MODEL':'person.contact.email','ERP': 'email', 'SAP': ['EmailAddress','value.*.EmailAddress']},
    {'MODEL':'person.contact.website','ERP': '', 'SAP': ['ContactEmployees.0.Website','value.*.ContactEmployees.0.Website']},
    {'MODEL':'person.contact.phone','ERP': 'phone', 'SAP': ['ContactEmployees.0.Phone1','value.*.ContactEmployees.0.Phone1']},
    {'MODEL':'person.contact.cellular','ERP': 'phone', 'SAP': ['ContactEmployees.0.MobilePhone','value.*.ContactEmployees.0.MobilePhone']},
    {'MODEL':'person.contact.location.address','ERP': 'address1', 'SAP': ['Address','value.*.Address']},
    {'MODEL':'person.contact.location.zip','ERP': 'zip', 'SAP': ['ZipCode','value.*.ZipCode']},
    {'MODEL':'person.contact.location.city','ERP': 'city', 'SAP': ['City','value.*.City']},
    {'MODEL':'person.contact.location.province','ERP': 'prov', 'SAP': ['County','value.*.County']},
    {'MODEL':'payment.method','ERP': 'payment_method', 'SAP': ['PeymentMethodCode','value.*.PeymentMethodCode']},
    {'MODEL':'payment.iban','ERP': 'iban', 'SAP': ['IBAN','value.*.IBAN']},
    #{'MODULE':'','ERP': 'piva', 'SAP': 'UnifiedFederalTaxID'},
)

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