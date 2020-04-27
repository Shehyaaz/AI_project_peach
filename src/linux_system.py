# This file includes methods for a Linux system
import os
import re
import subprocess

def peachResponse(audio):
    "speaks audio passed as argument"
    print(audio)
    for line in audio.splitlines():
        line = line.replace("\"", "").replace("'", "")
        command = """pico2wave -l=en-US -w=temp.wav "{}" """.format(line)
        os.system(command)
        os.system('aplay temp.wav')

def launchApp(command):
    reg_ex = re.search('launch (.*)', command)
    if reg_ex:
        appname = reg_ex.group(1)
        subprocess.call(appname, stdout=subprocess.PIPE)
        peachResponse('I have launched the desired application')
