# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    gender = fields.Selection([('male', 'Male'),
                              ('female', 'Female')], string='Giới tính')

    detailed_type = fields.Selection(selection_add=[
        ('model', 'Models'),
        ('cloth', 'Clothes')],
        ondelete={
            'model': 'set service',
            'cloth': 'set service',
        }
    )

    def _detailed_type_mapping(self):
        type_mapping = super()._detailed_type_mapping()
        type_mapping['model'] = 'service'
        type_mapping['cloth'] = 'service'
        return type_mapping

    def migrate_data(self):
        print("okkk")
        import os
        import base64
        import binascii
        import io

        from PIL import Image, ImageOps
        try:
            from PIL.Image import Transpose, Palette, Resampling
        except ImportError:
            Transpose = Palette = Resampling = Image
        folder_path = "C:\\Users\\hoangnh61\\Downloads\\Try_on\\input\\image"
        file_list = os.listdir(folder_path)
        product = self.env['product.template']
        for file_name in file_list:
            # Check if the file is an image
            if file_name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                # Construct the full file path
                file_path = os.path.join(folder_path, file_name)
                print(file_name[:5])
                with open(file_path, 'rb') as image_file:
                    binary_data = image_file.read()
                    encoded_data = base64.b64encode(binary_data)
                    product.create({
                        'name': file_name[:5],
                        'detailed_type': 'model',
                        'image_1920': encoded_data
                    })
                    # product.image_1920 = Image.open(file_path)
