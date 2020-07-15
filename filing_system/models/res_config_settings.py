# -*- coding: utf-8 -*-

from odoo import api, fields, models, _





class ResConfigSettings(models.TransientModel):
    
    _inherit = 'res.config.settings'


    documents_filing_settings = fields.Boolean(related='company_id.documents_filing_settings', readonly=False,
                                                string="Filing")
    filing_folder = fields.Many2one('documents.folder', related='company_id.filing_folder', readonly=False,
                                     string="filing default workspace")
    filing_tags = fields.Many2many('documents.tag', 'filing_tags_table',
                                    related='company_id.filing_tags', readonly=False,
                                    string="Filing Tags")

    @api.onchange('filing_folder')
    def on_filing_folder_change(self):
        if self.filing_folder != self.filing_tags.mapped('folder_id'):
            self.filing_tags = False
