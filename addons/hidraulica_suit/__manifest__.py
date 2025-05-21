{
    "name": "Suit Hidráulica",
    "summary": "Hidráulica VC",
    "author": "ADATECS.surl",
    "website": "https://www.desoft.cu",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "17.0.0.0.1",
    "license": "LGPL-3",
    # any module necessary for this one to work correctly
    "depends": [
        "sale_management",
        "sale_purchase",
        "account",
        "l10n_latam_base",
        "sale_margin",
    ],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "data/res_partner_data.xml",
        "data/res_company_data.xml",
        "data/res_bank_data.xml",
        "views/work_program_views.xml",
        "views/sale_order_views.xml",
        "views/res_company_views.xml",
        "views/res_partner_views.xml",
    ],
}
