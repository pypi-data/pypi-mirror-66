import os
import threading
import time
from pathlib import Path
import requests
from colorama import Fore


class KiviaUtils:
    def __init__(self):
        self.GET = 1
        self.POST = 2
        self.PUT = 3
        self.LINE = "-"
        self.DELETE = 4
        self.isLoading = False

    def printProgressBar(self, iteration, total, prefix='', suffix='', length=100, fill='='):
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s [%s] %s' % (prefix, bar, suffix), end='\r')
        if iteration == total:
            print()

    def uniqueComputerId(self):
        return open("/var/lib/dbus/machine-id").read()

    def line(self, times=18, text='-', linebreak=True):
        if times == 0:
            return text + "\n" if linebreak else ""
        else:
            return f"{self.LINE if text == '-' else text}{self.line(times - 1, text)}"

    def showDatas(self, title, list: [], showNo=False, lolcat=True, exclude=[],
                  isError=False, onEmpty="List is Empty", seperator=':', linebreak=False):
        if not list:
            print(onEmpty)
            return
        vars = ""
        for x, y in enumerate(list):
            if showNo:
                vars += f"S.No : {x + 1}\n"
            for a in y:
                if a not in exclude:
                    vars += f"{a} {seperator} {y[a]}\n"
            vars += f"{self.line()}"
        data = (f"{self.line()}"
                f"{title if not isError else 'ERROR'}\n{self.line()}"
                f"{vars}")
        if lolcat:
            from kivia.lolcat import lolcat
            print(lolcat(data))
        else:
            print(data)

    def loading(self, prefix='', suffix=''):
        self.isLoading = True

        def count(i):
            if self.isLoading:
                if i == 65:
                    i = 0
                i += 1
                self.printProgressBar(i, 66, prefix=prefix, suffix=suffix, length=50)
                time.sleep(0.2)
                count(i)

        count(0)
        print('                                                                         ', end='\r')

    def showLoading(self, prefix='', suffix=''):
        thread = threading.Thread(target=self.loading, args=(prefix, suffix))
        thread.start()

    def sendMessageToSystem(self, title, message):
        os.system(f"notify {title} {message}")

    def hideLoading(self):
        self.isLoading = False

    def lolcatText(self, data):
        from kivia.lolcat import lolcat
        return lolcat(data)

    def getAppRoot(self, modulename):
        path = f"{Path.home()}/.kivia/.{modulename}"
        if not os.path.isdir(path):
            os.mkdir(path)
        return path

    def fetchData(self, _type: int, url, prefix='', suffix='', data=None, headers={}):
        try:
            self.showLoading(prefix, suffix)
            if _type == 1:
                x = requests.get(url, headers=headers)
            elif _type == 2:
                if not data:
                    self.hideLoading()
                    raise KeyError("Please pass data")
                x = requests.post(url, json=data, headers=headers)
            elif _type == 3:
                if not data:
                    self.hideLoading()
                    raise KeyError("Please pass data")
                x = requests.put(url, data=data, headers=headers)
            else:
                x = requests.delete(url, headers=headers)
            self.hideLoading()
            time.sleep(0.2)
            return x
        except Exception as e:
            if type(e) == KeyError:
                raise e
            else:
                self.hideLoading()

    def generateError(self, param, printit=True):
        data = f"{Fore.LIGHTRED_EX}{self.line()}Error\n{self.line()}{param}\n{self.line()}{Fore.RESET}"
        return print(data) if printit else data

    def confirm(self, defaultmsg="Do you want to continue? [Y/n]", linebreak=True):
        choice = input((f"\n{Fore.RESET}" if linebreak else Fore.RESET) + defaultmsg)
        return choice == "y" or choice == "Y" or choice == ""

    def isError(self, request):
        return "error" in request

    def colored(self, param, COLOR):
        print(f"{COLOR}{param}{Fore.RESET}")

    def hasSudoPermission(self):
        return os.geteuid() == 0

    def getCurrentDir(self):
        return os.path.dirname(__file__)

    def askSudoPermission(self):
        import subprocess
        x = subprocess.call("sudo -v".split())
        return x == 0

    def createDirs(self, path):
        try:
            os.mkdir(path)
        except:
            pass

    def getRandomCharacters(self, no):
        import random
        return ''.join(random.sample("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890", no))
