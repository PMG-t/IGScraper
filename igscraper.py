import time
from datetime import datetime
from termcolor import colored

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class UTILS:
    
    def __init__(self): pass

    def throw_msg(self, message, category='done', overwrite=False):
        category_color = { 'done':'blue', 'success':'green', 'warning':'yellow', 'error':'red' }
        if overwrite:
            print(colored(message, category_color[category.lower()]), end='\r')
        else:
            print(colored(message, category_color[category.lower()]))

    def status_bar(self, status, show_perc=False, dim=40):
        prog = int(status*dim)
        return '[' + ''.join(['=' for _ in range(prog-1 if prog>0 else 0)]) + ('>' if prog<dim else '') + ''.join([' ' for _ in range(dim-prog if dim-prog>0 else 0)]) + ']' + (': ' + str(status*100) + '%' if show_perc else '')

    def try_or_default(self, f, args=[], default=None):
        try:
            return f(*args) if args else f()
        except:
            return default
        
    def timeout_exec(self, f, args=[], sleeptime=0):
        time.sleep(sleeptime)
        return f(*args) if args else f()


class IGScraper():

    base_ig_url = 'https://www.instagram.com/'
    sleeptime = 2
    write_log = False
    xpaths = {
        'main_div': '/html/body/div[2]'
    }

    igs_utils = UTILS()

    def __init__(self, chromedriver_path='chromedriver.exe', profile=None):
        self.set_profile(profile)
        self.driver = webdriver.Chrome(chromedriver_path)

    def set_profile(self, profile):
        if profile:
            self.profile=profile
    
    def set_sleeptime(self, sleeptime):
        self.sleeptime = sleeptime
        
    def timeout_exec(self, f, args=[], sleeptime=-1):
        return self.igs_utils.timeout_exec(f, args, self.sleeptime if sleeptime<0 else sleeptime)

    def set_log(self, write_log):
        self.write_log = write_log

    def log(self, message, category='done', overwrite=False):
        if (self.write_log):
            self.igs_utils.throw_msg(message, category, overwrite)

    def init_xpaths(self):
        main_div = self.driver.find_element_by_xpath(self.xpaths['main_div'])
        self.xpaths['head_selector'] =      '//*[@id="' + main_div.get_attribute('id')  + '"]'
        self.xpaths['posts_href'] =          self.xpaths['head_selector'] + '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/article/div[1]/div/child::div/child::div/a'
        
        self.xpaths['post_author'] =        self.xpaths['head_selector'] + '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/div/div/div[1]/div/div/a'
        self.xpaths['post_description'] =   self.xpaths['head_selector'] + '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/h1'
        self.xpaths['post_datetime'] =      self.xpaths['head_selector'] + '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[2]/div/div/a/div/time'
        
        # self.xpaths['first_post'] =         self.xpaths['head_selector'] + '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[2]/article/div[1]/div/div[1]/div[1]/a',
        # self.xpaths['post_datetime'] =      self.xpaths['head_selector'] + '/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[2]/div/div/a/div/time',
        # self.xpaths['post_descr'] =         self.xpaths['head_selector'] + '/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/h1',
        # self.xpaths['button_more'] =        self.xpaths['head_selector'] + '/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/li/div/button',
        # self.xpaths['users'] =              self.xpaths['head_selector'] + '/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/child::*/div/li/div/div/div[2]/h3/div[1]/div/span/a',
        # self.xpaths['comments'] =           self.xpaths['head_selector'] + '/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/child::*/div/li/div/div/div[2]/div[1]/span',
        # self.xpaths['comments_datetime'] =  self.xpaths['head_selector'] + '/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/child::*/div/li/div/div/div[2]/div[2]/div/a/time',
        # self.xpaths['comments_like'] =      self.xpaths['head_selector'] + '/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/child::*/div/li/div/div/div[2]/div[2]/div/button[1]/div',
        # self.xpaths['next_post'] = {
        #     'first_post':                   self.xpaths['head_selector'] + '/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div[1]/button',
        #     'others':                       self.xpaths['head_selector'] + '/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div[2]/button'
        # }

    def profile_url(self):
        return self.base_ig_url + self.profile +'/'

    def load_profile_page(self):
        self.driver.get(self.profile_url())
        self.timeout_exec(self.init_xpaths)

    def scroll_profile(self):
        self.driver.execute_script('window.scrollBy(0, window.innerHeight)')

    def get_posts_href(self):
        a_elements = self.driver.find_elements_by_xpath(self.xpaths['posts_href'])
        return [self.igs_utils.try_or_default(lambda el: el.get_attribute('href'), args=[a]) for a in a_elements]

    def scroll_profile_posts(self, n_post=5, sleeptime=-1):
        self.init_xpaths()
        all_posts = set(self.get_posts_href())
        while len(all_posts) < n_post:
            self.timeout_exec(self.scroll_profile, sleeptime=sleeptime)    
            _ = [all_posts.add(post) for post in self.get_posts_href()]
            self.log(f'Post loaded: {len(all_posts)} / {n_post} {self.igs_utils.status_bar(len(all_posts)/n_post)}', category='done', overwrite=True)
        return all_posts
    
    def get_post_id(self, post_link):
        return post_link[post_link.index('/p/')+3 : -1]

    def get_post_link(self, post_id):
        return f'https://www.instagram.com/p/{post_id}/'

    def open_post(self, post_id):
        post_link = self.get_post_link(post_id)
        self.driver.get(post_link)

    def safe_find_element(self, xpath, timeout=30):
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return self.driver.find_element_by_xpath(xpath)

    def get_post_data(self, post_id, scrape_comments=False):
        self.open_post(post_id)
        self.init_xpaths()
        p_author = self.safe_find_element(self.xpaths['post_author']).text
        p_description = self.safe_find_element(self.xpaths['post_description']).text
        p_date = self.safe_find_element(self.xpaths['post_datetime']).get_attribute('datetime')
        post_info = {
            'post_id': post_id,
            'author': p_author,
            'description': p_description,
            'date': p_date
        }
        return post_info
