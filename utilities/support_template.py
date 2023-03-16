# !!! Watch ya steps - don't commit this file: 
# rename this into '_support.py' as it will be ignored by .gitignore (and imported in igs_test.ipynb)

login_account_info = {
    'username':     '<your-ig-username>',
    'password':     '<your-ig-password>'
}

ig_profiles = {
    'profile1':     '<profile1-username>',
    'profile2':     '<profile2-username>'
    
    # ... enojy :)
}

ig_xpaths = {
    'profile_page': {
        'posts_number':                 '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[1]/div/span/span',
        'posts_href':                   '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/article/div[1]/div/child::div/child::div/a',
    },
    'login_procedure': {
        'allow_cookies_button':         '/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]', 
        'username_input':               '//*[@id="loginForm"]/div/div[1]/div/label/input',
        'password_input':               '//*[@id="loginForm"]/div/div[2]/div/label/input',
        'submit_button':                '//*[@id="loginForm"]/div/div[3]/button',
        'save_info_button':             '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/section/div/button',
        'notification_button':          '/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]',
    },
    'post_info': {
        'post_author':                  '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/div/div/div[1]/div/div/a',
        'post_description':             '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/h1',
        'post_datetime':                '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[2]/div/div/a/div/time',
        'post_comments': {
            'button_more':              '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/li/div/button',
            'users':                    '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/child::ul/div/li/div/div/div[2]/h3/div/div/div/a',
            'comments':                 '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/child::ul/div/li/div/div/div[2]/div[1]/span',
            'comments_datetime':        '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/child::ul/div/li/div/div/div[2]/div[2]/div/a/time',
            'comments_like':            '/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/child::ul/div/li/div/div/div[2]/div[2]/div/button[1]/div',
        }
    }   
}