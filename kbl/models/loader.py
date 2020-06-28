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
        _logger.info('===== load_from_kbl =====')
        
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
                Partner = self.env['res.partner'].search([('company_id', '=', COMPANY_ID), ('old_id', '=', oldPartner['id'])])
                if oldPartner['parent_id']:
                    ParentId = self.env['res.partner'].search([('company_id', '=', COMPANY_ID), ('old_id', '=', oldPartner['parent_id'][0])], limit=1)
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
            Task = self.env['project.task'].search([('company_id', '=', COMPANY_ID), ('old_id', '=', oldTask['id'])])
            if oldTask['partner_id']:
                Partner = self.env['res.partner'].search([('company_id', '=', COMPANY_ID), ('old_id', '=', oldTask['partner_id'][0])], limit=1)
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
            Progress = self.env['project.task.progress'].search([('company_id', '=', COMPANY_ID), ('old_id', '=', oldProgress['id'])])
            if Progress:
                if Progress.name != oldProgress['name']:
                    Progress.name = oldProgress['name']
                if Progress.date != oldProgress['date']:
                    Progress.date = oldProgress['date']
                if Progress.create_date != oldProgress['create_date']:
                    Progress.create_date = oldProgress['create_date']
                if Progress.write_date != oldProgress['write_date']:
                    Progress.write_date = oldProgress['write_date']
            else:
                vals = {
                    'company_id': COMPANY_ID,
                    'old_id': oldProgress['id'],
                    'name': oldProgress['name'],
                    'task_id': self.env['project.task'].search([('company_id', '=', COMPANY_ID), ('old_id', '=', oldProgress['task_id'][0])], limit=1).id,
                    'date': oldProgress['date'],
                    'create_date': oldProgress['create_date'],
                    'write_date': oldProgress['write_date'],
                }
                if vals['task_id']:
                    self.env['project.task.progress'].create(vals)
        _logger.info("== END KBL Tevékenységek ==")


    def load_from_kozbeszguru(self):
        _logger.info('===== load_from_kozbeszguru =====')
        
        # Server variables
        url = 'https://www.kozbeszguru.hu'
        db = 'kozbeszguru_odoo'
        username = 'odoosupport@eyssen.hu'
        password = 'tihvax-perhis-zItqa1'
        
        # Server Check
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), context=ssl._create_unverified_context())
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), context=ssl._create_unverified_context())
        
        # Constants
        COMPANY_ID = 2
        PROJECT_PROJECT = {
            4: 7,
            21: 8,
            2: 9,
            15: 10,
            19: 11,
            6: 12,
            8: 13,
            18: 14,
            13: 15,
            9: 16,
            10: 17,
            7: 18,
        }
        PROJECT_TASK_TYPE = {
            19: 1,
            17: 5,
            11: 6,
            20: 7,
            28: 8,
            16: 3,
            30: 9,
            14: 10,
            23: 4,
            31: 11,
            15: 12,
            33: 13,
            12: 14,
            13: 15,
            22: 3,
        }
        EMPLOYEE = {
            3: 3,
            2: 4,
            4: 5,
            5: 6,
            25: 7,
            14: 8,
            8: 9,
            9: 10,
            6: 11,
            23: 12,
            20: 13,
            10: 14,
            24: 15,
            11: 16,
            13: 17,
            29: 18,
            21: 19,
            16: 20,
            12: 21,
            30: 22,
        }
        
