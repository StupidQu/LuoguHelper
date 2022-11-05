import json
from colorama import Fore
import requests
from submissions import get_record_details


def submit_code(code, pro, con=None, ):
    url = "https://www.luogu.com.cn/fe/api/problem/submit/" + pro
    if con is not None:
        url += "?contestId=" + con
    datas = json.dumps({"enableO2": 1, "lang": 0, "code": code})
    headers = {
        "cookie": "__client_id=f6be92ba81aee9971fbd19c1c1b3476772c690ea; login_referer=https%3A%2F%2Fwww.luogu.com.cn%2F; _uid=846712",
        "origin": "https://www.luogu.com.cn",
        "referer": "https://www.luogu.com.cn/problem/" + pro,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52",
        "X-CSRF-TOKEN": "1667643980:OH+HIvLWzLw2vfHM2T4XJpWRR7/g5sUo4zj19ijmPh0=",
        "Content-Type": "application/json"
    }
    response = requests.post(url, data=datas, headers=headers)
    # print(response.text)
    rid = json.loads(response.text)['rid']
    print(Fore.GREEN + "OK submitted, rid =" + Fore.MAGENTA , rid , Fore.RESET)
    get_record_details(str(rid))
