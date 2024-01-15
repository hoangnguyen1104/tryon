
from odoo import api, fields, models
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import logging
from datetime import datetime, timedelta
import threading
import time
from PIL import Image
from io import BytesIO
import base64
from requests import RequestException


_logger = logging.getLogger(__name__)

def filter_expect_tags(key_html, tags_crawl):
    if key_html.name in tags_crawl:
        return [key_html]
    return key_html.find_all(tags_crawl)

def resize_image(img_url, max_width=620, timeout=5):
    try:
        response = requests.get(img_url, timeout=timeout)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))

        # Set a maximum width for the image
        width_percent = (max_width / float(img.size[0]))
        new_height = int((float(img.size[1]) * float(width_percent)))
        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

        # Convert the image to a data URL
        buffered = BytesIO()
        img.save(buffered, format="JPEG")

        # Encode the image data using base64
        img_data_url = f"data:image/jpeg;base64,{base64.b64encode(buffered.getvalue()).decode('utf-8')}"

        return img_data_url
    except RequestException as e:
        print(f"Error or timeout resizing image: {e}")
        return img_url


def to_prettify(key_html):
    tags = ["p", "a", "h1", "h2", "h3", "h4", "h5", "h6"]
    content = ''
    max_image_width = 620
    dict = {}
    for item in key_html:
        try:
            if item.name in tags:
                content += f'<{item.name}>{item.text}</{item.name}>'
            elif item.name == 'img':
                # Resize the image and append with <img> tags
                img_url = item.get('data-src') or item['src']
                alt_text = item.get('alt', '')
                value = f'<img src="{img_url}" style="width: 620px;" alt="{alt_text}">'
                if not dict.get(value):
                    dict.update({
                        value: 1
                    })
                    content += value
                # resized_img_data_url = resize_image(img_url, max_image_width)
                #
                # if resized_img_data_url:
                #     alt_text = item.get('alt', '')
                #     value = f'<img src="{resized_img_data_url}" alt="{alt_text}">'
                #     if not dict.get(value):
                #         dict.update({
                #             value: 1
                #         })
                #         content += value
        except Exception as e:
            _logger.error(item)
            _logger.error(e)
    return content

def get_element_by_xpath(url, xpath):
    _logger.info(xpath)
    soup = get_soup(url)
    root = etree.HTML(str(soup))
    element = root.xpath(xpath)
    return etree.tostring(element[0], encoding='unicode')


def get_script(url):
    soup = get_soup(url)
    scripts = soup.body.find_all('script', recursive=False)
    ans = ''
    for s in scripts:
        ans += str(s) + '\n'
    return ans

def get_id_by_tag_class(_tag, _class):
    next_id = str(_tag)
    for c in _class:
        next_id += '.' + str(c)
    return next_id


def get_next_page(url, next_page):
    _tag, _class = get_tag_class(next_page)
    next_id = get_id_by_tag_class(_tag, _class)
    chrome_option = Options()
    chrome_option.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_option)
    driver.get(url)
    while True:
        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, next_id)))
        # Get the current page source
        page_source = driver.page_source

        # Create a BeautifulSoup object to parse the page source
        soup = BeautifulSoup(page_source, 'html.parser')
        next_button = driver.find_element(By.CSS_SELECTOR, next_id)

        if next_button.is_enabled():
            # Get the URL of the next page
            next_url = next_button.get_attribute('href')

            # Click on the next page button/link
            next_button.click()

            # Wait for the next page to load
            WebDriverWait(driver, 10).until(EC.staleness_of(next_button))

            # Print the URL of the next page
            print('Next page URL:', next_url)
            return next_url
        else:
            return None
    return None


def get_name_from(url):
    chars = ['.', '/', ':', '|', '*', '?', '<', '>']
    for c in chars:
        url = url.replace(c, '')
    return url


def get_text(html_selector):
    soup = BeautifulSoup(html_selector, 'html.parser')
    text = soup.get_text()
    return text.strip()

def get_link_post(post):
    soup = BeautifulSoup(post, 'html.parser')
    return soup.find('a')['href']

def get_tag_class(html_selector):
    soup = BeautifulSoup(html_selector, 'html.parser')
    root_tag = soup.find().name
    root_class = soup.find().get('class')
    return root_tag, root_class


def find_element_by_text(soup, text_selector):
    return soup.find(text=str(text_selector)).parent


def get_soup(url):
    response = requests.get(url, verify=False)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def get_element_all(soup, _tag, _class):
    return soup.find_all(_tag, class_=_class)

def get_element(soup, _tag, _class):
    return soup.find(_tag, class_=_class)


def remove_scripts_tag(soup):
    script_tags = soup.find_all('script')
    for script_tag in script_tags:
        script_tag.extract()
    return soup


def remove_form_tag(soup):
    form_tags = soup.find_all('form')
    for form_tag in form_tags:
        form_tag.extract()
    return soup


def unwrap_noscript_tag(soup):
    noscript_tags = soup.find_all('noscript')
    for noscript_tag in noscript_tags:
        noscript_tag.unwrap()
    return soup


