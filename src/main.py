from peachMain import *
if platform.system() == "Linux":
    from linux_system import peachResponse
elif platform.system() == "Darwin": # Mac OS
    from mac_system import peachResponse

if __name__ == '__main__':
    username = input("Please enter your name :")
    greeting_text = '''Hi {}, I am Peach, your personal voice assistant !!\nPlease give a command or say 'help me' and I will tell you what all I can do for you !!'''.format(username)

    peachResponse(greeting_text)
    # loop to continue executing multiple commands
    while True:
        try:
            peachAssistant(myCommand())
        except Exception as e:
            print(e)
            peachResponse("Oops! Something went wrong.")
