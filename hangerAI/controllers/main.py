from urllib.parse import urlencode
from werkzeug.utils import send_file

import json
import logging
import requests
from io import BytesIO
from odoo import http
from odoo.http import Stream
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
        # model
        system_models = product_template.search([('detailed_type', '=', 'model'), ('create_uid', '=', 1)])
        user_models = product_template.search([('detailed_type', '=', 'model'), ('create_uid', '=', request.uid)])
        # upper
        system_uppers = product_template.search([('detailed_type', '=', 'upper'), ('create_uid', '=', 1)])
        user_uppers = product_template.search([('detailed_type', '=', 'upper'), ('create_uid', '=', request.uid)])
        # lower
        system_lowers = product_template.search([('detailed_type', '=', 'lower'), ('create_uid', '=', 1)])
        user_lowers = product_template.search([('detailed_type', '=', 'lower'), ('create_uid', '=', request.uid)])
        values = {
            'models': system_models,
            'user_models': user_models,
            'system_uppers': system_uppers,
            'user_uppers': user_uppers,
            'system_lowers': system_lowers,
            'user_lowers': user_lowers,
        }
        return request.render("hangerAI.hanger_try_on", values)

    @http.route([
        '/upscale-image',
    ], type='http', auth="public", website=True)
    def upscale_image(self, **kwargs):
        if kwargs.get('image_to_upscale'):
            values = {
                "default_image": kwargs.get('image_to_upscale').split(',')[1]
            }
        else:
            values = {}
        return request.render("hangerAI.hanger_upscale_image", values)

    @http.route([
        '/upscale',
    ], type='http', auth="public", website=True, csrf=False)
    def upscale(self, **kwargs):
        product_template = request.env['product.template'].sudo()
        if kwargs.get('image_to_upscale'):
            values = {
                "default_image": 1,
                "default_image_val": kwargs.get('image_to_upscale').split(',')[1],
                "images": product_template.search([], limit=10)
            }
        else:
            values = {
                "images": product_template.search([], limit=10),
                "default_image": 0
            }
        return request.render("hangerAI.hanger_upscale", values)

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
        type_gallery = kwargs.get('type-gallery')
        detailed_type = False
        if type_gallery == 'tops':
            detailed_type = 'upper'
        if type_gallery == 'bottoms':
            detailed_type = 'lower'

        import base64
        def encode_image_to_base64(file_storage):
            encoded_string = base64.b64encode(file_storage.read())
            return encoded_string.decode("utf-8")

        product = request.env['product.template']
        try:
            file = kwargs.get('image')
            new_model = product.create({
                'name': file.filename,
                'detailed_type': detailed_type,
                'image_1920': encode_image_to_base64(file)
            })
        except Exception as e:
            _logger.info("upload model fail")
            _logger.info(e)
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
        import base64
        import os
        import shutil
        def make_folder(folder, file, type_file, name_file):
            folder_path = 'D:\\test-try-on\\' + folder

            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
            os.makedirs(folder_path)

            # Set the file path including the folder path and file name with the .jpg extension
            file_path = os.path.join(folder_path, name_file + type_file)

            # Decode the binary data from base64
            decoded_data = base64.b64decode(file)

            # Open the file in binary write mode
            with open(file_path, 'wb') as file:
                # Write the binary data to the file
                file.write(decoded_data)

        product_template = request.env['product.template']
        model = product_template.browse(int(kwargs.get('model_id')))
        make_folder("agnostic-v3.2", model.agonostic_v32, ".jpg", model.name + "_00")
        make_folder("image", model.image_1920, ".jpg", model.name + "_00")
        make_folder("image-densepose", model.densepose, ".jpg", model.name + "_00")
        make_folder("image-parse-agnostic-v3.2", model.parse_agonostic_v32, ".png", model.name + "_00")
        make_folder("image-parse-v3", model.parse_v3, ".png", model.name + "_00")
        make_folder("openpose_img", model.openpose_img, ".png", model.name + "_00_rendered")
        make_folder("openpose_json", model.openpose_json, ".json", model.name + "_00_keypoints")
        make_folder("cloth", model.cloth_model, ".jpg", model.name + "_00")
        make_folder("cloth-mask", model.cloth_mask_model, ".jpg", model.name + "_00")

    @http.route([
        '/mkdir_cloth',
    ], type='http', auth="public", website=True, csrf=False)
    def mkdir_cloth(self, **kwargs):
        import base64
        import os
        import shutil
        def make_folder(folder, file, type_file, name_file):
            folder_path = 'D:\\test-try-on\\' + folder

            # Set the file path including the folder path and file name with the .jpg extension
            file_path = os.path.join(folder_path, name_file + type_file)

            # Decode the binary data from base64
            decoded_data = base64.b64decode(file)

            # Open the file in binary write mode
            with open(file_path, 'wb') as file:
                # Write the binary data to the file
                file.write(decoded_data)

        product_template = request.env['product.template']
        cloth = product_template.browse(int(kwargs.get('cloth_id')))
        model = product_template.browse(int(kwargs.get('model_id')))
        image_binary = base64.b64decode(cloth.image_1920)

        make_folder("cloth", cloth.image_1920, ".jpg", cloth.name + "_00")
        make_folder("cloth-mask", cloth.mask, ".jpg", cloth.name + "_00")

        url = 'http://127.0.0.1:5000/process_image'

        # Parameters for the request (image and cloth names)
        params = {
            'image': model.name,
            'cloth': cloth.name
        }

        # Make the POST request
        try:
            response = requests.post(url, params=params)
        except Exception as e:
            print(e)

        # Check the response status code
        if response.status_code == 200:
            # Request was successful
            byte_string = response.content
            string = byte_string.decode('utf-8')
            prefix = '{"files":"b\''
            suffix = "\'}\n"
            inner_string = string[len(prefix):-len(suffix)]
            image_data = base64.b64decode(inner_string[:-1])
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            response_data = {
                'image': image_base64,
                'content_type': 'image/jpeg',
                'filename': 'image.jpg'
            }
            return json.dumps(response_data)
        else:
            # Request failed
            print('Request failed with status code:', response.status_code)

        # Return the binary image data as the response
        response_data = {
            'image': base64.b64encode(image_binary).decode('utf-8'),
            'content_type': 'image/jpeg',
            'filename': 'image.jpg'
        }
        return json.dumps(response_data)

    @http.route([
        '/download_result',
    ], type='http', auth="public", website=True, csrf=False)
    def download_result(self, **kwargs):
        import base64
        kwargs.get('image_to_download')
        image_data = kwargs.get('image_to_download').split(',')[1]
        decoded_image_data = base64.b64decode(image_data)
        attachment_val = {
            'name': 'tryon_result',
            'datas': base64.b64encode(decoded_image_data),
            'type': 'binary',
        }
        attachment = request.env['ir.attachment'].sudo().create(attachment_val)
        return request.redirect('/web/content/%s?download=true' % attachment.id)
        
    @http.route([
        '/to_upscale',
    ], type='http', auth="public", website=True, csrf=False)
    def to_upscale(self, **kwargs):
        pass 
        return request.redirect('/upscale')
