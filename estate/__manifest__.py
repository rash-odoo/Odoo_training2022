{
    'name' : 'Real Estate',
    'version': '1.0',
    'category': 'Tools',
    #'summary':'This module will add a record to store some information'.
    #'description': 'This module will add a record to store details',
    'application' : True,
    #'depends':  'base',
    #'auto-install':'False'    
    'data': [
        'security/ir.model.access.csv',
        'security/estate_property_security.xml',
        'views/estate_property_manus.xml',
        'views/estate_property_views.xml',
        'views/my_property_views.xml',
        'views/estate_template.xml',
        'wizard/estate_wizard_views.xml',
        
    ],  
    #'licence' : 'LGPL-3',
}