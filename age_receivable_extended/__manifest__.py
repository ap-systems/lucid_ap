{'name': "Age Receivable Extended", 'summary': "",
       'version': "1.0",
       'depends': ['base','account','account_reports','project'],
       'author': "AP Accounting Services",
       'license': '',
       'website': "http://www.ap-accounting.co.za",
       'category': 'Account',
       'description': """
    
    """,
       'data': [
            'views/report.xml',
            'views/project_view.xml',
            'wizard/aged_receivable.xml',
            'security/ir.model.access.csv',
        ],
       'qweb': [],
       'sequence': 10,
       'installable': True ,
       'auto_install':  False,
       }

