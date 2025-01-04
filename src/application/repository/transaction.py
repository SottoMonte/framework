import domain.model.client as client
from kink import inject,di

values = {
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
location = {'FAST':'FAST','CACHE':'cache'}

keys_test = (
    {'MODEL':'identifier'},
    {'MODEL':'state'},
    {'MODEL':'action'},
    {'MODEL':'remark'},
    {'MODEL':'worker'},
    {'MODEL':'parameter'},
    {'MODEL':'transaction'},
    {'MODEL':'result'},
)