from odoo import api, fields, models, _
import requests
import json
import logging
import base64

_logger = logging.getLogger(__name__)

class PushingPostsConfirm(models.TransientModel):
    _name = 'pushing.posts.confirm'
    _description = 'Popup Confirm Before Pushing Posts'

    def _get_default_consuming_ids(self):
        if self.env.context.get('consuming_id'):
            consuming_id = self.env['consuming.sites'].browse(int(self.env.context.get('consuming_id')))
            return consuming_id.ids
        return False

    def _get_default_post_ids(self):
        return self.env.context.get('active_ids')

    consuming_ids = fields.Many2many('consuming.sites', string='Consuming Sites', default=_get_default_consuming_ids)
    post_ids = fields.Many2many('posts', default=_get_default_post_ids)

    def act_confirm_pushing(self):
        for post in self.post_ids:
            for consuming in self.consuming_ids:
                url = consuming.web_url + "/?rest_route=/wp/v2/posts"
                payload = json.dumps({
                    "title": post.data_title,
                    "status": "publish",
                    "content": post.data_content
                })
                _logger.info(payload)
                account = consuming.username + ":" + consuming.token
                encoded_bytes = base64.b64encode(account.encode('utf-8'))
                encoded_string = encoded_bytes.decode('utf-8')
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': "Basic " + encoded_string
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                _logger.info(response)

