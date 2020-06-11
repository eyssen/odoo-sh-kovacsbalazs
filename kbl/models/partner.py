# -*- coding: utf-8 -*-
from odoo import api, fields, models
from werkzeug.urls import url_encode

import logging
_logger = logging.getLogger(__name__)





class Partner(models.Model):
    
    _inherit = 'res.partner'

    
    nickname = fields.Char(u'Becenév')
    
    
    @api.depends('is_company', 'name', 'parent_id.name', 'type', 'company_name', 'nickname')
    def _compute_display_name(self):
        diff = dict(show_address=None, show_address_only=None, show_email=None)
        names = dict(self.with_context(**diff).name_get())
        for partner in self:
            if partner.nickname:
                partner.display_name = names.get(partner.id) + ' [' + partner.nickname + ']'
            else:
                partner.display_name = names.get(partner.id)
