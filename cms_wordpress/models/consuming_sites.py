from odoo import api, fields, models


class SourcingSites(models.Model):
    _name = "consuming.sites"
    _description = "Wordpress/Website to inject data posts"
    _rec_name = 'web_url'

    name = fields.Char(string="Name")
    web_url = fields.Char(String="Website Url")
    username = fields.Char(string="Username")
    token = fields.Char(string="Token")
    assign_ids = fields.Many2many('res.users', string="Assignee")

    def action_open_pushing(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Posts',
            'view_mode': 'tree',
            'view_id': self.env.ref('cms_wordpress.view_posts_tree').id,
            'res_model': 'posts',
            'domain': [],
            'context': {'consuming_id': self.id}
        }