#         # res.partner
#         _logger.info("== START Guru Partner ==")
#         for x in [1, 2]:
#             if x == 1:
#                 oldPartners = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['is_company', '=', 1]]],
#                     {'fields': ['id', 'parent_id', 'name', 'active', 'customer', 'supplier', 'employee', 'type', 'street', 'street2', 'city', 'zip', 'phone', 'mobile', 'email', 'website', 'comment', 'vat_hu', 'vat', 'reg_number', 'create_date', 'write_date']})
#             else:
#                 oldPartners = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['is_company', '=', 0]]],
#                     {'fields': ['id', 'parent_id', 'name', 'active', 'customer', 'supplier', 'employee', 'type', 'street', 'street2', 'city', 'zip', 'phone', 'mobile', 'email', 'website', 'comment', 'vat_hu', 'vat', 'reg_number', 'create_date', 'write_date']})
#             for oldPartner in oldPartners:
#                 #TODO: country, tags (category_id), költségvetési pozíció
#                 if oldPartner['id'] == 1:
#                     oldPartner['id'] = 14
#                 if oldPartner['parent_id'] == 1:
#                     oldPartner['parent_id'] = 14
#                 Partner = self.env['res.partner'].search([('company_id', '=', COMPANY_ID), ('old_id', '=', oldPartner['id'])])
#                 if oldPartner['parent_id']:
#                     ParentId = self.env['res.partner'].search([('company_id', '=', COMPANY_ID), ('old_id', '=', oldPartner['parent_id'][0])], limit=1)
#                 else:
#                     ParentId = None
#                 if Partner:
#                     if x == 1:
#                         if Partner.is_company != True:
#                             Partner.is_company = True
#                     else:
#                         if Partner.is_company != False:
#                             Partner.is_company = False
#                     if ParentId:
#                         if Partner.parent_id.id != ParentId.id:
#                             Partner.parent_id = ParentId.id
#                     if Partner.name != oldPartner['name']:
#                         Partner.name = oldPartner['name']
#                     if Partner.active != oldPartner['active']:
#                         Partner.active = oldPartner['active']
#                     if Partner.customer_rank != oldPartner['customer']:
#                         Partner.customer_rank = oldPartner['customer']
#                     if Partner.supplier_rank != oldPartner['supplier']:
#                         Partner.supplier_rank = oldPartner['supplier']
#                     if Partner.employee != oldPartner['employee']:
#                         Partner.employee = oldPartner['employee']
#                     if Partner.type != oldPartner['type']:
#                         Partner.type = oldPartner['type']
#                     if Partner.street != oldPartner['street']:
#                         Partner.tstreetype = oldPartner['street']
#                     if Partner.street != oldPartner['street']:
#                         Partner.street = oldPartner['street']
#                     if Partner.street2 != oldPartner['street2']:
#                         Partner.street2 = oldPartner['street2']
#                     if Partner.city != oldPartner['city']:
#                         Partner.city = oldPartner['city']
#                     if Partner.zip != oldPartner['zip']:
#                         Partner.zip = oldPartner['zip']
#                     if Partner.phone != oldPartner['phone']:
#                         Partner.phone = oldPartner['phone']
#                     if Partner.mobile != oldPartner['mobile']:
#                         Partner.mobile = oldPartner['mobile']
#                     if Partner.email != oldPartner['email']:
#                         Partner.email = oldPartner['email']
#                     if Partner.website != oldPartner['website']:
#                         Partner.website = oldPartner['website']
#                     if Partner.comment != oldPartner['comment']:
#                         Partner.comment = oldPartner['comment']
#                     if Partner.vat_hu != oldPartner['vat_hu']:
#                         Partner.vat_hu = oldPartner['vat_hu']
#                     if Partner.vat != oldPartner['vat']:
#                         Partner.vat = oldPartner['vat']
#                     if Partner.reg_number != oldPartner['reg_number']:
#                         Partner.reg_number = oldPartner['reg_number']
#                     if Partner.create_date != oldPartner['create_date']:
#                         Partner.create_date = oldPartner['create_date']
#                     if Partner.write_date != oldPartner['write_date']:
#                         Partner.write_date = oldPartner['write_date']
#                 else:
#                     vals = {
#                         'company_id': COMPANY_ID,
#                         'old_id': oldPartner['id'],
#                         'name': oldPartner['name'],
#                         'active': oldPartner['active'],
#                         'customer_rank': oldPartner['customer'],
#                         'supplier_rank': oldPartner['supplier'],
#                         'employee': oldPartner['employee'],
#                         'type': oldPartner['type'],
#                         'street': oldPartner['street'],
#                         'street2': oldPartner['street2'],
#                         'city': oldPartner['city'],
#                         'zip': oldPartner['zip'],
#                         'phone': oldPartner['phone'],
#                         'mobile': oldPartner['mobile'],
#                         'email': oldPartner['email'],
#                         'website': oldPartner['website'],
#                         'vat_hu': oldPartner['vat_hu'],
#                         'vat': oldPartner['vat'],
#                         'reg_number': oldPartner['reg_number'],
#                         'create_date': oldPartner['create_date'],
#                         'write_date': oldPartner['write_date'],
#                     }
#                     if x == 1:
#                         vals['is_company'] = True
#                     else:
#                         vals['is_company'] = False
#                     if ParentId:
#                         vals['parent_id'] = ParentId.id
#                     self.env['res.partner'].create(vals)
#         _logger.info("== END Guru Partner ==")
#         
#         # project.task
#         _logger.info("== START Guru Task ==")
#         for oldTask in models.execute_kw(db, uid, password, 'project.task', 'search_read', [   , ['id', '>', 0]]],
#             {'fields': [
#                 'id',
#                 'name',
#                 'project_id',
#                 'stage_id',
#                 'sequence',
#                 'create_date',
#                 'write_date',
#                 'partner_id',
#                 'next_step',
#                 'invoice_plan_date',
#                 'weekly_notofy_emails',
#                 'user_id',
#                 'requesting_partner_id',
#                 'consultant',
#                 'inspector',
#                 'estimated_price',
#                 'control',
#                 'bidding_deadline',
#                 'invoice_partial_plan_date',
#                 'nops',
#                 'notsdtp',
#                 'noooe',
#                 'notsitp',
#                 'server_link',
#                 'procedure',
#                 'procedure_type_id',
#                 'kff_task',
#                 'registration_code',
#                 'order_send_date',
#                 'kff_identification',
#                 'contact',
#                 'proceedings_type',
#                 'expert_date',
#                 'document',
#                 'expert_sent',
#                 'foureyes_sent',
#                 'kff_desc',
#                 'kff_guru_deadline',
#                 'date_deadline',
#                 'sent_kff_guru_notify_3',
#                 'description',
#                 'bid_validity_expires',
#                 'sent_bid_validity_expires_3',
#                 'sent_bid_validity_expires_7',
#                 'trainee_task',
#                 'scheduled_date_of_contract',
#                 'kmok_responsible',
#                 'kmok_state',
#                 'kmok_recent_act',
#                 'kmok_next_act',
#                 'pr_task',
#                 'kef',
#                 'date1_date',
#                 'date2_date',
#                 'date3_date',
#                 'date4_date',
#                 'date5_date',
#                 'date6_date',
#                 'date7_date',
#                 'date8_date',
#                 'date9_date',
#                 'date10_date',
#                 'date11_date',
#                 'date12_date',
#                 'date13_date',
#                 'date14_date',
#                 'date15_date',
#                 'date17_date',
#                 'date18_date',
#                 'date19_date',
#                 'date20_date',
#                 'date21_date',
#                 'date22_date',
#                 'date23_date',
#                 'date24_date',
#                 'date25_date',
#                 'date26_date',
#                 'date27_date',
#                 'date28_date',
#                 'date29_date',
#             ]}):
#             Task = self.env['project.task'].search([('company_id', '=', COMPANY_ID), ('old_id', '=', oldTask['id'])])
#             if oldTask['partner_id']:
#                 Partner = self.env['res.partner'].search([('company_id', '=', COMPANY_ID), ('old_id', '=', oldTask['partner_id'][0])], limit=1)
#             else:
#                 Partner = None
#             if oldTask['requesting_partner_id']:
#                 RequestingPartner = self.env['res.partner'].search([('company_id', '=', COMPANY_ID), ('old_id', '=', oldTask['requesting_partner_id'][0])], limit=1)
#             else:
#                 RequestingPartner = None
#             if oldTask['user_id']:
#                 UserId = self.env['res.users'].search([('old_id', '=', oldTask['user_id'][0])], limit=1).id
#             else:
#                 UserId = None
#             if oldTask['consultant']:
#                 ConsultantId = self.env['res.users'].search([('old_id', '=', oldTask['consultant'][0])], limit=1).id
#             else:
#                 ConsultantId = None
#             if oldTask['inspector']:
#                 InspectorId = self.env['res.users'].search([('old_id', '=', oldTask['inspector'][0])], limit=1).id
#             else:
#                 InspectorId = None
#             if Task:
#                 if Task.name != oldTask['name']:
#                     Task.name = oldTask['name']
#                 if oldTask['project_id']:
#                     if Task.project_id.id != PROJECT_PROJECT[oldTask['project_id'][0]]:
#                         Task.project_id = PROJECT_PROJECT[oldTask['project_id'][0]]
#                 if Task.stage_id.id != PROJECT_TASK_TYPE[oldTask['stage_id'][0]]:
#                     Task.stage_id = PROJECT_TASK_TYPE[oldTask['stage_id'][0]]
#                 if Task.sequence != oldTask['sequence']:
#                     Task.sequence = oldTask['sequence']
#                 if Task.create_date != oldTask['create_date']:
#                     Task.create_date = oldTask['create_date']
#                 if Task.write_date != oldTask['write_date']:
#                     Task.write_date = oldTask['write_date']
#                 if Partner:
#                     if Task.partner_id.id != Partner.id:
#                         Task.partner_id = Partner.id
#                 if Task.next_step != oldTask['next_step']:
#                     Task.next_step = oldTask['next_step']
#                 if Task.invoice_plan_date != oldTask['invoice_plan_date']:
#                     Task.invoice_plan_date = oldTask['invoice_plan_date']
#                 if Task.weekly_notofy_emails != oldTask['weekly_notofy_emails']:
#                     Task.weekly_notofy_emails = oldTask['weekly_notofy_emails']
#                 if Task.user_id.id != UserId:
#                     Task.user_id = UserId
#                 if RequestingPartner:
#                     if Task.requesting_partner_id.id != RequestingPartner.id:
#                         Task.requesting_partner_id = RequestingPartner.id
#                 if ConsultantId:
#                     if Task.consultant.id != ConsultantId:
#                         Task.consultant = ConsultantId
#                 if InspectorId:
#                     if Task.inspector.id != InspectorId:
#                         Task.inspector = InspectorId
#                 if Task.estimated_price != oldTask['estimated_price']:
#                     Task.estimated_price = oldTask['estimated_price']
#                 if Task.control != oldTask['control']:
#                     Task.control = oldTask['control']
#                 if Task.bidding_deadline != oldTask['bidding_deadline']:
#                     Task.bidding_deadline = oldTask['bidding_deadline']
#                 if Task.invoice_partial_plan_date != oldTask['invoice_partial_plan_date']:
#                     Task.invoice_partial_plan_date = oldTask['invoice_partial_plan_date']
#                 if Task.nops != oldTask['nops']:
#                     Task.nops = oldTask['nops']
#                 if Task.notsdtp != oldTask['notsdtp']:
#                     Task.notsdtp = oldTask['notsdtp']
#                 if Task.noooe != oldTask['noooe']:
#                     Task.noooe = oldTask['noooe']
#                 if Task.notsitp != oldTask['notsitp']:
#                     Task.notsitp = oldTask['notsitp']
#                 if Task.server_link != oldTask['server_link']:
#                     Task.server_link = oldTask['server_link']
#                 if Task.procedure != oldTask['procedure']:
#                     Task.procedure = oldTask['procedure']
#                 if oldTask['procedure_type_id']:
#                     if Task.procedure_type_id.id != oldTask['procedure_type_id'][0]:
#                         Task.procedure_type_id = oldTask['procedure_type_id'][0] # TODO
#                 if Task.kff_task != oldTask['kff_task']:
#                     Task.kff_task = oldTask['kff_task']
#                 if Task.registration_code != oldTask['registration_code']:
#                     Task.registration_code = oldTask['registration_code']
#                 if Task.order_send_date != oldTask['order_send_date']:
#                     Task.order_send_date = oldTask['order_send_date']
#                 if Task.kff_identification != oldTask['kff_identification']:
#                     Task.kff_identification = oldTask['kff_identification']
#                 if Task.contact != oldTask['contact']:
#                     Task.contact = oldTask['contact']
#                 if Task.proceedings_type != oldTask['proceedings_type']:
#                     Task.proceedings_type = oldTask['proceedings_type']
#                 if Task.expert_date!= oldTask['expert_date']:
#                     Task.expert_date = oldTask['expert_date']
#                 if Task.document != oldTask['document']:
#                     Task.document = oldTask['document']
#                 if Task.expert_sent != oldTask['expert_sent']:
#                     Task.expert_sent = oldTask['expert_sent']
#                 if Task.foureyes_sent != oldTask['foureyes_sent']:
#                     Task.foureyes_sent = oldTask['foureyes_sent']
#                 if Task.kff_desc != oldTask['kff_desc']:
#                     Task.kff_desc = oldTask['kff_desc']
#                 if Task.kff_guru_deadline != oldTask['kff_guru_deadline']:
#                     Task.kff_guru_deadline = oldTask['kff_guru_deadline']
#                 if Task.date_deadline != oldTask['date_deadline']:
#                     Task.date_deadline = oldTask['date_deadline']
#                 if Task.sent_kff_guru_notify_3 != oldTask['sent_kff_guru_notify_3']:
#                     Task.sent_kff_guru_notify_3 = oldTask['sent_kff_guru_notify_3']
#                 if Task.description != oldTask['description']:
#                     Task.description = oldTask['description']
#                 if Task.bid_validity_expires != oldTask['bid_validity_expires']:
#                     Task.bid_validity_expires = oldTask['bid_validity_expires']
#                 if Task.sent_bid_validity_expires_3 != oldTask['sent_bid_validity_expires_3']:
#                     Task.sent_bid_validity_expires_3 = oldTask['sent_bid_validity_expires_3']
#                 if Task.sent_bid_validity_expires_7 != oldTask['sent_bid_validity_expires_7']:
#                     Task.sent_bid_validity_expires_7 = oldTask['sent_bid_validity_expires_7']
#                 if Task.trainee_task != oldTask['trainee_task']:
#                     Task.trainee_task = oldTask['trainee_task']
#                 if Task.scheduled_date_of_contract != oldTask['scheduled_date_of_contract']:
#                     Task.scheduled_date_of_contract = oldTask['scheduled_date_of_contract']
#                 if Task.kmok_responsible != oldTask['kmok_responsible']:
#                     Task.kmok_responsible = oldTask['kmok_responsible']
#                 if oldTask['kmok_state']:
#                     if Task.kmok_state.id != oldTask['kmok_state'][0]:
#                         Task.kmok_state = oldTask['kmok_state'][0]
#                 if Task.kmok_recent_act != oldTask['kmok_recent_act']:
#                     Task.kmok_recent_act = oldTask['kmok_recent_act']
#                 if Task.kmok_next_act != oldTask['kmok_next_act']:
#                     Task.kmok_next_act = oldTask['kmok_next_act']
#                 if Task.pr_task != oldTask['pr_task']:
#                     Task.pr_task = oldTask['pr_task']
#                 if Task.kef != oldTask['kef']:
#                     Task.kef = oldTask['kef']
#                 if Task.date1_date != oldTask['date1_date']:
#                     Task.date1_date = oldTask['date1_date']
#                 if Task.date2_date != oldTask['date2_date']:
#                     Task.date2_date = oldTask['date2_date']
#                 if Task.date3_date != oldTask['date3_date']:
#                     Task.date3_date = oldTask['date3_date']
#                 if Task.date4_date != oldTask['date4_date']:
#                     Task.date4_date = oldTask['date4_date']
#                 if Task.date5_date != oldTask['date5_date']:
#                     Task.date5_date = oldTask['date5_date']
#                 if Task.date6_date != oldTask['date6_date']:
#                     Task.date6_date = oldTask['date6_date']
#                 if Task.date7_date != oldTask['date7_date']:
#                     Task.date7_date = oldTask['date7_date']
#                 if Task.date8_date != oldTask['date8_date']:
#                     Task.date8_date = oldTask['date8_date']
#                 if Task.date9_date != oldTask['date9_date']:
#                     Task.date9_date = oldTask['date9_date']
#                 if Task.date10_date != oldTask['date10_date']:
#                     Task.date10_date = oldTask['date10_date']
#                 if Task.date11_date != oldTask['date11_date']:
#                     Task.date11_date = oldTask['date11_date']
#                 if Task.date12_date != oldTask['date12_date']:
#                     Task.date12_date = oldTask['date12_date']
#                 if Task.date13_date != oldTask['date13_date']:
#                     Task.date13_date = oldTask['date13_date']
#                 if Task.date14_date != oldTask['date14_date']:
#                     Task.date14_date = oldTask['date14_date']
#                 if Task.date15_date != oldTask['date15_date']:
#                     Task.date15_date = oldTask['date15_date']
#                 if Task.date17_date != oldTask['date17_date']:
#                     Task.date17_date = oldTask['date17_date']
#                 if Task.date18_date != oldTask['date18_date']:
#                     Task.date18_date = oldTask['date18_date']
#                 if Task.date19_date != oldTask['date19_date']:
#                     Task.date19_date = oldTask['date19_date']
#                 if Task.date20_date != oldTask['date20_date']:
#                     Task.date20_date = oldTask['date20_date']
#                 if Task.date21_date != oldTask['date21_date']:
#                     Task.date21_date = oldTask['date21_date']
#                 if Task.date22_date != oldTask['date22_date']:
#                     Task.date22_date = oldTask['date22_date']
#                 if Task.date23_date != oldTask['date23_date']:
#                     Task.date23_date = oldTask['date23_date']
#                 if Task.date24_date != oldTask['date24_date']:
#                     Task.date24_date = oldTask['date24_date']
#                 if Task.date25_date != oldTask['date25_date']:
#                     Task.date25_date = oldTask['date25_date']
#                 if Task.date26_date != oldTask['date26_date']:
#                     Task.date26_date = oldTask['date26_date']
#                 if Task.date27_date != oldTask['date27_date']:
#                     Task.date27_date = oldTask['date27_date']
#                 if Task.date28_date != oldTask['date28_date']:
#                     Task.date28_date = oldTask['date28_date']
#                 if Task.date29_date != oldTask['date29_date']:
#                     Task.date29_date = oldTask['date29_date']
#             else:
#                 vals = {
#                     'company_id': COMPANY_ID,
#                     'old_id': oldTask['id'],
#                     'name': oldTask['name'],
#                     'stage_id': PROJECT_TASK_TYPE[oldTask['stage_id'][0]],
#                     'sequence': oldTask['sequence'],
#                     'create_date': oldTask['create_date'],
#                     'write_date': oldTask['write_date'],
#                     'next_step': oldTask['next_step'],
#                     'invoice_plan_date': oldTask['invoice_plan_date'],
#                     'weekly_notofy_emails': oldTask['weekly_notofy_emails'],
#                     'user_id': UserId,
#                     'estimated_price': oldTask['estimated_price'],
#                     'control': oldTask['control'],
#                     'bidding_deadline': oldTask['bidding_deadline'],
#                     'invoice_partial_plan_date': oldTask['invoice_partial_plan_date'],
#                     'nops': oldTask['nops'],
#                     'notsdtp': oldTask['notsdtp'],
#                     'noooe': oldTask['noooe'],
#                     'notsitp': oldTask['notsitp'],
#                     'server_link': oldTask['server_link'],
#                     'procedure': oldTask['procedure'],
#                     'kff_task': oldTask['kff_task'],
#                     'registration_code': oldTask['registration_code'],
#                     'order_send_date': oldTask['order_send_date'],
#                     'kff_identification': oldTask['kff_identification'],
#                     'contact': oldTask['contact'],
#                     'proceedings_type': oldTask['proceedings_type'],
#                     'expert_date': oldTask['expert_date'],
#                     'document': oldTask['document'],
#                     'expert_sent': oldTask['expert_sent'],
#                     'foureyes_sent': oldTask['foureyes_sent'],
#                     'kff_desc': oldTask['kff_desc'],
#                     'kff_guru_deadline': oldTask['kff_guru_deadline'],
#                     'date_deadline': oldTask['date_deadline'],
#                     'sent_kff_guru_notify_3': oldTask['sent_kff_guru_notify_3'],
#                     'description': oldTask['description'],
#                     'bid_validity_expires': oldTask['bid_validity_expires'],
#                     'sent_bid_validity_expires_3': oldTask['sent_bid_validity_expires_3'],
#                     'sent_bid_validity_expires_7': oldTask['sent_bid_validity_expires_7'],
#                     'trainee_task': oldTask['trainee_task'],
#                     'scheduled_date_of_contract': oldTask['scheduled_date_of_contract'],
#                     'kmok_responsible': oldTask['kmok_responsible'],
#                     'kmok_recent_act': oldTask['kmok_recent_act'],
#                     'kmok_next_act': oldTask['kmok_next_act'],
#                     'pr_task': oldTask['pr_task'],
#                     'kef': oldTask['kef'],
#                     'date1_date': oldTask['date1_date'],
#                     'date2_date': oldTask['date2_date'],
#                     'date3_date': oldTask['date3_date'],
#                     'date4_date': oldTask['date4_date'],
#                     'date5_date': oldTask['date5_date'],
#                     'date6_date': oldTask['date6_date'],
#                     'date7_date': oldTask['date7_date'],
#                     'date8_date': oldTask['date8_date'],
#                     'date9_date': oldTask['date9_date'],
#                     'date10_date': oldTask['date10_date'],
#                     'date11_date': oldTask['date11_date'],
#                     'date12_date': oldTask['date12_date'],
#                     'date13_date': oldTask['date13_date'],
#                     'date14_date': oldTask['date14_date'],
#                     'date15_date': oldTask['date15_date'],
#                     'date17_date': oldTask['date17_date'],
#                     'date18_date': oldTask['date18_date'],
#                     'date19_date': oldTask['date19_date'],
#                     'date20_date': oldTask['date20_date'],
#                     'date21_date': oldTask['date21_date'],
#                     'date22_date': oldTask['date22_date'],
#                     'date23_date': oldTask['date23_date'],
#                     'date24_date': oldTask['date24_date'],
#                     'date25_date': oldTask['date25_date'],
#                     'date26_date': oldTask['date26_date'],
#                     'date27_date': oldTask['date27_date'],
#                     'date28_date': oldTask['date28_date'],
#                     'date29_date': oldTask['date29_date'],
# }
#                 if oldTask['project_id']:
#                     vals['project_id'] = PROJECT_PROJECT[oldTask['project_id'][0]]
#                 if Partner:
#                     vals['partner_id'] = Partner.id
#                 if RequestingPartner:
#                     vals['requesting_partner_id'] = RequestingPartner.id
#                 if ConsultantId:
#                     vals['consultant'] = ConsultantId
#                 if InspectorId:
#                     vals['inspector'] = InspectorId
#                 if oldTask['procedure_type_id']:
#                     vals['procedure_type_id'] = oldTask['procedure_type_id'][0]
#                 if oldTask['kmok_state']:
#                     vals['kmok_state'] = oldTask['kmok_state'][0]
#                 self.env['project.task'].create(vals)
#         _logger.info("== END Guru Task ==")
# 
#         # project.task.progress
#         _logger.info("== START Guru Tevékenységek ==")
#         for oldProgress in models.execute_kw(db, uid, password, 'project.task.progress', 'search_read', [[['id', '>', 0]]],
#             {'fields': ['id', 'name', 'task_id', 'date', 'create_date', 'write_date']}):
#             Progress = self.env['project.task.progress'].search([('company_id', '=', COMPANY_ID), ('old_id', '=', oldProgress['id'])])
#             if Progress:
#                 if Progress.name != oldProgress['name']:
#                     Progress.name = oldProgress['name']
#                 if Progress.date != oldProgress['date']:
#                     Progress.date = oldProgress['date']
#                 if Progress.create_date != oldProgress['create_date']:
#                     Progress.create_date = oldProgress['create_date']
#                 if Progress.write_date != oldProgress['write_date']:
#                     Progress.write_date = oldProgress['write_date']
#             else:
#                 vals = {
#                     'company_id': COMPANY_ID,
#                     'old_id': oldProgress['id'],
#                     'name': oldProgress['name'],
#                     'task_id': self.env['project.task'].search([('company_id', '=', COMPANY_ID), ('old_id', '=', oldProgress['task_id'][0])], limit=1).id,
#                     'date': oldProgress['date'],
#                     'create_date': oldProgress['create_date'],
#                     'write_date': oldProgress['write_date'],
#                 }
#                 if vals['task_id']:
#                     self.env['project.task.progress'].create(vals)
#         _logger.info("== END Guru Tevékenységek ==")
#         
#         # account.analytic.line
#         _logger.info("== START Guru Munkaidő-beosztás ==")
#         for oldLine in models.execute_kw(db, uid, password, 'account.analytic.line', 'search_read', [[['project_id', 'not in', [12, 14]], ['project_id', '!=', False]]],
#             {'fields': ['id', 'name', 'date', 'user_id', 'task_id', 'project_id', 'employee_id', 'unit_amount', 'create_date', 'write_date', 'coa', 'foreign_language', 'include_in_customer', 'include_in_colleaggue']}):
#             Line = self.env['account.analytic.line'].search([('company_id', '=', COMPANY_ID), ('old_id', '=', oldLine['id'])])
#             if Line:
#                 pass
#                 # TODO
#             else:
#                 vals = {
#                     'company_id': COMPANY_ID,
#                     'old_id': oldLine['id'],
#                     'name': oldLine['name'],
#                     'date': oldLine['date'],
#                     'project_id': PROJECT_PROJECT[oldLine['project_id'][0]],
#                     'account_id': self.env['project.project'].search([('id', '=', PROJECT_PROJECT[oldLine['project_id'][0]])], limit=1).analytic_account_id.id,
#                     'unit_amount': oldLine['unit_amount'],
#                     'create_date': oldLine['create_date'],
#                     'write_date': oldLine['write_date'],
#                     'coa': oldLine['coa'],
#                     'foreign_language': oldLine['foreign_language'],
#                     'include_in_customer': oldLine['include_in_customer'],
#                     'include_in_colleaggue': oldLine['include_in_colleaggue'],
#                 }
#                 if oldLine['task_id']:
#                     vals['task_id'] = self.env['project.task'].search([('company_id', '=', COMPANY_ID), ('old_id', '=', oldLine['task_id'][0])], limit=1).id
#                 if oldLine['employee_id']:
#                     vals['employee_id'] = EMPLOYEE[oldLine['employee_id'][0]]
#                 if oldLine['user_id']:
#                     vals['user_id'] = self.env['res.users'].search([('old_id', '=', oldLine['user_id'][0])], limit=1).id
#                 self.env['account.analytic.line'].create(vals)
#         _logger.info("== END Guru Munkaidő-beosztás ==")
# 
#         # hr.employee.wage
#         _logger.info("== START Guru Employee Wage ==")
#         for oldWage in models.execute_kw(db, uid, password, 'hr.employee.wage', 'search_read', [[['id', '>', 0]]],
#              {'fields': [
#                  'id',
#                  'employee_id',
#                  'date',
#                  'state',
#                  'sum',
#                  'currency_id',
#                  'accounting_period_start',
#                  'accounting_period_end',
#                  'previous_sum',
#                  'grand_total',
#                  'basic_wage',
#                  'payable',
#                  'next_base',
#                  'active',
#                  'create_date',
#                  'write_date',
#                  ]}):
#             Wage = self.env['hr.employee.wage'].search([('old_id', '=', oldWage['id'])], limit=1)
#             if Wage:
#                 pass
#                 # TODO
#             else:
#                 vals = {
#                     'company_id': COMPANY_ID,
#                     'old_id': oldWage['id'],
#                     'employee_id': EMPLOYEE[oldWage['employee_id'][0]],
#                     'date': oldWage['date'],
#                     'state': oldWage['state'],
#                     'sum': oldWage['sum'],
#                     'currency_id': oldWage['currency_id'],
#                     'accounting_period_start': oldWage['accounting_period_start'],
#                     'accounting_period_end': oldWage['accounting_period_end'],
#                     'previous_sum': oldWage['previous_sum'],
#                     'grand_total': oldWage['grand_total'],
#                     'basic_wage': oldWage['basic_wage'],
#                     'payable': oldWage['payable'],
#                     'next_base': oldWage['next_base'],
#                     'active': oldWage['active'],
#                     'create_date': oldWage['create_date'],
#                     'write_date': oldWage['write_date'],
#                 }
#                 self.env['hr.employee.wage'].create(vals)
#         _logger.info("== END Guru Employee Wage ==")

        # project.task.meeting.log
        _logger.info("== START Guru Meeting Log ==")
        for oldLog in models.execute_kw(db, uid, password, 'project.task.meeting.log', 'search_read', [[['id', '>', 0]]],
             {'fields': [
                 'task_id',
                 'name',
                 'date',
                 'file1',
                 ]}):
            Log = self.env['project.task.meeting.log'].search([('old_id', '=', oldLog['id'])], limit=1)
            if Log:
                pass
                # TODO
            else:
                vals = {
                    'company_id': COMPANY_ID,
                    'old_id': oldLog['id'],
                    'task_id': self.env['project.task'].search([('company_id', '=', COMPANY_ID), ('old_id', '=', oldLog['task_id'][0])], limit=1).id,
                    'name': oldLog['name'],
                    'date': oldLog['date'],
                }
                if oldLog['file1']:
                    vals['file1'] = oldLog['file1']
                self.env['project.task.meeting.log'].create(vals)
        _logger.info("== STOP Guru Meeting Log ==")

        # project.task.wage
        _logger.info("== START Guru Task Wage ==")
        for oldWage in models.execute_kw(db, uid, password, 'project.task.wage', 'search_read', [[['id', '>', 0]]],
             {'fields': [
                 'task_id',
                 'project_id',
                 'user_id',
                 'state',
                 'wage',
                 'amount',
                 'date_set',
                 'date_accounted',
                 'meeting_log_id',
                 'comment',
                 'employee_wage_id',
                 'aal_id',
                 'create_date',
                 'write_date',
                 ]}):
            Wage = self.env['project.task.wage'].search([('old_id', '=', oldWage['id'])], limit=1)
            if Wage:
                pass
                # TODO
            else:
                vals = {
                    'company_id': COMPANY_ID,
                    'old_id': oldWage['id'],
                    'user_id': self.env['res.users'].search([('old_id', '=', oldWage['user_id'][0])], limit=1).id,
                    'state': oldWage['state'],
                    'wage': oldWage['wage'],
                    'amount': oldWage['amount'],
                    'date_set': oldWage['date_set'],
                    'date_accounted': oldWage['date_accounted'],
                    'comment': oldWage['comment'],
                    'create_date': oldWage['create_date'],
                    'write_date': oldWage['write_date'],
                }
                if oldWage['meeting_log_id']:
                    vals['meeting_log_id'] = self.env['project.task.meeting.log'].search([('old_id', '=', oldWage['meeting_log_id'][0])], limit=1).id
                if oldWage['aal_id']:
                    vals['aal_id'] = self.env['account.analytic.line'].search([('old_id', '=', oldWage['aal_id'][0])], limit=1).id
                if oldWage['task_id']:
                    vals['task_id'] = self.env['project.task'].search([('company_id', '=', COMPANY_ID), ('old_id', '=', oldWage['task_id'][0])], limit=1).id
                if oldWage['project_id']:
                    vals['project_id'] = PROJECT_PROJECT[oldWage['project_id'][0]]
                if oldWage['employee_wage_id']:
                    vals['employee_wage_id'] = self.env['hr.employee.wage'].search([('old_id', '=', oldWage['employee_wage_id'][0])], limit=1).id
                self.env['project.task.wage'].create(vals)
        _logger.info("== END Guru Task Wage ==")





    def load_from_kozbeszguru_files(self):
        _logger.info('===== load_from_kozbeszguru_files =====')
        
        # Server variables
        url = 'https://www.kozbeszguru.hu'
        db = 'kozbeszguru_odoo'
        username = 'odoosupport@eyssen.hu'
        password = 'tihvax-perhis-zItqa1'
        
        # Server Check
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), context=ssl._create_unverified_context())
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), context=ssl._create_unverified_context())
        
        # Constants
        COMPANY_ID = 2

        # project.task
        _logger.info("== START Guru Task Files ==")
        for oldTask in models.execute_kw(db, uid, password, 'project.task', 'search_read', [[['project_id', 'not in', [12, 14]], ['id', '>', 0]]],
            {'fields': [
                'date2_file1',
                'date3_file1',
                'date4_file1',
                'date7_file1',
                'date9_file1',
                'date10_file1',
                'date11_file1',
                'date12_file1',
                'date13_file1',
                'date14_file1',
                'date15_file1',
                'date21_file1',
                'date22_file1',
                'date23_file1',
                'date24_file1',
            ]}):
            Task = self.env['project.task'].search([('company_id', '=', COMPANY_ID), ('old_id', '=', oldTask['id'])])
            if Task:
                if not Task.date2_file1 and oldTask['date2_file1']:
                    Task.date2_file1 = oldTask['date2_file1']
                if not Task.date3_file1 and oldTask['date3_file1']:
                    Task.date3_file1 = oldTask['date3_file1']
                if not Task.date4_file1 and oldTask['date4_file1']:
                    Task.date4_file1 = oldTask['date4_file1']
                if not Task.date7_file1 and oldTask['date7_file1']:
                    Task.date7_file1 = oldTask['date7_file1']
                if not Task.date9_file1 and oldTask['date9_file1']:
                    Task.date9_file1 = oldTask['date9_file1']
                if not Task.date10_file1 and oldTask['date10_file1']:
                    Task.date10_file1 = oldTask['date10_file1']
                if not Task.date11_file1 and oldTask['date11_file1']:
                    Task.date11_file1 = oldTask['date11_file1']
                if not Task.date12_file1 and oldTask['date12_file1']:
                    Task.date12_file1 = oldTask['date12_file1']
                if not Task.date13_file1 and oldTask['date13_file1']:
                    Task.date13_file1 = oldTask['date13_file1']
                if not Task.date14_file1 and oldTask['date14_file1']:
                    Task.date14_file1 = oldTask['date14_file1']
                if not Task.date15_file1 and oldTask['date15_file1']:
                    Task.date15_file1 = oldTask['date15_file1']
                if not Task.date21_file1 and oldTask['date21_file1']:
                    Task.date21_file1 = oldTask['date21_file1']
                if not Task.date22_file1 and oldTask['date22_file1']:
                    Task.date22_file1 = oldTask['date22_file1']
                if not Task.date23_file1 and oldTask['date23_file1']:
                    Task.date23_file1 = oldTask['date23_file1']
                if not Task.date24_file1 and oldTask['date24_file1']:
                    Task.date24_file1 = oldTask['date24_file1']

        _logger.info("== END Guru Task Files ==")





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





class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'
    
    
    old_id = fields.Integer(u'Régi Odoo azonosító')





class HrEmployeeWage(models.Model):
    
    _inherit = 'hr.employee.wage'
    
    
    old_id = fields.Integer(u'Régi Odoo azonosító')





class ProjectTaskWage(models.Model):
    
    _inherit = 'project.task.wage'
    
    
    old_id = fields.Integer(u'Régi Odoo azonosító')





class ProjectTaskMeetingLog(models.Model):
    
    _inherit = 'project.task.meeting.log'

    
    old_id = fields.Integer(u'Régi Odoo azonosító')
