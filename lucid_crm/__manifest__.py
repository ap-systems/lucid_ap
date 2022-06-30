{
    'name': "Lucid Crm", 
        'summary': "",
       'version': "1.3",
       'depends': ['base', 'crm' ,'sale','sale_management','project'],
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

