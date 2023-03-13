import os
import time
from datetime import datetime
from termcolor import colored
from collections import OrderedDict

import pandas as pd

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
        return '[' + ''.join(['=' for _ in range(prog-1 if prog>0 else 0)]) + ('>' if prog<dim else '') + ''.join([' ' for _ in range((dim-prog-1 if prog==0 else dim-prog) if dim-prog>0 else 0)]) + ']' + (': ' + str(status*100) + '%' if show_perc else '')

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

    def open_instagram(self):
        self.driver.get(self.base_ig_url)

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
        self.xpaths['profile_page'] = {
            'posts_href':                   self.xpaths['head_selector'] + '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/article/div[1]/div/child::div/child::div/a',
        }
        self.xpaths['login_procedure'] = {
            'allow_cookies_button':         self.xpaths['head_selector'] + '/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]', 
            'username_input':               '//*[@id="loginForm"]/div/div[1]/div/label/input',
            'password_input':               '//*[@id="loginForm"]/div/div[2]/div/label/input',
            'submit_button':                '//*[@id="loginForm"]/div/div[3]/button',
            'save_info_button':             self.xpaths['head_selector'] + '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/section/div/button',
            'notification_button':          self.xpaths['head_selector'] + '/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]',
        }
        self.xpaths['post_info'] = {
            'post_author':                  self.xpaths['head_selector'] + '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/div/div/div[1]/div/div/a',
            'post_description':             self.xpaths['head_selector'] + '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/h1',
            'post_datetime':                self.xpaths['head_selector'] + '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[2]/div/div/a/div/time',
            'post_comments': {
                'button_more':              self.xpaths['head_selector'] + '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/li/div/button',
                'users':                    self.xpaths['head_selector'] + '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/child::ul/div/li/div/div/div[2]/h3/div/div/div/a',
                'comments':                 self.xpaths['head_selector'] + '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/child::ul/div/li/div/div/div[2]/div[1]/span',
                'comments_datetime':        self.xpaths['head_selector'] + '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/child::ul/div/li/div/div/div[2]/div[2]/div/a/time',
                'comments_like':            self.xpaths['head_selector'] + '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/child::ul/div/li/div/div/div[2]/div[2]/div/button[1]/div',
            }
        }

    def ig_login(self, login_info, sleeptime=10):
        self.driver.maximize_window()
        self.open_instagram()
        self.timeout_exec(self.init_xpaths, sleeptime=sleeptime)
        self.driver.find_element_by_xpath(self.xpaths['login_procedure']['allow_cookies_button']).click()
        self.safe_find_element(self.xpaths['login_procedure']['username_input']).send_keys(login_info['username'])
        self.safe_find_element(self.xpaths['login_procedure']['password_input']).send_keys(login_info['password'])
        self.timeout_exec(lambda: self.safe_find_element(self.xpaths['login_procedure']['submit_button']).click())
        self.timeout_exec(self.init_xpaths, sleeptime=sleeptime)
        self.safe_find_element(self.xpaths['login_procedure']['save_info_button']).click()
        self.timeout_exec(self.init_xpaths, sleeptime=sleeptime)
        self.safe_find_element(self.xpaths['login_procedure']['notification_button']).click()


    def profile_url(self):
        return self.base_ig_url + self.profile +'/'

    def load_profile_page(self):
        self.driver.get(self.profile_url())
        self.driver.maximize_window()
        self.timeout_exec(self.init_xpaths)

    def scroll_profile(self):
        self.driver.execute_script('window.scrollBy(0, window.innerHeight)')

    def get_posts_href(self):
        a_elements = self.safe_find_elements(self.xpaths['profile_page']['posts_href'])
        return [self.igs_utils.try_or_default(lambda el: el.get_attribute('href'), args=[a]) for a in a_elements]

    def scroll_profile_posts(self, n_post=5, sleeptime=-1, write_to_csv=''):
        self.load_profile_page()
        self.timeout_exec(self.init_xpaths, sleeptime=10)
        all_posts = self.get_posts_href()
        all_post_unique = set(all_posts)
        while len(all_post_unique) < n_post:
            self.scroll_profile()
            all_posts.extend(self.timeout_exec(self.get_posts_href, sleeptime=sleeptime))
            all_post_unique = set(all_posts)
            self.log(f'Post loaded: {len(all_post_unique)} / {n_post} {self.igs_utils.status_bar(len(all_post_unique)/n_post)}', category='done', overwrite=True)
        all_posts = [self.get_post_id(post_link) for post_link in list(OrderedDict.fromkeys(all_posts))]
        if write_to_csv:
            filename = write_to_csv+'.csv'
            pd.DataFrame(all_posts, columns=['post_ids']).to_csv(filename, sep='\t', mode='a', header=not os.path.exists(filename), index=False)
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
    
    def safe_find_elements(self, xpath, timeout=30):
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return self.driver.find_elements_by_xpath(xpath)

    def get_post_data(self, post_id, scrape_comments=False, load_comments_steps=10, load_comments_retry=3):
        self.open_post(post_id)
        self.init_xpaths()
        p_author = self.safe_find_element(self.xpaths['post_info']['post_author']).text
        p_description = self.safe_find_element(self.xpaths['post_info']['post_description']).text
        p_date = self.safe_find_element(self.xpaths['post_info']['post_datetime']).get_attribute('datetime')
        post_data = {
            'post_id': post_id,
            'post_data': {
                'author': p_author,
                'description': p_description.replace('\n', ' '),
                'date': p_date
            }
        }
        if scrape_comments:
            post_data['comments_data'] = self.get_post_comments(load_steps=load_comments_steps, load_retry=load_comments_retry)
        return post_data
    
    def get_posts_data(self, post_ids, scrape_comments=False, load_comments_steps=10, load_comments_retry=3, write_to_file=''):
        posts_data = []
        for idx,pid in enumerate(post_ids):
            self.log(f'Post scraped: {idx} / {len(post_ids)} {self.igs_utils.status_bar(idx/len(post_ids))}', category='success', overwrite=(not scrape_comments))
            self.log('')
            post_data = self.get_post_data(pid, scrape_comments=scrape_comments, load_comments_steps=load_comments_steps, load_comments_retry=load_comments_retry)
            posts_data.append(post_data)
            if write_to_file:
                self.write_post_data(post_data, write_to_file + '_posts')
                self.write_comments_data(post_data, write_to_file + '_comments')
        return posts_data
    
    def get_post_comments(self, load_steps=10, load_retry=3):
        tot_steps = load_steps
        while (load_steps>0 and load_retry>0):
            try:
                self.safe_find_element(self.xpaths['post_info']['post_comments']['button_more'], timeout=10).click()
                self.log(f'Comments scraped: {len(self.driver.find_elements_by_xpath(self.xpaths["post_info"]["post_comments"]["users"]))} | Load more: {tot_steps-load_steps} / {tot_steps} {self.igs_utils.status_bar((tot_steps-load_steps)/tot_steps)}', category='done', overwrite=True)
            except:
                load_retry -= 1
            load_steps -= 1
        users = self.driver.find_elements_by_xpath(self.xpaths['post_info']['post_comments']['users'])
        comments = self.driver.find_elements_by_xpath(self.xpaths['post_info']['post_comments']['comments'])
        comments_datetime = self.driver.find_elements_by_xpath(self.xpaths['post_info']['post_comments']['comments_datetime'])
        comments_likes = self.driver.find_elements_by_xpath(self.xpaths['post_info']['post_comments']['comments_like'])
        return [
            {
                'user': user.text,
                'comment': comment.text.replace('\n', ' '),
                'comment_datetime': comment_datetime.get_attribute('datetime'),
                'comment_likes': int(comment_likes.text.split()[0].replace(',','')) if len(comment_likes.text)>0 and comment_likes.text[0].isnumeric() else 0
            } 
            for user, comment, comment_datetime, comment_likes in zip(users, comments, comments_datetime, comments_likes)
        ]
    
    def write_post_data(self, post_data, filename):
        data = [
            {
                'post_id': post_data['post_id'],
                'author': post_data['post_data']['author'],
                'description': post_data['post_data']['description'],
                'date': post_data['post_data']['date']
            }
        ]
        filename = filename + '.csv'
        pd.DataFrame(data).to_csv(filename, mode='a', sep='\t', header=not os.path.exists(filename), index=False)

    def write_comments_data(self, post_data, filename):
        data = [
            {
                'post_id': post_data['post_id'],
                'user': comment['user'],
                'comment': comment['comment'],
                'comment_datetime': comment['comment_datetime'],
                'comment_likes': comment['comment_likes']  
            } 
            for comment in post_data['comments_data']
        ]
        filename = filename + '.csv'
        pd.DataFrame(data).to_csv(filename, mode='a', sep='\t', header=not os.path.exists(filename), index=False)
        
