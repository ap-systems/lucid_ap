{
    'name': "Lucid Crm", 
        'summary': "",
       'version': "1.8",
       'depends': ['base', 'crm' ,'sale','sale_management','project','sale_crm'],
       'author': "AP Accounting Services",
       'license': '',
       'website': "http://www.ap-accounting.co.za",
       'category': 'crm',
       'description': """
    
    """,
       'data': [
                'security/ir.model.access.csv',
                'views/crm.xml',
                # 'views/sale.xml',
                'views/project.xml'
        ],
       'qweb': [ 
           
           
           ],
       'sequence': 10,
       'installable': True ,
       'auto_install':  False,
       }

