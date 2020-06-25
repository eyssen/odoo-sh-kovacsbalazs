# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from odoo.exceptions import AccessError

import logging
_logger = logging.getLogger(__name__)





class Digest(models.Model):
    
    _inherit = 'digest.digest'

    
    kpi_project_task_kozbesz_elokeszites = fields.Boolean(u'Előkészítés alatt lévő közbeszerzési eljárások')
    kpi_project_task_kozbesz_elokeszites_value = fields.Integer(compute='_compute_project_task_kozbesz_elokeszites_value')
    kpi_project_task_kozbesz_folyamatban = fields.Boolean(u'Folyamatban lévő közbeszerzési eljárások')
    kpi_project_task_kozbesz_folyamatban_value = fields.Integer(compute='_compute_project_task_kozbesz_folyamatban_value')
    kpi_project_task_kozbesz_lezart = fields.Boolean(u'Lezárt közbeszerzési eljárások')
    kpi_project_task_kozbesz_lezart_value = fields.Integer(compute='_compute_project_task_kozbesz_lezart_value')
    kpi_project_task_kff_folyamatban = fields.Boolean(u'Folyamatban lévő KFF ellenőrzések')
    kpi_project_task_kff_folyamatban_value = fields.Integer(compute='_compute_project_task_kff_folyamatban_value')
    kpi_project_task_kff_lezart = fields.Boolean(u'Lezárt KFF ellenőrzések')
    kpi_project_task_kff_lezart_value = fields.Integer(compute='_compute_project_task_kff_lezart_value')
    kpi_project_task_egyeb_folyamatban = fields.Boolean(u'Egyéb folyamatban lévő feladatok')
    kpi_project_task_egyeb_folyamatban_value = fields.Integer(compute='_compute_project_task_egyeb_folyamatban_value')
    

    def _compute_project_task_kozbesz_elokeszites_value(self):
        if not self.env.user.has_group('project.group_project_user'):
            raise AccessError(_("Do not have access, skip this data for user's digest email"))
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            record.kpi_project_task_kozbesz_elokeszites_value = self.env['project.task'].search_count([
                ('project_id', 'in', [2, 8]),
                ('stage_id', 'in', [17, 28]),
                ('create_date', '>=', start),
                ('create_date', '<', end),
                ('company_id', '=', company.id)
            ])
    

    def _compute_project_task_kozbesz_folyamatban_value(self):
        if not self.env.user.has_group('project.group_project_user'):
            raise AccessError(_("Do not have access, skip this data for user's digest email"))
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            record.kpi_project_task_kozbesz_folyamatban_value = self.env['project.task'].search_count([
                ('project_id', 'in', [2, 8]),
                ('stage_id', 'in', [11, 12, 13, 14, 15]),
                ('create_date', '>=', start),
                ('create_date', '<', end),
                ('company_id', '=', company.id)
            ])
    

    def _compute_project_task_kozbesz_lezart_value(self):
        if not self.env.user.has_group('project.group_project_user'):
            raise AccessError(_("Do not have access, skip this data for user's digest email"))
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            record.kpi_project_task_kozbesz_lezart_value = self.env['project.task'].search_count([
                ('project_id', 'in', [2, 8]),
                ('stage_id', 'in', [16]),
                ('create_date', '>=', start),
                ('create_date', '<', end),
                ('company_id', '=', company.id)
            ])
    

    def _compute_project_task_kff_folyamatban_value(self):
        if not self.env.user.has_group('project.group_project_user'):
            raise AccessError(_("Do not have access, skip this data for user's digest email"))
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            record.kpi_project_task_kff_folyamatban_value = self.env['project.task'].search_count([
                ('project_id', 'in', [6]),
                ('stage_id', 'in', [17, 30, 31, 33]),
                ('create_date', '>=', start),
                ('create_date', '<', end),
                ('company_id', '=', company.id)
            ])
    

    def _compute_project_task_kff_lezart_value(self):
        if not self.env.user.has_group('project.group_project_user'):
            raise AccessError(_("Do not have access, skip this data for user's digest email"))
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            record.kpi_project_task_kff_lezart_value = self.env['project.task'].search_count([
                ('project_id', 'in', [6]),
                ('stage_id', 'in', [16]),
                ('create_date', '>=', start),
                ('create_date', '<', end),
                ('company_id', '=', company.id)
            ])
    

    def _compute_project_task_egyeb_folyamatban_value(self):
        if not self.env.user.has_group('project.group_project_user'):
            raise AccessError(_("Do not have access, skip this data for user's digest email"))
        for record in self:
            start, end, company = record._get_kpi_compute_parameters()
            record.kpi_project_task_egyeb_folyamatban_value = self.env['project.task'].search_count([
                ('project_id', 'in', [7, 9, 10, 11, 13, 15]),
                ('stage_id', 'not in', [16, 23]),
                ('create_date', '>=', start),
                ('create_date', '<', end),
                ('company_id', '=', company.id)
            ])


    def compute_kpis_actions(self, company, user):
        res = super(Digest, self).compute_kpis_actions(company, user)
        res['kpi_project_task_kozbesz_elokeszites'] = 'project.open_view_project_all&menu_id=%s' % self.env.ref('project.menu_main_pm').id
        res['kpi_project_task_kozbesz_folyamatban'] = 'project.open_view_project_all&menu_id=%s' % self.env.ref('project.menu_main_pm').id
        res['kpi_project_task_kozbesz_lezart'] = 'project.open_view_project_all&menu_id=%s' % self.env.ref('project.menu_main_pm').id
        res['kpi_project_task_kff_folyamatban'] = 'project.open_view_project_all&menu_id=%s' % self.env.ref('project.menu_main_pm').id
        res['kpi_project_task_kff_lezart'] = 'project.open_view_project_all&menu_id=%s' % self.env.ref('project.menu_main_pm').id
        res['kpi_project_task_egyeb_folyamatban'] = 'project.open_view_project_all&menu_id=%s' % self.env.ref('project.menu_main_pm').id
        return res
