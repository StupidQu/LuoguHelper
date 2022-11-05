from ctypes.wintypes import PINT
import json
from time import sleep
from colorama import Fore, Style
# from django.shortcuts import render
import requests


def compile_result(cr):
    passed = cr['success']
    message = cr['message']
    if passed == False and message is not None:
        return Fore.RED + "Compile Error: " + Fore.YELLOW + message
    elif passed == False:
        return Fore.RED + "Compile Error."
    if message is not None:
        return Fore.GREEN + "Compile Passed: " + Fore.YELLOW + message + Fore.RESET + "."
    else:
        return Fore.GREEN + "Compile Passed."


def testcase_result(tc):
    status = tc['status']
    result = ""
    if status == 12:
        result = Fore.GREEN + "Accepted"
    elif status == 6:
        result = Fore.RED + "Wrong Answer"
    elif status == 7:
        result = Fore.MAGENTA + "Runtime Error"
    elif status == 5:
        result = Fore.BLUE + "Time Limit Exceeded"
    else:
        result = Fore.BLACK + "Unknown Error(or MLE)"
    result = result + Style.RESET_ALL
    time = str(tc['time']) + 'ms'
    memory = str(round(tc['memory'] / 1024, 2)) + "MB"
    score = str(tc['score']) + "pts"
    desc = tc['description']
    if (tc['signal'] == 11):
        desc = "Segmentation fault."

    if desc is not "":
        desc = ", " + desc
    # print(time, memory, score, desc)
    return result + ", " + time + ", " + memory + ", " + score + desc + Style.RESET_ALL


def subtask_result(st):
    score = st['score']
    status = st['status']
    result = Style.BRIGHT
    if status == 14:
        result += Fore.RED + "Unaccepted"
    else:
        result += Fore.GREEN + "Accepted"
    result = result + Style.RESET_ALL + ", " + str(score) + "pts\n"
    for i in st['testCases'].values():
        result += "\tTestCases #" + \
            str(i['id'] + 1) + ": " + testcase_result(i) + "\n"
    return "Subtask #" + str(st['id'] + 1) + ": " + result


def render_name(name, color):
    if color == "Gray":
        return Fore.RESET + name
    elif color == "Blue":
        return Fore.BLUE + name + Fore.RESET
    elif color == "Orange":
        return Fore.YELLOW + name + Fore.RESET
    elif color == "Red":
        return Fore.RED + name + Fore.RESET


def multi_subtasks(st):
    final_res = ""
    for _, i in st['judgeResult']['subtasks'].items():
        result = Style.BRIGHT
        score = i['score']
        status = i['status']
        if status == 14:
            result += Fore.RED + "Unaccepted"
        else:
            result += Fore.GREEN + "Accepted"
        result = result + Style.RESET_ALL + ", " + str(score) + "pts\n"
        if isinstance(i['testCases'], list):
            # result += 
            final_res += "Subtask #" + str(i['id'] + 1) + ": " + result + "\tTestCases #" + \
                str(i['testCases'][0]['id'] + 1) + ": " + \
                testcase_result(i['testCases'][0]) + "\n\n"
            continue
        # print(score['judgeResult']
        # print(st['judgeResult']['subtasks'][str(i + 1)])
        # print(i['testCases'])
        # print(type(i['testCases']))
        for j in i['testCases'].values():
            # print(j)
            result += "\tTestCases #" + \
                str(j['id'] + 1) + ": " + testcase_result(j) + "\n"
        final_res += "Subtask #" + str(i['id'] + 1) + ": " + result + "\n"
    return final_res


def get_record_details(rid):
    url = "https://www.luogu.com.cn/record/" + rid + "?_contentOnly=1"
    # print(url)
    headers = {
        "cookie": "__client_id=05e830a8b367d3a62069adc4e1a21a82b85773ad; _uid=846712",
        "origin": "https://www.luogu.com.cn",
        "referer": "https://www.luogu.com.cn/problem/P1001",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52",
        # "X-CSRF-TOKEN": "1667196860:6yo2kpl/Ls0sB4z9/SMA3VUbw0wwv7Ig1DQmWapF87g=",
        # "Content-Type": "application/json"
    }
    ret = requests.get(url, headers=headers)
    # print(ret.text)
    if json.loads(ret.text)['code'] != 200:
        print(Fore.RED + "Patch Error: " + str(json.loads(ret.text)['code']))
        return
    score = json.loads(ret.text)["currentData"]["record"]["detail"]
    while score['compileResult'] is None:
        print(Fore.CYAN + "Judging, please wait..." + Style.RESET_ALL)
        ret = requests.get(url, headers=headers)
    # print(ret.text)
        if json.loads(ret.text)['code'] != 200:
            print(Fore.RED + "Patch Error: " +
                  str(json.loads(ret.text)['code']))
            return
        score = json.loads(ret.text)["currentData"]["record"]["detail"]
        sleep(3)
    print(compile_result(score["compileResult"]) + Style.RESET_ALL + "\n")
    if score["compileResult"]['success'] == False:
        return
    # sleep(2)
    # print(score['judgeResult']['subtasks'][0]['testCases']['1'])
    # print(score['judgeResult'])
    while len(score['judgeResult']['subtasks']) == 0:
        print(Fore.CYAN + "Judging, please wait..." + Style.RESET_ALL)
        ret = requests.get(url, headers=headers)
    # print(ret.text)
        if json.loads(ret.text)['code'] != 200:
            print(Fore.RED + "Patch Error: " +
                  str(json.loads(ret.text)['code']))
            return
        score = json.loads(ret.text)["currentData"]["record"]["detail"]
        sleep(2)
    # print(score['judgeResult']['subtasks'])
    if len(score['judgeResult']['subtasks']) != 1 and isinstance(score['judgeResult']['subtasks'], list) == False:
        print(multi_subtasks(score))
    else:
        # print(len(score['judgeResult']['subtasks']))
        for i in range(len(score['judgeResult']['subtasks'])):
            if isinstance(score['judgeResult']['subtasks'][i], dict) == False:
                continue
            # print(i)
            print(subtask_result(score['judgeResult']['subtasks'][i]))
    result_all = ""
    if json.loads(ret.text)["currentData"]["record"]['status'] == 14:
        result_all = Fore.RED + Style.BRIGHT + "Unaccepted" + Style.RESET_ALL
    else:
        result_all = Fore.GREEN + Style.BRIGHT + "Accepted" + Style.RESET_ALL
    # print(json.loads(ret.text)["currentData"]["record"])
    print('Owner: ' + render_name(json.loads(ret.text)["currentData"]["record"]['user']['name'], json.loads(ret.text)["currentData"]["record"]['user']['color']) + ', Problem: ' + json.loads(
        ret.text)["currentData"]["record"]['problem']['pid'] + ", Result: " + result_all + ", " + str(json.loads(ret.text)["currentData"]["record"]['score']) + 'pts')
    # print(testcase_result(score['judgeResult']
    #       ['subtasks'][0]['testCases']['0']))
    # print()
