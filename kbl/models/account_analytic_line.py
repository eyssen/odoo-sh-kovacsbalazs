# -*- coding: utf-8 -*-

from odoo import api, fields, models, _





class AccountAnalyticLine(models.Model):
    
    _inherit = 'account.analytic.line'
    
    
    coa = fields.Boolean(u'Teljesítésigazolás megvan?')
    foreign_language = fields.Boolean(u'Idegen nyelven történő tanácsadás?')
    include_in_customer = fields.Boolean(u'Szerepeljen az ügyfél teljesítésigazolásában?')
    include_in_colleaggue = fields.Boolean(u'Szerepeljen a kolléga havi teljesítménybérében?')
