import json
from colorama import Fore
import requests
import config
from bs4 import BeautifulSoup
from submissions import get_record_details


def get_csrf_token(pro, con):
    url = "https://www.luogu.com.cn/proble/" + pro
    if con is not None:
        url += "?contestId=" + con
    headers = {
        "cookie": "__client_id=" + config.get_config("account", "client_id") + "; login_referer=https%3A%2F%2Fwww.luogu.com.cn%2F; _uid=" + config.get_config("account", "uid"),
        "origin": "https://www.luogu.com.cn",
        "referer": "https://www.luogu.com.cn/problem/" + pro,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52",
        "X-CSRF-TOKEN": "1667643980:OH+HIvLWzLw2vfHM2T4XJpWRR7/g5sUo4zj19ijmPh0=",
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup.head.find_all('meta', attrs={'name':'csrf-token'})[0]['content']

def submit_code(code, pro, con=None):
    get_cookie()
    # get_csrf_token(pro, con)
    url = "https://www.luogu.com.cn/fe/api/problem/submit/" + pro
    if con is not None:
        url += "?contestId=" + con
    datas = json.dumps({"enableO2": 1, "lang": 0, "code": code})
    csrf = get_csrf_token(pro, con)
    # print(csrf)
    headers = {
        "cookie": "__client_id=" + config.get_config("account", "client_id") + "; login_referer=https%3A%2F%2Fwww.luogu.com.cn%2F; _uid=" + config.get_config("account", "uid"),
        "origin": "https://www.luogu.com.cn",
        "referer": "https://www.luogu.com.cn/problem/" + pro,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52",
        "X-CSRF-TOKEN": csrf,
        "Content-Type": "application/json"
    }
    response = requests.post(url, data=datas, headers=headers)
    # print(response.text)
    rid = json.loads(response.text)['rid']
    print(Fore.GREEN + "OK submitted, rid = " + Fore.MAGENTA + str(rid) +  Fore.GREEN +  ", csrf-token = " + Fore.MAGENTA + csrf + Fore.RESET)
    return rid
    get_record_details(str(rid))


def extract_cookies(cookie):
    """从浏览器或者request headers中拿到cookie字符串，提取为字典格式的cookies"""
    cookies = dict()
    for l in cookie.split('; '):
        # print(l)
        t = l.split("=")
        if len(t) < 2:
            continue
        cookies[t[0]] = t[1]
    # cookies = dict([l.split("=", 2) for l in cookie.split("; ")])
    return cookies


def get_cookie():
    if config.is_section_exist('account') == False:
        return
    url = "https://www.luogu.com.cn/"
    headers = {
        "cookie": "__client_id=" + config.get_config("account", "client_id") + "; login_referer=https%3A%2F%2Fwww.luogu.com.cn%2F; _uid=" + config.get_config("account", "uid"),
        "origin": "https://www.luogu.com.cn",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers)
    # print(type(resp?
    # print(response.headers.get('Set-Cookie'))
    # cookie = extract_cookies(response.headers.get('Set-Cookie'))
    cookie = dict()
    if response.headers.get('Set-Cookie') is not None:
        cookie = extract_cookies(response.headers.get('Set-Cookie'))
    if '_client_id' in cookie.keys():
        print(Fore.GREEN + "I:" + Fore.RESET + " Cookie updated.")
        config.set_config('account', '_client_id', cookie['_client_id'])
    # print(Fore.GREEN + "I:" + Fore.RESET + " Cookie updated.")
    # if cookie
    # print(response.headers)
