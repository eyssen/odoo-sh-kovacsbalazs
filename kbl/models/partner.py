# -*- coding: utf-8 -*-
from odoo import api, fields, models
from werkzeug.urls import url_encode

import logging
_logger = logging.getLogger(__name__)





class ResPartner(models.Model):
    
    _inherit = 'res.partner'
    
    
    old_id = fields.Integer(u'Régi Odoo azonosító')