class SourcingSites(models.Model):
    _name = "sourcing.sites"
    _description = "Website for crawl data"
    _rec_name = 'web_url'

    web_url = fields.Char(String="Website Url")
    category_id = fields.Many2one('category.sites', string="Category Site")
    xpath_post = fields.Char(string="Xpath Post")
    xpath_title = fields.Char(string="Xpath Tittle")
    xpath_content = fields.Char(string="Xpath Content")
    crawl_fields = fields.One2many('xpath.fields.line', 'sourcing_id', String="Crawl Fields")
    sync_date = fields.Datetime(string="Sync Date")
    xpath_next_page = fields.Char(string="Xpath Next Page")
    state = fields.Selection([
        ('active', "Ready Crawl"),
        ('pending', "Pending"),
        ('draft', "Draft")
    ], string="State")
    description = fields.Html(string="Note")
    post_number_clone = fields.Integer(string="Number Post Crawl")
    posts_data = fields.One2many('posts', 'sourcing_id', string='Data Posts')
    minute_cron = fields.Integer('Minute next cron')

    def check_exist(self, link):
        post_env = self.env['posts']
        posts = post_env.search([('url', '=', link), ('sourcing_id', '=', self.id)])
        if len(posts) > 0:
            return True
        return False

    def crawl_website(self, url, post, fields, num_post):
        soup = get_soup(url)
        _tag, _class = get_tag_class(post)
        posts = soup.find_all(_tag, class_=_class)
        _logger.info(posts)

        post_env = self.env['posts']
        post_line_env = self.env['post.line']
        dem = 0
        tags_crawl = self.env['tag.crawl.website'].search([]).mapped('name')
        for p in posts:
            dem += 1
            if dem > num_post:
                break
            try:
                link = p.find('a')['href']
                _logger.info(link)
                if self.check_exist(link):
                    _logger.info("link exist!")
                    continue
                new_post = post_env.create({
                    'url': link,
                    'title': p.find('a').text,
                    'sourcing_id': self.id
                })

                p_soup = get_soup(link)
                # scripts = get_script(link)
                content = ''
                for i in range(len(fields)):
                    key_html = fields[i][1]
                    _tag, _class = get_tag_class(key_html)
                    _logger.info(fields[i][1])
                    key_html = get_element(p_soup, _tag, _class)
                    key_html = remove_scripts_tag(key_html)
                    key_html = filter_expect_tags(key_html, tags_crawl)
                    # key_html = remove_form_tag(key_html)
                    # key_html = unwrap_noscript_tag(key_html)
                    key_html_str = to_prettify(key_html)
                    content += key_html_str + '\n'
                    _logger.info(key_html_str)
                    new_post_line = post_line_env.create({
                        'name': fields[i][0],
                        'content': key_html_str,
                        'post_id': new_post.id
                    })
                    if fields[i][0] == 'title':
                        new_post.data_title = get_text(key_html_str)
                    if fields[i][0] == 'content':
                        new_post.data_content = key_html_str

            except Exception as e:
                print(e)
        return dem

    def action_clone(self):
        self.sync_date = datetime.now()
        url = self.web_url
        num_post = self.post_number_clone
        fields = []
        for field in self.crawl_fields:
            fields.append((field.name, field.xpath))
        while num_post > 0:
            sl = self.crawl_website(url, self.xpath_post, fields, num_post)
            num_post -= sl
            if num_post > 0:
                url = get_next_page(url, self.xpath_next_page)

    def do_crawl(self):
        self.sync_date = datetime.now()
        url = self.web_url
        num_post = int(self.env['ir.config_parameter'].sudo().get_param('cms_wordpress.number_post_auto_crawl'))
        fields = []
        for field in self.crawl_fields:
            fields.append((field.name, field.xpath))
        while num_post > 0:
            sl = self.crawl_website(url, self.xpath_post, fields, num_post)
            num_post -= sl
            if num_post > 0:
                url = get_next_page(url, self.xpath_next_page)

    def ir_cron_crawl(self):
        sourcing_sites = self.sudo().search([])
        for site in sourcing_sites:
            threaded_calculation = threading.Thread(
                target=self._run_delayed_calculations, args=([site.id]))
            threaded_calculation.start()

    def parse_xpath_fields(self, url, post, fields, fields_html):
        soup = get_soup(url)
        _tag, _class = get_tag_class(post)
        posts = soup.find_all(_tag, class_=_class)
        link_post = get_link_post(post)
        for p in posts:
            try:
                link = p.find('a')['href']
                if link == link_post:
                    for i in range(len(fields)):
                        fields_html[i] = get_element_by_xpath(link, fields[i][1])
                    break
            except Exception as e:
                print(e)
        return fields_html

    def action_parsing_xpath(self):
        if self.xpath_post.startswith('//*'):
            self.xpath_post = get_element_by_xpath(self.web_url, self.xpath_post)
            self.xpath_next_page = get_element_by_xpath(self.web_url, self.xpath_next_page)
            fields = [('title', self.xpath_title), ('content', self.xpath_content)]
            fields_html = []
            fields_html.append(False)
            fields_html.append(False)
            for field in self.crawl_fields:
                fields.append((field.name, field.xpath))
                fields_html.append(False)
            fields_html = self.parse_xpath_fields(self.web_url, self.xpath_post, fields, fields_html)
            self.xpath_title = fields_html[0]
            self.xpath_content = fields_html[1]
            i = 2
            for field in self.crawl_fields:
                field.xpath = fields_html[i]
                i = i + 1

    def _run_delayed_calculations(self, site_id):
        # Delay to ensure data consistency
        time.sleep(3)
        # Enter thread-safe environment
        with api.Environment.manage():
            new_cr = self.pool.cursor()
            self = self.with_env(self.env(cr=new_cr))
            site = self.env['sourcing.sites'].sudo().browse(int(site_id))
            # Perform calculations and updates for each move
            site.do_crawl()
            new_cr.commit()
        return {}

    @api.model_create_multi
    def create(self, values_list):
        res = super(SourcingSites, self).create(values_list)
        field_line = self.env['xpath.fields.line']
        field_line.create({
            'name': 'title',
            'xpath': res.xpath_title,
            'sourcing_id': res.id
        })
        field_line.create({
            'name': 'content',
            'xpath': res.xpath_content,
            'sourcing_id': res.id
        })
        return res

