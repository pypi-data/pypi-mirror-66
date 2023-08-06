import re
import requests
from bs4 import BeautifulSoup

from zwutils import reutils

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
class FreeProxy(object):
    @staticmethod
    def data5u():
        urls = [
            'http://www.data5u.com/'
        ]
        for url in urls:
            r = requests.get(url, headers={'User-Agent': USER_AGENT})
            soup = BeautifulSoup(r.text, features='html.parser')
            items = soup.find_all('ul', attrs={'class':'l2'})
            for item in items:
                re_str = r'http[s]*'
                t = item.text
                ip = reutils.find_ip(t)
                port = reutils.find_port(t, port_start=5000)
                tp = re.findall(re_str, t, re.I)
                ip = ip[0]
                port = port[0]
                tp = tp[0].lower()
                yield '{}://{}:{}'.format(tp, ip, port)
    
    @staticmethod
    def xicidaili():
        urls = [
            'http://www.xicidaili.com/nn/',  # 高匿
            'http://www.xicidaili.com/nt/',  # 透明
        ]
        for url in urls:
            r = requests.get(url, headers={'User-Agent': USER_AGENT})
            soup = BeautifulSoup(r.text, features='html.parser')
            items = soup.find_all('tr')
            items = [o for o in items if 'class' in o.attrs]
            for item in items:
                re_str = r'http[s]*'
                t = item.text
                ip = reutils.find_ip(t)
                port = reutils.find_port(t, port_start=80)
                tp = re.findall(re_str, t, re.I)
                ip = ip[0]
                port = port[0]
                tp = tp[0].lower()
                yield '{}://{}:{}'.format(tp, ip, port)

if __name__ == '__main__':
    FreeProxy.xicidaili()
