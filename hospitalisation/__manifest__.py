# -*- coding: utf-8 -*-
{
    'name': "Hospitalisation",

    'summary': """
    """,

    'description': """
        
    """,

    'author': "Osisoftware",
    'website': "https://www.osisoftware.com",

    'category': 'Hospital',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/partner_inherit.xml',
        'views/osi_diagnostics.xml',
        'views/osi_lits.xml',
        'views/osi_tags.xml',
        'views/osi_stages.xml',
        'views/osi_region.xml',
        'views/osi_hospitalisation.xml',
        'views/res_config.xml',
        'views/menuitem.xml',
    ],

}
