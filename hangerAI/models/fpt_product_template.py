# -*- coding: utf-8 -*-

from odoo import api, fields, models
import os
import base64
import binascii
import io

from PIL import Image, ImageOps
try:
    from PIL.Image import Transpose, Palette, Resampling
except ImportError:
    Transpose = Palette = Resampling = Image

class ProductTemplate(models.Model):
    _inherit = "product.template"

    gender = fields.Selection([('male', 'Male'),
                              ('female', 'Female')], string='Giới tính')

    detailed_type = fields.Selection(selection_add=[
        ('model', 'Người mẫu'),
        ('upper', 'Áo'),
        ('lower', 'Quần')],
        ondelete={
            'model': 'set service',
            'upper': 'set service',
            'lower': 'set service',
        }
    )

    agonostic_v32 = fields.Binary()
    densepose = fields.Binary()
    parse_agonostic_v32 = fields.Binary()
    parse_v3 = fields.Binary()
    openpose_img = fields.Binary()
    openpose_json = fields.Binary()

    root_id = fields.Many2one('product.template')

    def _detailed_type_mapping(self):
        type_mapping = super()._detailed_type_mapping()
        type_mapping['model'] = 'service'
        type_mapping['cloth'] = 'service'
        return type_mapping

    def migrate_data(self):
        def get_from(model, folderName):
            key = model[:5]
            item_path = f"D:\\P.KTCN\\Try_on\\input\{folderName}"
            item_list = os.listdir(item_path)
            for item in item_list:
                if item.startswith(key):
                    path = os.path.join(item_path, item)
                    with open(path, 'rb') as image_file:
                        binary_data = image_file.read()
                        encoded_data = base64.b64encode(binary_data).decode('utf-8')
                        return encoded_data

        dem = 0

        # migrate model
        model_path = "D:\\P.KTCN\\Try_on\\input\\image"
        model_list = os.listdir(model_path)
        product = self.env['product.template']
        for model in model_list:
            # Check if the file is an image
            if model.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                dem += 1
                if dem == 1:
                    continue
                if dem > 100: break
                # Construct the full file path
                path = os.path.join(model_path, model)
                with open(path, 'rb') as image_file:
                    binary_data = image_file.read()
                    encoded_data = base64.b64encode(binary_data)
                    product.create({
                        'name': model[:5],
                        'detailed_type': 'model',
                        'image_1920': encoded_data,
                        'agonostic_v32': get_from(model,"agnostic-v3.2"),
                        'densepose': get_from(model,"image-densepose"),
                        'parse_agonostic_v32': get_from(model,"image-parse-agnostic-v3.2"),
                        'parse_v3': get_from(model,"image-parse-v3"),
                        'openpose_img': get_from(model,"openpose_img"),
                        'openpose_json': get_from(model,"openpose_json"),
                    })


