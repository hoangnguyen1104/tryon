from odoo import api, fields, models, _

class PreviewHtml(models.TransientModel):
    _name = 'preview.html'
    _description = 'Popup preview string html'

    content = fields.Text(string="Content")