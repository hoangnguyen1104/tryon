
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

_logger = logging.getLogger(__name__)

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
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup


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

    def check_exist(self, link):
        post_env = self.env['posts']
        posts = post_env.search([('url', '=', link), ('sourcing_id', '=', self.id)])
        if len(posts) > 0:
            return True
        return False

    def crawl_website(self, url, post, fields):
        soup = get_soup(url)
        _tag, _class = get_tag_class(post)
        posts = soup.find_all(_tag, class_=_class)
        _logger.info(posts)

        post_env = self.env['posts']
        post_line_env = self.env['post.line']

        for p in posts:
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
                    key_html = remove_form_tag(key_html)
                    key_html = unwrap_noscript_tag(key_html)
                    content += key_html.prettify() + '\n'
                    _logger.info(key_html.prettify())
                    new_post_line = post_line_env.create({
                        'name': fields[i][0],
                        'content': key_html.prettify(),
                        'post_id': new_post.id
                    })
            except Exception as e:
                print(e)
        return len(posts)

    def action_clone(self):
        self.sync_date = datetime.now()
        url = self.web_url
        num_post = self.post_number_clone
        fields = []
        for field in self.crawl_fields:
            fields.append((field.name, field.xpath))
        while num_post > 0:
            sl = self.crawl_website(url, self.xpath_post, fields)
            num_post -= sl
            url = get_next_page(url, self.xpath_next_page)

    def do_crawl(self):
        self.sync_date = datetime.now()
        url = self.web_url
        num_post = int(self.env['ir.config_parameter'].sudo().get_param('cms_wordpress.number_post_auto_crawl'))
        fields = []
        for field in self.crawl_fields:
            fields.append((field.name, field.xpath))
        while num_post > 0:
            sl = self.crawl_website(url, self.xpath_post, fields)
            num_post -= sl
            url = get_next_page(url, self.xpath_next_page)
        pass

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
            fields = []
            fields_html = []
            for field in self.crawl_fields:
                fields.append((field.name, field.xpath))
                fields_html.append(False)
            fields_html = self.parse_xpath_fields(self.web_url, self.xpath_post, fields, fields_html)
            i = 0
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
