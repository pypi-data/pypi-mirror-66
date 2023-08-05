import os

from colorama import Fore

import kivia.util as util


class Utils:
    def __init__(self):
        self.__util = util.KiviaUtils()
        self.GET = 1
        self.POST = 2
        self.PUT = 3
        self.DELETE = 4

    def printProgressBar(self, iteration, total, prefix='', suffix='', length=100, fill='='):
        self.__util.printProgressBar(iteration, total, prefix, suffix, length, fill)

    def setLine(self, line):
        self.__util.LINE = line

    def uniqueComputerId(self):
        return self.__util.uniqueComputerId()

    def line(self, times=18, text="-", linebreak=True):
        return self.__util.line(times, text, linebreak)

    def showDatas(self, title, list: [], showNo=False, lolcat=True, exclude=[], isError=False, onEmpty="List is Empty"):
        self.__util.showDatas(title, list, showNo, lolcat, exclude, isError, onEmpty)

    def loading(self, prefix='', suffix=''):
        self.__util.loading(prefix, suffix)

    def showLoading(self, prefix, suffix):
        self.__util.showLoading(prefix, suffix)

    def sendMessageToSystem(self, title, message):
        self.__util.sendMessageToSystem(title, message)

    def hideLoading(self):
        self.__util.isLoading = False

    def lolcatText(self, data):
        from kivia.lolcat import lolcat
        return lolcat(data)

    def getAppRoot(self, modulename):
        return self.__util.getAppRoot(modulename)

    def fetchData(self, _type: int, url, prefix='', suffix='', data=None, headers={}):
        return self.__util.fetchData(_type, url, prefix, suffix, data, headers)

    def generateError(self, param, printit=True):
        return self.__util.generateError(param, printit=printit)

    def confirm(self, defaultmsg="Do you want to continue? [Y/n]", linebreak=True):
        return self.__util.confirm(defaultmsg, linebreak)

    def isError(self, request):
        return self.__util.isError(request)

    def colored(self, param, COLOR, printit=True):
        x = f"{COLOR}{param}{Fore.RESET}"
        return print(x) if printit else x

    def hasSudoPermission(self):
        return os.geteuid() == 0

    def getCurrentDir(self):
        return self.__util.getCurrentDir()

    def createDirs(self, path):
        return self.__util.createDirs(path)

    def getRandomCharacters(self, no):
        return self.__util.getRandomCharacters(no)

    def askSudoPermission(self):
        return self.__util.askSudoPermission()
