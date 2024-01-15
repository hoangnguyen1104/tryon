from odoo import api, fields, models, _
from odoo.exceptions import AccessError, ValidationError, UserError, MissingError

class TagCrawlWebsite(models.Model):
    _name = "tag.crawl.website"
    _description = "Tags element will be crawl"
    _rec_name = 'name'

    name = fields.Char(string='Name')
    description = fields.Html(string='Meaning')
