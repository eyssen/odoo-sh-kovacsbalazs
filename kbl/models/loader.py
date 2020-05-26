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
        
        # Server variables
        url = 'https://kbl-legal.odoo.com'
        db = 'kbl-legal-prod-495708'
        username = 'odoosupport@eyssen.hu'
        password = 'omakusoa'
        
        # Server Check
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), context=ssl._create_unverified_context())
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), context=ssl._create_unverified_context())
        
        # Constants
        COMPANY_ID = 1
        PROJECT_PROJECT = {
            2: 3,
            3: 2,
        }
        PROJECT_TASK_TYPE = {
            4: 1,
            5: 2,
            6: 3,
            7: 4,
        }

        # project.task
        for oldTask in models.execute_kw(db, uid, password, 'project.task', 'search_read', [[['id', '>', 0]]],
            {'fields': ['id', 'name', 'project_id', 'stage_id', 'sequence']}):
            Task = self.env['project.task'].search([('old_id', '=', oldTask['id'])])
            if Task:
                if Task.name != oldTask['name']:
                    Task.name = oldTask['name']
                if Task.project_id != PROJECT_PROJECT[oldTask['project_id'][0]]:
                    Task.project_id = PROJECT_PROJECT[oldTask['project_id'][0]]
                if Task.stage_id != PROJECT_TASK_TYPE[oldTask['stage_id'][0]]:
                    Task.stage_id = PROJECT_TASK_TYPE[oldTask['stage_id'][0]]
                if Task.sequence != oldTask['sequence']:
                    Task.sequence = oldTask['sequence']
            else:
                self.env['project.task'].create({
                    'company_id': COMPANY_ID,
                    'old_id': oldTask['id'],
                    'name': oldTask['name'],
                    'project_id': PROJECT_PROJECT[oldTask['project_id'][0]],
                    'stage_id': PROJECT_TASK_TYPE[oldTask['stage_id'][0]],
                    'sequence': oldTask['sequence'],
                })


    def load_from_kozbeszguru(self):
        
        pass


    def load_from_ams(self):
        
        pass
