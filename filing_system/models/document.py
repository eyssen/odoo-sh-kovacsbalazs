# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError





class FilingDocument(models.Model):
    
    _name = 'filing.document'
    _description = 'Filing Document'
    
    
    name = fields.Char(u'Tárgy', required=True)
    number = fields.Char(u'Iktatószám')
    mailbox_id = fields.Many2one('filing.mailbox', u'Postafiók neve')
    from_id = fields.Many2one('res.partner', u'Feladó')
    to_id = fields.Many2one('res.partner', u'Címzett')
    date = fields.Date(u'Időpont')
    description = fields.Text(u'Leírás')
    return_receipt = fields.Char(u'Tértivevény')


    _sql_constraints = [
        ('number_uniq', 'unique(number)', u'Filing Number must be unique!'),
    ]


    @api.onchange('mailbox_id')
    def _onchange_mailbox(self):
        if self.mailbox_id:
            if not self.from_id and not self.to_id:
                if self.mailbox_id.default_from_id:
                    self.from_id = self.mailbox_id.default_from_id
                if self.mailbox_id.default_to_id:
                    self.to_id = self.mailbox_id.default_to_id
    
    
    @api.model
    def create(self, vals):
        if not vals.get('number') and 'mailbox_id' in vals:
            vals['number'] = self.env['filing.mailbox'].browse(vals.get('mailbox_id')).sequence_id.next_by_id()
        return super(FilingDocument, self).create(vals)


    @api.model
    def write(self, vals):
        if not self.number and 'mailbox_id' in vals:
            self.number = self.env['filing.mailbox'].browse(vals.get('mailbox_id')).sequence_id.next_by_id()
        result = super(FilingDocument, self).write(vals)
        return result





class FilingMailbox(models.Model):
    
    _name = 'filing.mailbox'
    
    
    name = fields.Char(u'Postafiók neve', required=True)
    sequence_id = fields.Many2one('ir.sequence', u'Sorszám', required=True)
    default_from_id = fields.Many2one('res.partner', u'Alapértelmezett feladó')
    default_to_id = fields.Many2one('res.partner', u'Alapértelmezett címzett')
    qty = fields.Integer(u'Darabszám', readonly=True)





class IrAttachment(models.Model):
    
    _name = 'ir.attachment'
    _inherit = 'ir.attachment'


    def _set_folder_settings(self, vals):
        vals = super(IrAttachment, self)._set_folder_settings(vals)
        if vals.get('res_model') == 'filing.document' and self.env.user.company_id.dms_filing_settings and not vals.get('folder_id'):
            folder = self.env.user.company_id.filing_folder
            if folder.exists():
                vals.setdefault('folder_id', folder.id)
                vals.setdefault('tag_ids', [(6, 0, self.env.user.company_id.filing_tags.ids)])
        return vals
