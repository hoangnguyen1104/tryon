
import json
import logging
from datetime import datetime
from werkzeug.exceptions import Forbidden, NotFound
from werkzeug.urls import url_decode, url_encode, url_parse

from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.http import request
_logger = logging.getLogger(__name__)

class HangerAPI(http.Controller):
    @http.route([
        '/hanger',
    ], type='http', auth="public", website=True)
    def hanger(self, **post):
        product_template = request.env['product.template']
        top_models = product_template.search([('detailed_type', '=', 'model')], limit=12)
        top_cloths = product_template.search([('detailed_type', '=', 'model')], limit=12)
        values = {
            'top_models': top_models,
            'top_cloths': top_cloths
        }
        return request.render("hangerAI.hanger_dashboard", values)

    @http.route([
        '/try-on',
    ], type='http', auth="public", website=True)
    def try_on(self, **post):
        product_template = request.env['product.template'].sudo()
        system_models = product_template.search([('detailed_type', '=', 'model'), ('create_uid', '=', 1)], limit=20)
        user_models = product_template.search([('detailed_type', '=', 'model'), ('create_uid', '=', request.uid)], limit=20)
        cloths = product_template.search([('detailed_type', '=', 'cloth')], limit=60)
        values = {
            'models': system_models,
            'user_models': user_models,
            'cloths': cloths
        }
        return request.render("hangerAI.hanger_try_on", values)

    @http.route([
        '/upscale-image',
    ], type='http', auth="public", website=True)
    def upscale_image(self, **post):
        values = {}
        return request.render("hangerAI.hanger_upscale_image", values)

    @http.route(['/upload_model'], type='http', auth="user",
                website=True, csrf=False)
    def upload_model(self, **kwargs):
        import base64
        def encode_image_to_base64(file_storage):
            encoded_string = base64.b64encode(file_storage.read())
            return encoded_string.decode("utf-8")

        product = request.env['product.template']
        file = request.httprequest.files.getlist('upload_files')[0]
        try:
            new_model = product.create({
                'name': file.filename,
                'detailed_type': 'model',
                'image_1920': encode_image_to_base64(file)
            })
        except Exception as e:
            _logger.info("upload model fail")
            _logger.info(e)

    @http.route(['/upload_gallery'], type='http', auth="user",
                website=True, csrf=False)
    def upload_gallery(self, **kwargs):
        pass
        return request.redirect("/try-on")

    @http.route([
        '/tagging',
    ], type='http', auth="public", website=True)
    def hanger_tagging_image(self, **post):
        values = {}
        return request.render("hangerAI.hanger_tagging", values)

    @http.route([
        '/mkdir_model',
    ], type='http', auth="public", website=True, csrf=False)
    def mkdir_model(self, **kwargs):
        a = 1
        pass