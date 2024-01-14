# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'CMS Management',
    'version': '1.0',
    'category': 'CMS Word Press',
    'sequence': 15,
    'summary': 'For auto crawl data in website and push to wordPress sites.',
    'website': 'https://www.odoo.com',
    'depends': ['base'],
    'data': [
        'security/cms_wordpress_security.xml',
        'security/ir.model.access.csv',
        'data/cron.xml',
        'views/sourcing_sites_views.xml',
        'views/category_sites_views.xml',
        'views/posts_views.xml',
        'views/consuming_sites_views.xml',
        'wizard/preview_html_views.xml',
        'wizard/pushing_posts_confirm.xml',
        'views/menuitem.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_frontend': [

        ],
        'mail.assets_messaging': [],
        'web.assets_backend': [],
        'web.assets_tests': [],
        'web.qunit_suite_tests': [],
    },
    'license': 'LGPL-3',
}
