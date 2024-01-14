from odoo import api, fields, models, _
from odoo.exceptions import AccessError, ValidationError, UserError, MissingError

class Posts(models.Model):
    _name = "posts"
    _description = "Posts clone from website"
    _rec_name = 'title'

    url = fields.Char(string='Url')
    title = fields.Char(string='Title')
    sourcing_id = fields.Many2one('sourcing.sites', string='Sourcing Site')
    post_line_ids = fields.One2many('post.line', 'post_id', String="Data Fields")

    @api.model
    def act_pushing_posts(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _("Preview Post"),
            'res_model': 'preview.html',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {
                'default_content': 'abc'
            },
            'target': 'new'
        }

        return {
            'type': 'ir.actions.act_window',
            'name': _("Pushing Posts Confirm"),
            'res_model': 'pushing.posts.confirm',
            'view_mode': 'form',
            'views': [(self.env.ref('cms_wordpress.pushing_posts_confirm_popup').id, 'form')],
            'context': {},
            'target': 'new'
        }

    def action_preview_post(self):
        content = ''
        for line in self.post_line_ids:
            content += line.content + '\n'
        return {
            'type': 'ir.actions.act_window',
            'name': _("Preview Post"),
            'res_model': 'preview.html',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {
                'default_content': content
            },
            'target': 'new'
        }


class PostLine(models.Model):
    _name = "post.line"
    _description = "Lines of each Post"
    _rec_name = 'name'

    name = fields.Char(string='Name')
    content = fields.Text(string="Content")
    trailer_content = fields.Text(string="Content", compute='_compute_trailer_content', store=True)
    post_id = fields.Many2one('posts')

    def truncate_string(self, text):
        max_length = 50
        truncated_text = text[:max_length] + '...' if len(text) > max_length else text
        return truncated_text

    @api.depends('content')
    def _compute_trailer_content(self):
        for r in self:
            r.trailer_content = self.truncate_string(r.content)
