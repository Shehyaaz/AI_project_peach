# This file include methods for a Mac system.
import os
import re
import subprocess

def peachResponse(audio):
    print(audio)
    for line in audio.splitlines():
        os.system("say " + line)

def launchApp(command):
    reg_ex = re.search('launch (.*)', command)
    if reg_ex:
        appname = reg_ex.group(1)
        appname1 = appname+".app"
        subprocess.Popen(["open", "-n", "/Applications/" + appname1], stdout=subprocess.PIPE)
        peachResponse('I have launched the desired application')