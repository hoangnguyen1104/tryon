from odoo import api, fields, models
import requests
from bs4 import BeautifulSoup


def get_element_all(soup, _tag, _class):
    return soup.find_all(_tag, class_=_class)


def get_link_post(post):
    soup = BeautifulSoup(post, 'html.parser')
    return soup.find('a')['href']


def get_tag_class(html_selector):
    soup = BeautifulSoup(html_selector, 'html.parser')
    root_tag = soup.find().name
    root_class = soup.find().get('class')
    return root_tag, root_class


def get_soup(url):
    response = requests.get(url, verify=False)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup


class XpathFieldLine(models.Model):
    _name = "xpath.fields.line"
    _description = "Save fields will crawl in website"
    _rec_name = 'name'

    name = fields.Char(string="Name")
    xpath = fields.Char(string="Xpath")
    state = fields.Boolean(string="Active", default=True)
    sourcing_id = fields.Many2one(string="Sourcing Site", comodel_name='sourcing.sites')
    stt = fields.Integer(string="Stt")

    def action_preview_elements(self):
        sourcing = self.sourcing_id
        soup = get_soup(sourcing.web_url)
        post = sourcing.xpath_post
        _tag, _class = get_tag_class(post)
        posts = soup.find_all(_tag, class_=_class)
        link_post = get_link_post(post)
        for p in posts:
            try:
                link = p.find('a')['href']
                if link == link_post:
                    soup_link = get_soup(link)
                    _tag, _class = get_tag_class(self.xpath)
                    elements = get_element_all(soup_link, _tag, _class)
                    pass
            except Exception as e:
                print(e)
        pass
