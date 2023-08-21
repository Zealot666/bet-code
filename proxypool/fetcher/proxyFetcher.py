# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     proxyFetcher
   Description :
   Author :        JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: proxyFetcher
-------------------------------------------------
"""
__author__ = 'JHao'

import json
import re
import time
from time import sleep

import requests
from pyquery import PyQuery as pq
from util.webRequest import WebRequest


class ProxyFetcher(object):
    """
    proxy getter
    """

    @staticmethod
    def freeProxy08():
        proxies = []
        ip_regex = re.compile(r'^\d+\.\d+\.\d+\.\d+$')
        port_regex = re.compile(r'^\d+$')
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/79.0.3945.130 Chrome/79.0.3945.130 Safari/537.36'
        }

        def getSingePage(url):
            try:
                time.sleep(5)
                html = requests.get(url, headers=headers, timeout=10).text
                doc = pq(html)
            except Exception as e:
                print('ERROR in ip.ihuan.me:', e)
                return
            for line in doc('tbody tr').items():
                tds = list(line('td').items())
                if len(tds) == 10:
                    ip = tds[0].text().strip()
                    port = tds[1].text().strip()
                    if re.match(ip_regex, ip) is not None and re.match(port_regex, port) is not None:
                        proxies.append(str(ip) + ":" + str(port))

        def getPages(url_start):
            pending_urls = []
            url = url_start
            doc = pq("1234")
            try:
                html = requests.get(url, headers=headers, timeout=10).text
                doc = pq(html)
            except Exception as e:
                print('ERROR in ip.ihuan.me:', e)
            pending_urls.append(url_start)
            for item in list(doc('.pagination a').items())[1:-1]:
                href = item.attr('href')
                if href is not None and href.startswith('?page='):
                    # pending_urls.append('https://ip.ihuan.me/' + href)
                    pending_urls.append(url_start + href)
            for url in pending_urls:
                getSingePage(url)
            return pending_urls[len(pending_urls) - 1]

        try:
            next_round = getPages("https://ip.ihuan.me/")
            for i in range(1, 5):
                    next_round = getPages(next_round)
        except:
            pass

        try:
            next_round = getPages("https://ip.ihuan.me/address/5Lit5Zu9.html/")
            for i in range(1, 5):
                next_round = getPages(next_round)
        except:
            pass

        for proxy in proxies:
            yield proxy

    @staticmethod
    def freeProxy09():
        """
        http://ip.jiangxianli.com/
        免费代理库
        :return:
        """
        urls = []
        for page in range(1, 8):
            url = f'https://ip.jiangxianli.com/?page={page}'
            urls.append(url)
        proxies = []
        ip_regex = re.compile(r'^\d+\.\d+\.\d+\.\d+$')
        port_regex = re.compile(r'^\d+$')
        for url in urls:
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/79.0.3945.130 Chrome/79.0.3945.130 Safari/537.36'
            }
            time.sleep(3)
            html = requests.get(url, headers=headers, timeout=10).text
            doc = pq(html)
            for line in doc('tr').items():
                tds = list(line('td').items())
                if len(tds) >= 2:
                    ip = tds[0].text().strip()
                    port = tds[1].text().strip()
                    if re.match(ip_regex, ip) is not None and re.match(port_regex, port) is not None:
                        proxies.append(str(ip) + ":" + str(port))

        for proxy in proxies:
            yield proxy

    @staticmethod
    def freeProxy16():
        url = "https://www.proxyscan.io/download?type=http"

        proxies = []
        ip_regex = re.compile(r'^\d+\.\d+\.\d+\.\d+$')
        port_regex = re.compile(r'^\d+$')

        html = WebRequest().get(url, timeout=10).text
        for item in html.split("\n"):
            try:
                ip = item.split(":")[0]
                port = item.split(":")[1]
                if re.match(ip_regex, ip) is not None and re.match(port_regex, port) is not None:
                    proxies.append(ip + ":" + port)
            except Exception:
                continue

        for ip in proxies:
            yield ip.strip()

    @staticmethod
    def freeProxy17():
        data = WebRequest().get('https://uu-proxy.com/api/free', timeout=10).text
        free = json.loads(data)['free']
        proxies = []
        for item in free['proxies']:
            proxies.append(str(item['ip']) + ":" + str(item['port']))

        for ip in proxies:
            yield ip.strip()

    @staticmethod
    def freeProxy18():
        urls = set()
        proxies = []
        ip_regex = re.compile(r'^\d+\.\d+\.\d+\.\d+$')
        port_regex = re.compile(r'^\d+$')

        for page in range(1, 2):
            url = "http://www.xsdaili.cn/dayProxy/" + str(page) + ".html"
            response = requests.get(url, timeout=8)
            for item in pq(response.text)('a').items():
                try:
                    if "/dayProxy/ip" in item.attr("href"):
                        urls.add("http://www.xsdaili.cn" + item.attr("href"))
                except Exception:
                    continue
            for url in urls:
                response = requests.get(url, timeout=8)
                doc = pq(response.text)
                for item in doc(".cont").items():
                    for line in item.text().split("\n"):
                        ip = line.split('@')[0].split(':')[0]
                        port = line.split('@')[0].split(':')[1]
                        if re.match(ip_regex, ip) is not None and re.match(port_regex, port) is not None:
                            proxies.append(ip + ":" + port)

        for ip in proxies[:500]:
            yield ip.strip()

    @staticmethod
    def paidProxy02():
        url = "http://uu-proxy.com/api/get_proxies?id=ZNKZNGASY4&size=50&schemes=http&support_https=true&restime_within_ms=1000&format=txt1_1"
        response = requests.get(url, timeout=8)
        proxies = response.text.split('\r\n')
        for ip in proxies:
            yield ip.strip()


if __name__ == '__main__':
    p = ProxyFetcher()
    for _ in p.freeProxy08():
        print(_)
