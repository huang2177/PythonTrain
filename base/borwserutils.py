import selenium.webdriver


class BrowserUtils(object):
    @staticmethod
    def chrome():
        return selenium.webdriver \
            .Chrome(executable_path='../chromedriver.exe')

def check_is_chinese(check_str):
    for ch in check_str.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False