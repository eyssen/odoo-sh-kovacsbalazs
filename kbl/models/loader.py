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
        password = 'pynfor-byswu2-gUdguf'
        
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
        
        # res.partner
        _logger.info("== START KBL Partner ==")
        for x in [1, 2]:
            if x == 1:
                oldPartners = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['is_company', '=', 1]]],
                    {'fields': ['id', 'parent_id', 'name', 'active', 'customer', 'supplier', 'employee', 'type', 'street', 'street2', 'city', 'zip', 'phone', 'mobile', 'email', 'website', 'comment', 'vat_hu', 'vat', 'reg_number', 'create_date', 'write_date']})
            else:
                oldPartners = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['is_company', '=', 0]]],
                    {'fields': ['id', 'parent_id', 'name', 'active', 'customer', 'supplier', 'employee', 'type', 'street', 'street2', 'city', 'zip', 'phone', 'mobile', 'email', 'website', 'comment', 'vat_hu', 'vat', 'reg_number', 'create_date', 'write_date']})
            for oldPartner in oldPartners:
                #TODO: country, tags (category_id), költségvetési pozíció
                Partner = self.env['res.partner'].search([('old_id', '=', oldPartner['id'])])
                if oldPartner['parent_id']:
                    ParentId = self.env['res.partner'].search([('old_id', '=', oldPartner['parent_id'][0])], limit=1)
                else:
                    ParentId = None
                if Partner:
                    if x == 1:
                        if Partner.is_company != True:
                            Partner.is_company = True
                    else:
                        if Partner.is_company != False:
                            Partner.is_company = False
                    if ParentId:
                        if Partner.parent_id.id != ParentId.id:
                            Partner.parent_id = ParentId.id
                    if Partner.name != oldPartner['name']:
                        Partner.name = oldPartner['name']
                    if Partner.active != oldPartner['active']:
                        Partner.active = oldPartner['active']
                    if Partner.customer_rank != oldPartner['customer']:
                        Partner.customer_rank = oldPartner['customer']
                    if Partner.supplier_rank != oldPartner['supplier']:
                        Partner.supplier_rank = oldPartner['supplier']
                    if Partner.employee != oldPartner['employee']:
                        Partner.employee = oldPartner['employee']
                    if Partner.type != oldPartner['type']:
                        Partner.type = oldPartner['type']
                    if Partner.street != oldPartner['street']:
                        Partner.tstreetype = oldPartner['street']
                    if Partner.street != oldPartner['street']:
                        Partner.street = oldPartner['street']
                    if Partner.street2 != oldPartner['street2']:
                        Partner.street2 = oldPartner['street2']
                    if Partner.city != oldPartner['city']:
                        Partner.city = oldPartner['city']
                    if Partner.zip != oldPartner['zip']:
                        Partner.zip = oldPartner['zip']
                    if Partner.phone != oldPartner['phone']:
                        Partner.phone = oldPartner['phone']
                    if Partner.mobile != oldPartner['mobile']:
                        Partner.mobile = oldPartner['mobile']
                    if Partner.email != oldPartner['email']:
                        Partner.email = oldPartner['email']
                    if Partner.website != oldPartner['website']:
                        Partner.website = oldPartner['website']
                    if Partner.comment != oldPartner['comment']:
                        Partner.comment = oldPartner['comment']
                    if Partner.vat_hu != oldPartner['vat_hu']:
                        Partner.vat_hu = oldPartner['vat_hu']
                    if Partner.vat != oldPartner['vat']:
                        Partner.vat = oldPartner['vat']
                    if Partner.reg_number != oldPartner['reg_number']:
                        Partner.reg_number = oldPartner['reg_number']
                    if Partner.create_date != oldPartner['create_date']:
                        Partner.create_date = oldPartner['create_date']
                    if Partner.write_date != oldPartner['write_date']:
                        Partner.write_date = oldPartner['write_date']
                else:
                    vals = {
                        'company_id': COMPANY_ID,
                        'old_id': oldPartner['id'],
                        'name': oldPartner['name'],
                        'active': oldPartner['active'],
                        'customer_rank': oldPartner['customer'],
                        'supplier_rank': oldPartner['supplier'],
                        'employee': oldPartner['employee'],
                        'type': oldPartner['type'],
                        'street': oldPartner['street'],
                        'street2': oldPartner['street2'],
                        'city': oldPartner['city'],
                        'zip': oldPartner['zip'],
                        'phone': oldPartner['phone'],
                        'mobile': oldPartner['mobile'],
                        'email': oldPartner['email'],
                        'website': oldPartner['website'],
                        'vat_hu': oldPartner['vat_hu'],
                        'vat': oldPartner['vat'],
                        'reg_number': oldPartner['reg_number'],
                        'create_date': oldPartner['create_date'],
                        'write_date': oldPartner['write_date'],
                    }
                    if x == 1:
                        vals['is_company'] = True
                    else:
                        vals['is_company'] = False
                    if ParentId:
                        vals['parent_id'] = ParentId.id
                    self.env['res.partner'].create(vals)
        _logger.info("== END KBL Partner ==")
        
        # project.task
        _logger.info("== START KBL Task ==")
        for oldTask in models.execute_kw(db, uid, password, 'project.task', 'search_read', [[['id', '>', 0]]],
            {'fields': ['id', 'name', 'project_id', 'stage_id', 'sequence', 'create_date', 'write_date', 'partner_id', 'next_step', 'invoice_plan_date', 'weekly_notofy_emails', 'user_id']}):
            Task = self.env['project.task'].search([('old_id', '=', oldTask['id'])])
            if oldTask['partner_id']:
                Partner = self.env['res.partner'].search([('old_id', '=', oldTask['partner_id'][0])], limit=1)
            else:
                Partner = None
            User = self.env['res.users'].search([('old_id', '=', oldTask['user_id'][0])], limit=1)
            if Task:
                if Task.name != oldTask['name']:
                    Task.name = oldTask['name']
                if Task.project_id.id != PROJECT_PROJECT[oldTask['project_id'][0]]:
                    Task.project_id = PROJECT_PROJECT[oldTask['project_id'][0]]
                if Task.stage_id.id != PROJECT_TASK_TYPE[oldTask['stage_id'][0]]:
                    Task.stage_id = PROJECT_TASK_TYPE[oldTask['stage_id'][0]]
                if Task.sequence != oldTask['sequence']:
                    Task.sequence = oldTask['sequence']
                if Task.create_date != oldTask['create_date']:
                    Task.create_date = oldTask['create_date']
                if Task.write_date != oldTask['write_date']:
                    Task.write_date = oldTask['write_date']
                if Partner:
                    if Task.partner_id.id != Partner.id:
                        Task.partner_id = Partner.id
                if Task.next_step != oldTask['next_step']:
                    Task.next_step = oldTask['next_step']
                if Task.invoice_plan_date != oldTask['invoice_plan_date']:
                    Task.invoice_plan_date = oldTask['invoice_plan_date']
                if Task.weekly_notofy_emails != oldTask['weekly_notofy_emails']:
                    Task.weekly_notofy_emails = oldTask['weekly_notofy_emails']
                if Task.user_id.id != User.id:
                    Task.user_id = User.id
            else:
                vals = {
                    'company_id': COMPANY_ID,
                    'old_id': oldTask['id'],
                    'name': oldTask['name'],
                    'project_id': PROJECT_PROJECT[oldTask['project_id'][0]],
                    'stage_id': PROJECT_TASK_TYPE[oldTask['stage_id'][0]],
                    'sequence': oldTask['sequence'],
                    'create_date': oldTask['create_date'],
                    'write_date': oldTask['write_date'],
                    'next_step': oldTask['next_step'],
                    'invoice_plan_date': oldTask['invoice_plan_date'],
                    'weekly_notofy_emails': oldTask['weekly_notofy_emails'],
                    'user_id': User.id,
                }
                if Partner:
                    vals['partner_id'] = Partner.id
                self.env['project.task'].create(vals)
        _logger.info("== END KBL Task ==")
        
        # project.task.progress
        _logger.info("== START KBL Tevékenységek ==")
        for oldProgress in models.execute_kw(db, uid, password, 'project.task.progress', 'search_read', [[['id', '>', 0]]],
            {'fields': ['id', 'name', 'task_id', 'date', 'create_date', 'write_date']}):
            Progress = self.env['project.task.progress'].search([('old_id', '=', oldTask['id'])])
            if Progress:
                if Progress.name != oldProgress['name']:
                    Progress.name = oldProgress['name']
                if Progress.date != oldProgress['date']:
                    Progress.date = oldProgress['date']
                if Progress.create_date != oldProgress['create_date']:
                    Progress.create_date = oldProgress['create_date']
                if Progress.write_date != oldProgress['write_date']:
                    Progress.write_date = oldProgress['write_date']
                if Progress.company_id != 1:
                    Progress.company_id = 1
            else:
                vals = {
                    'company_id': COMPANY_ID,
                    'old_id': oldProgress['id'],
                    'name': oldProgress['name'],
                    'task_id': self.env['project.task'].search([('old_id', '=', oldProgress['task_id'][0])], limit=1).id,
                    'date': oldProgress['date'],
                    'create_date': oldProgress['create_date'],
                    'write_date': oldProgress['write_date'],
                }
                self.env['project.task.progress'].create(vals)
        _logger.info("== END KBL Tevékenységek ==")


    def load_from_kozbeszguru(self):
        
        pass


    def load_from_ams(self):
        
        pass





class ResPartner(models.Model):
    
    _inherit = 'res.partner'
    
    
    old_id = fields.Integer(u'Régi Odoo azonosító')





class ProjectTask(models.Model):
    
    _inherit = 'project.task'
    
    
    old_id = fields.Integer(u'Régi Odoo azonosító')





class ProjectTaskProgress(models.Model):
    
    _inherit = 'project.task.progress'
    
    
    old_id = fields.Integer(u'Régi Odoo azonosító')





class ResUsers(models.Model):
    
    _inherit = 'res.users'
    
    
    old_id = fields.Integer(u'Régi Odoo azonosító')
