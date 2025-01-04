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
location = {'SCRAPING': 'cpe/overview',}

keys_test = (
    {'MODEL':'cpeid','SCRAPING': 'td:0','SCRAPING': 'body:0',},
    {'MODEL':'state','SCRAPING': 'td:1',},
    {'MODEL':'name','SCRAPING': 'td:3',},
    {'MODEL':'location','SCRAPING': 'td:4',},
    {'MODEL':'manufacturer','SCRAPING': 'td:5',},
    {'MODEL':'model','SCRAPING': 'td:6',},
    {'MODEL':'version','SCRAPING': 'td:7',},
    {'MODEL':'ip','SCRAPING': 'td:8',},
    {'MODEL':'last','SCRAPING': 'td:9',},
)