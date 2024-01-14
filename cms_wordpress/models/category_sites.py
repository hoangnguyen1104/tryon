
from odoo import api, fields, models


class SourcingSites(models.Model):
    _name = "category.sites"
    _description = "Category Sites"
    _rec_name = 'name'

    name = fields.Char(String="Name")
    description = fields.Html(string="Note")
