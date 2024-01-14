from odoo import api, fields, models


class XpathFieldLine(models.Model):
    _name = "xpath.fields.line"
    _description = "Save fields will crawl in website"
    _rec_name = 'name'

    name = fields.Char(string="Name")
    xpath = fields.Char(string="Xpath")
    state = fields.Boolean(string="Active", default=True)
    sourcing_id = fields.Many2one(string="Sourcing Site", comodel_name='sourcing.sites')
