# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    'name' : 'Cookie Notice',
    'author' : 'Softhealer Technologies',
    'website': 'http://www.softhealer.com',
    "support": "info@softhealer.com",    
    'category': 'website',
    'summary': 'Cookie Notice allows you to elegantly inform users that your site uses cookies and to comply with the EU cookie law regulations.',
    'description': """
EU Cookie Law Notice    
     allows you to elegantly inform users that your site uses cookies and to comply with the EU cookie law regulations. 

    This plugin uses implied consent, adding a subtle banner to your website either in the header or footer so you can show your compliance status regarding the new EU Cookie Law.

    You can customise the style so it fits in with your existing website- change the position on the page.
    
                    """,    
    'version':'12.0.1',
    'depends' : ['base','website','portal'],
    'application' : True,
    'data' : [
            
            'views/website_view.xml',       
            'views/res_config_settings_view.xml',
            'views/cookie_notice_template.xml',      
     
            ],            
    'images': ['static/description/background.png',],              
    'auto_install':False,
    'installable' : True,
    "price": 15,
    "currency": "EUR"   
}
