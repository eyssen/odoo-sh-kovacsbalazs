# -*- coding: utf-8 -*-
from odoo import api, fields, models
from werkzeug.urls import url_encode

import logging
_logger = logging.getLogger(__name__)





class ProjectTask(models.Model):
    
    _inherit = 'project.task'
    
    
    project_name = fields.Char(u'Project name', related='project_id.name', readonly=True)
    next_step = fields.Char(u'Soron következő lépés')
    invoice_plan_date = fields.Date(u'Várható számlázási dátum')
    weekly_notofy_emails = fields.Char(u'Heti értesítés emailcímei')
    progress_ids = fields.One2many('project.task.progress', 'task_id', u'Tevékenységek')


    def get_share_url(self):
        self.ensure_one()
        params = {
            'model': self._name,
            'id': self.id,
        }
        if hasattr(self, 'access_token') and self.access_token:
            params['access_token'] = self.access_token
        if hasattr(self, 'partner_id') and self.partner_id:
            params.update(self.partner_id.signup_get_auth_param()[self.partner_id.id])

        return '/web#' + url_encode(params) + '&view_type=form'


    def task_weekly_notify(self):
        Tasks = self.env['project.task'].search([('weekly_notofy_emails', '!=', False), ('stage_id', 'in', [5])])
        for Task in Tasks:
            self.env.ref('kbl.notify_weekly').with_context().send_mail(Task.id, force_send=True)





class ProjectTaskProgress(models.Model):
    
    _name = 'project.task.progress'
    _order = 'task_id, date'


    name = fields.Char(u'Leírás', required=True)
    task_id = fields.Many2one('project.task', u'Feladat', required=True)
    date = fields.Date(u'Dátum', required=True)
