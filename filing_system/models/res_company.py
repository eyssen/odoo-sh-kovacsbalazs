# -*- coding: utf-8 -*-

from odoo import fields, models, api, _





class ResCompany(models.Model):

    _inherit = "res.company"


    def _domain_company(self):
        company = self.env.company
        return ['|', ('company_id', '=', False), ('company_id', '=', company)]

    documents_filing_settings = fields.Boolean()
    filing_folder = fields.Many2one('documents.folder', string="Filing Workspace", domain=_domain_company,
                                     default=lambda self: self.env.ref('documents.documents_internal_folder',
                                                                       raise_if_not_found=False))
    filing_tags = fields.Many2many('documents.tag', 'filing_tags_table')
