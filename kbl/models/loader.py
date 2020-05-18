# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import xmlrpc.client
import ssl

import logging
_logger = logging.getLogger(__name__)





class KblLoader(models.TransientModel):
    
    _name = 'kbl.loader'


    def load_from_kbl(self):
        
        pass


    def load_from_kozbeszguru(self):
        
        pass


    def load_from_ams(self):
        
        pass
