import os
import sys
import time

import click
from colorama import Fore

from kivia.DB import DB
from kivia.utils import Utils

util = Utils()
BASE_URL = "https://wisd4.herokuapp.com"


def makeDirs():
    util.createDirs(util.getCurrentDir() + "/dbs")
    util.createDirs(util.getCurrentDir() + "/modules")
    util.createDirs(util.getCurrentDir() + "/modules/test_modules")
    util.createDirs(util.getCurrentDir() + "/modules/live_modules")


makeDirs()
db = DB(util.getCurrentDir() + "/dbs/kivia.db")
db.createTable("modules", {
    "name": "text",
    "description": "text",
    "version": "integer",
    "alias": "text",
    "filename": "text",
    "time": "text"
})


@click.group()
def run():
    """
    Kivia is a module based cli app that helps you to do everything in CLI
    \n To install a package type /kpm install [modulename]
    \n\nTo search a package type /kpm search [modulename]
    """
    pass


@run.command("list")
def request():
    """This command list the modules installed in your system """
    modules = db.getAll("modules")
    data = []
    for x in modules:
        data.append(
            {"Name": x[0], "Description": x[1], "Version": x[2], "Alias": x[3], "Installed on": time.ctime(int(x[5]))})
    util.showDatas("List of installed modules:", data)


@run.command("install")
@click.argument("link")
def add_module(link):
    """This command install a module installed in your system """
    try:
        if db.get("modules", {"alias": link}):
            util.generateError(f"{link} is already installed.")
        else:
            data = util.fetchData(util.GET, f"{BASE_URL}/api/install/{link}", prefix="Searching.").json()
            util.showDatas("Module Information", [data], exclude=["rawUrl", "unique"])
            if "error" not in data:
                if util.confirm(linebreak=False):
                    code = util.fetchData(util.GET, url=data['rawUrl'],
                                          prefix="Installing Module.").content
                    os.system(f"pip3 install {' '.join(data['dependencies'])}")
                    filename = util.getRandomCharacters(15) + "." + data['rawUrl'].split('/').pop().split('.')[1]
                    open(
                        f"{os.path.dirname(__file__)}/modules/live_modules/{filename}",
                        "w").write(
                        code.decode("utf-8"))
                    import requests
                    requests.post(f"{BASE_URL}/api/ct/{data['unique']}", data={"id": util.uniqueComputerId()})
                    db.insert("modules", (
                        data['name'], data['description'], data['version'], data['alias'],
                        filename,
                        str(round(time.time()))))
                    util.colored("\n Module Installed Successfully !", Fore.GREEN)
                else:
                    util.colored("Operation aborted.", Fore.RED)
    except Exception as e:
        # raise e
        util.generateError("Some error")


@run.command("remove")
@click.argument('id')
def delete_module(id):
    """This command uninstalls a module from a system"""
    module = db.get("modules", {"alias": id})
    if not module:
        util.generateError(f"{id} module not found.")
    else:
        if util.confirm(
                f"{util.line(10)}Module {util.colored(module[0][0], Fore.LIGHTCYAN_EX, printit=False)} will be removed\n{util.line(10)}Are you sure (y/n):",
                linebreak=False):
            try:
                os.remove(f"{os.path.dirname(__file__)}/modules/live_modules/{module[0][4]}")
            except:
                pass
            db.delete("modules", {"alias": id})
            print("Module removed successfully.")
        else:
            print("Operation aborted.")


@run.command("search")
@click.argument("alias")
def search_module(alias):
    """This command searches a modules in internet """
    searchData = util.fetchData(util.GET, f"{BASE_URL}/api/search/{alias}", prefix="Searching..").json()
    util.showDatas(f"Top 10 Modules with name {alias}", searchData, isError=util.isError(searchData), showNo=True,
                   onEmpty=util.generateError(
                       "No search result found.Make sure search key is greater than 4 character.", printit=False))


@run.command()
def bindtobash():
    """This command binds the kivia cli to bash i.e you dont need to type kivia after doing this"""
    if util.hasSudoPermission():
        print(f"----\n{Fore.RED}Please dont run this with sudo\n-----")
    else:
        if "kpm $@" in os.popen("cat ~/.bashrc").read()[:-1]:
            print("Kivia is already installed to bash.")
        else:
            os.system(f'echo "{open(util.getCurrentDir() + "/bashrc.sh").read()}">>~/.bashrc')
            print(
                f"{Fore.LIGHTGREEN_EX}Kivia is now installed to bash.\n Check it by reopening this terminal"
                f" and typing {Fore.WHITE}--help")


@run.command()
def top():
    """This command lists the top modules from the internet."""
    searchData = util.fetchData(util.GET, f"{BASE_URL}/api/top", prefix="Listing Modules..").json()
    util.showDatas(f"Top 10 Modules", searchData, isError=util.isError(searchData), showNo=True,
                   onEmpty=util.generateError(
                       "No Modules Found.", printit=False))


def moduleExists(args, type='live_modules'):
    def run(name):
        exec(f"import kivia.modules.{type}.{name} as md")
        locals()['md'].run(args[1:])
        return True

    if type == 'live_modules':
        modules = db.getAll("modules")
        for x in modules:
            if x[3] == args[0]:
                return run(x[4].split('.').pop(0))
    else:
        return run(args[0])
    return False


def showhelp():
    click.echo(util.lolcatText('''
  _  ___       _       
 | |/ (_)     (_)      
 | ' / ___   ___  __ _ 
 |  < | \ \ / / |/ _` |
 | . \| |\ V /| | (_| |
 |_|\_\_| \_/ |_|\__,_|
 
Kivia(KPM) is a package manager which helps you to install,search cli packages from internet.

For more help type kpm --help'''))


def startUp():
    args = sys.argv[1:]
    showhelp() if not args else run(args) if not moduleExists(args) else ()
