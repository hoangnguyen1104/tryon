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
        ('lower', 'Quần'),
        ('dress', 'Váy')
    ],
        ondelete={
            'model': 'set service',
            'upper': 'set service',
            'lower': 'set service',
            'dress': 'set service',
        }
    )
    # update
    type_model = fields.Char()
    cloth_align = fields.Binary()
    cloth_align_mask = fields.Binary()
    cloth_align_parse = fields.Binary()

    parse_bytedance = fields.Binary()
    pose_25 = fields.Binary()
    ####


    cloth_model = fields.Binary()
    cloth_mask_model = fields.Binary()

    agonostic_v32 = fields.Binary()
    densepose = fields.Binary()
    parse_agonostic_v32 = fields.Binary()
    parse_v3 = fields.Binary()
    openpose_img = fields.Binary()
    openpose_json = fields.Binary()
    mask = fields.Binary()

    root_id = fields.Many2one('product.template')

    def _detailed_type_mapping(self):
        type_mapping = super()._detailed_type_mapping()
        type_mapping['model'] = 'service'
        type_mapping['upper'] = 'service'
        type_mapping['lower'] = 'service'
        type_mapping['dress'] = 'service'
        return type_mapping

    def migrate_data(self):

        product_temp = self.env['product.template']
        miss_models = product_temp.sudo().search([('detailed_type', '=', 'model'), ('cloth_align', '=', False)])
        miss_models.unlink()
        return

        def get_from(model, folderName):
            key = model[:6]
            item_path = f"E:\\GP-VTON\\GP-VTON\\dataset\\Dresscode\\dresses\\{folderName}"
            item_list = os.listdir(item_path)
            for item in item_list:
                if item.startswith(key):
                    path = os.path.join(item_path, item)
                    with open(path, 'rb') as image_file:
                        binary_data = image_file.read()
                        encoded_data = base64.b64encode(binary_data).decode('utf-8')
                        return encoded_data

        # migrate model
        dem = 0
        model_path = "E:\\GP-VTON\\GP-VTON\\dataset\\Dresscode\\dresses\\image"
        model_list = os.listdir(model_path)
        product = self.env['product.template']
        for model in model_list:
            # Check if the file is an image
            if model.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                dem += 1
                if dem > 100: break
                # Construct the full file path
                path = os.path.join(model_path, model)
                with open(path, 'rb') as image_file:
                    binary_data = image_file.read()
                    encoded_data = base64.b64encode(binary_data)
                    product.create({
                        'name': model[:6],
                        'detailed_type': 'model',
                        'type_model': 'dress',
                        'image_1920': encoded_data,
                        'parse_bytedance': get_from(model,"parse-bytedance"),
                        'densepose': get_from(model,"densepose"),
                        'pose_25': get_from(model,"pose_25"),
                        'cloth_align': get_from(model,"cloth_align"),
                        'cloth_align_mask': get_from(model, "cloth_align_mask-bytedance"),
                        'cloth_align_parse': get_from(model, "cloth_align_parse-bytedance"),
                    })

        # migrate cloths
        dem = 0
        model_path = "E:\\GP-VTON\\GP-VTON\\dataset\\Dresscode\\dresses\\cloth_align"
        model_list = os.listdir(model_path)
        product = self.env['product.template']
        for model in model_list:
            # Check if the file is an image
            if model.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                dem += 1
                if dem > 100: break
                # Construct the full file path
                path = os.path.join(model_path, model)
                with open(path, 'rb') as image_file:
                    binary_data = image_file.read()
                    encoded_data = base64.b64encode(binary_data)
                    product.create({
                        'name': model[:6],
                        'detailed_type': 'dress',
                        'image_1920': encoded_data,
                        'cloth_align_mask': get_from(model, "cloth_align_mask-bytedance"),
                        'cloth_align_parse': get_from(model, "cloth_align_parse-bytedance"),
                    })

    def get_file_from(self, root, model, folderName):
        key = model[:6]
        item_path = root + folderName
        item_list = os.listdir(item_path)
        for item in item_list:
            if item.startswith(key):
                path = os.path.join(item_path, item)
                with open(path, 'rb') as image_file:
                    binary_data = image_file.read()
                    encoded_data = base64.b64encode(binary_data).decode('utf-8')
                    return encoded_data

    def get_file_from_hr(self, root, model, folderName):
        key = model[:5]
        item_path = root + folderName
        item_list = os.listdir(item_path)
        for item in item_list:
            if item.startswith(key):
                path = os.path.join(item_path, item)
                with open(path, 'rb') as image_file:
                    binary_data = image_file.read()
                    encoded_data = base64.b64encode(binary_data).decode('utf-8')
                    return encoded_data

    def migrate_data_hr(self):
        root = "D:\\code\\Python\\HangersAI\\Try_on\\input\\"
        product = self.env['product.template']

        # import model
        dem = 0
        root_path = root + "image"
        item_list = os.listdir(root_path)
        for item in item_list:
            if item.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                dem += 1
                if dem > 100: break
                path = os.path.join(root_path, item)
                with open(path, 'rb') as image_file:
                    binary_data = image_file.read()
                    encoded_data = base64.b64encode(binary_data)
                    product.create({
                        'name': item[:6],
                        'detailed_type': 'model',
                        'type_model': 'upper_hr',
                        'image_1920': encoded_data,
                        'agonostic_v32': self.get_file_from_hr(root, item, "agnostic-v3.2"),
                        'densepose': self.get_file_from_hr(root, item, "image-densepose"),
                        'parse_agonostic_v32': self.get_file_from_hr(root, item, "image-parse-agnostic-v3.2"),
                        'parse_v3': self.get_file_from_hr(root, item, "image-parse-v3"),
                        'openpose_img': self.get_file_from_hr(root, item, "openpose_img"),
                        'openpose_json': self.get_file_from_hr(root, item, "openpose_json"),
                        'cloth_model': self.get_file_from_hr(root, item, "cloth"),
                        'cloth_mask_model': self.get_file_from_hr(root, item, "cloth-mask")
                    })
        # import upper
        dem = 0
        root_path = root + "cloth"
        item_list = os.listdir(root_path)
        for item in item_list:
            if item.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                dem += 1
                if dem > 100: break
                path = os.path.join(root_path, item)
                with open(path, 'rb') as image_file:
                    binary_data = image_file.read()
                    encoded_data = base64.b64encode(binary_data)
                    product.create({
                        'name': item[:6],
                        'detailed_type': 'upper',
                        'image_1920': encoded_data,
                        'mask': self.get_file_from_hr(root, item, "cloth-mask")
                    })

    def migrate_data_gp_lower(self):
        root = "D:\\code\\Python\\HangersAI\\GP-VTON\\dataset\\Dresscode\\lower\\"
        product = self.env['product.template']

        # import model
        dem = 0
        root_path = root + "image"
        item_list = os.listdir(root_path)
        for item in item_list:
            if item.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                dem += 1
                if dem > 100: break
                path = os.path.join(root_path, item)
                with open(path, 'rb') as image_file:
                    binary_data = image_file.read()
                    encoded_data = base64.b64encode(binary_data)
                    product.create({
                        'name': item[:6],
                        'detailed_type': 'model',
                        'type_model': 'lower_gp',
                        'image_1920': encoded_data,
                        'parse_bytedance': self.get_file_from(root, item,"parse-bytedance"),
                        'densepose': self.get_file_from(root, item,"densepose"),
                        'pose_25': self.get_file_from(root, item,"pose_25"),
                        'cloth_align': self.get_file_from(root, item,"cloth_align"),
                        'cloth_align_mask': self.get_file_from(root, item, "cloth_align_mask-bytedance"),
                        'cloth_align_parse': self.get_file_from(root, item, "cloth_align_parse-bytedance"),
                    })
        dem = 0
        root_path = root + "cloth_align"
        item_list = os.listdir(root_path)
        for item in item_list:
            if item.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                dem += 1
                if dem > 100: break
                path = os.path.join(root_path, item)
                with open(path, 'rb') as image_file:
                    binary_data = image_file.read()
                    encoded_data = base64.b64encode(binary_data)
                    product.create({
                        'name': item[:6],
                        'detailed_type': 'lower',
                        'image_1920': encoded_data,
                        'cloth_align_mask': self.get_file_from(root, item, "cloth_align_mask-bytedance"),
                        'cloth_align_parse': self.get_file_from(root, item, "cloth_align_parse-bytedance"),
                    })

    def migrate_data_gp_dress(self):
        root = "D:\\code\\Python\\HangersAI\\GP-VTON\\dataset\\Dresscode\\dresses\\"
        product = self.env['product.template']

        # import model
        dem = 0
        root_path = root + "image"
        item_list = os.listdir(root_path)
        for item in item_list:
            if item.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                dem += 1
                if dem > 100: break
                path = os.path.join(root_path, item)
                with open(path, 'rb') as image_file:
                    binary_data = image_file.read()
                    encoded_data = base64.b64encode(binary_data)
                    product.create({
                        'name': item[:6],
                        'detailed_type': 'model',
                        'type_model': 'dress_gp',
                        'image_1920': encoded_data,
                        'parse_bytedance': self.get_file_from(root, item, "parse-bytedance"),
                        'densepose': self.get_file_from(root, item, "densepose"),
                        'pose_25': self.get_file_from(root, item, "pose_25"),
                        'cloth_align': self.get_file_from(root, item, "cloth_align"),
                        'cloth_align_mask': self.get_file_from(root, item, "cloth_align_mask-bytedance"),
                        'cloth_align_parse': self.get_file_from(root, item, "cloth_align_parse-bytedance"),
                    })
        dem = 0
        root_path = root + "cloth_align"
        item_list = os.listdir(root_path)
        for item in item_list:
            if item.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                dem += 1
                if dem > 100: break
                path = os.path.join(root_path, item)
                with open(path, 'rb') as image_file:
                    binary_data = image_file.read()
                    encoded_data = base64.b64encode(binary_data)
                    product.create({
                        'name': item[:6],
                        'detailed_type': 'dress',
                        'image_1920': encoded_data,
                        'cloth_align_mask': self.get_file_from(root, item, "cloth_align_mask-bytedance"),
                        'cloth_align_parse': self.get_file_from(root, item, "cloth_align_parse-bytedance"),
                    })
