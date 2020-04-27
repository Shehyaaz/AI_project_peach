# An AI Voice Assistant - PeachAI
import sys
import speech_recognition as sr
import platform
import webbrowser
import requests
from pyowm import OWM
import youtube_dl
import vlc
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import wikipedia
from time import strftime

import data
from send_email import *
if platform.system() == "Linux":
    from linux_system import *
elif platform.system() == "Darwin": # Mac OS
    from mac_system import *

def myCommand():
    "listens for commands"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        command = myCommand()
    return command

def peachAssistant(command):
    "if statements for executing commands"
    # open any website
    if 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain
            webbrowser.open(url)
            peachResponse('The website you have requested has been opened for you Sir.')
        else:
            peachResponse('The website you have requested could not be opened.')
    # greetings
    elif 'hello' in command or 'hi' in command or 'hey' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            peachResponse('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            peachResponse('Hello Sir. Good afternoon')
        else:
            peachResponse('Hello Sir. Good evening')
    # help  me
    elif 'help me' in command:
        peachResponse("""
        You can use these commands and I'll help you out:
        1. Open xyz.com : replace xyz with any website name
        2. Send email : Follow up questions such as recipient name, content will be asked in order.
        3. Current weather in city : Tells you the current condition and temperature in t
        4. Greetings
        5. play me a video : Plays song in your VLC media player
        6. news for today : reads top news of today
        7. time : Current system time
        8. top stories from google news (RSS feeds)
        9. tell me about xyz : tells you about xyz
        10. Play Picross on puzzle-nonogram.com
        11. Play Connect 4
        """)
    # joke
    elif 'joke' in command:
        res = requests.get('https://icanhazdadjoke.com/', headers={"Accept":"application/json"})
        if res.status_code == requests.codes.ok:
            peachResponse(str(res.json()['joke']))
        else:
            peachResponse('oops!I ran out of jokes')
    # top stories from google news
    elif 'news for today' in command:
        try:
            news_url = "https://news.google.com/news/rss"
            Client = urlopen(news_url)
            xml_page = Client.read()
            Client.close()
            soup_page = soup(xml_page, "xml")
            news_list = soup_page.findAll("item")
            for news in news_list[:15]:
                peachResponse(news.title.text)
        except Exception as e:
            print(e)
    # current weather
    elif 'current weather' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM(data.owmApi) # our API key!
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit='celsius')
            response = '''Current weather in %s is %s.
             The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius''' % (city, k, x['temp_max'], x['temp_min'])
            peachResponse(response)
    # current time
    elif 'time' in command:
        import datetime
        now = datetime.datetime.now()
        peachResponse('Current time is %d hours %d minutes' % (now.hour, now.minute))
    # email
    elif 'email' in command:
        peachResponse("Who is the recipient?")
        recipient = myCommand()
        # lookup for recipient's email id
        try:
            receiver_email = data.receiver_email[recipient.lower()]
            peachResponse('What should I send?')
            content = myCommand()
            send_mail(recipient,receiver_email,content)
            peachResponse('Email has been sent successfully. You can check the inbox.')
        except KeyError:
            peachResponse('The email address could not be found.')

    # launch any system application
    elif 'launch' in command:
        launchApp(command)

    # play youtube song
    elif 'play me a song' in command or 'play a song' in command:
        peachResponse("Which song should I play, Sir ?")
        mysong = myCommand()
        if mysong:
            peachResponse("Please give me a minute")
            if (data.music_folder+"/"+mysong) in os.listdir(data.music_folder):
                player = vlc.MediaPlayer(data.music_folder + '/' + mysong)
                player.play()
            else :
                flag = 0
                url = "https://www.youtube.com/results?search_query=" + mysong.replace(' ', '+')
                response = urlopen(url)
                html = response.read()
                soup1 = soup(html , "lxml")
                url_list = []
                for vid in soup1.findAll(attrs={'class':'yt-uix-tile-link'}):
                    if ('https://www.youtube.com' + vid['href']).startswith("https://www.youtube.com/watch?v="):
                        flag = 1
                        final_url = 'https://www.youtube.com' + vid['href']
                        url_list.append(final_url)
                url = url_list[0]
                ydl_opts = {'outtmpl': data.music_folder+'/'+mysong}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                player = vlc.MediaPlayer(data.music_folder+'/'+mysong)
                player.play()

            com = myCommand()
            if 'stop' in com:
                player.stop()
            elif 'pause' in com:
                player.pause()
            else :
                player.play()

            if flag == 0:
                peachResponse('I have not found anything in Youtube !')


    # tell me about
    elif'tell me about' in command or 'what is ' in command or 'define' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                try:
                    ny = wikipedia.summary(topic)
                except wikipedia.DisambiguationError as e:
                    t = random.choice(e.options)
                    ny = wikipedia.summary(t, sentences=4)
                peachResponse(ny)
        except Exception as e:
            print(e)
            peachResponse(e)

    # play nonogram puzzle
    elif 'nonogram' in command:
        peachResponse('Enjoy your game.')
        url = "https://www.puzzle-nonograms.com/"
        webbrowser.open(url)

    # play connect 4
    elif 'connect' in command:
        peachResponse('Would you like to play with a friend ?')
        ans = myCommand()
        if 'yes' in ans:
            from connect4 import connect4
            connect4.mainGame()
        else:
            peachResponse('You are up against me!')
            from connect4 import connect4_with_ai
            connect4_with_ai.mainGame()

    # hangman
    elif 'hangman' in command:
        from hangman import hangman_ai
        hangman_ai.play()
        peachResponse("I hope you had fun sir!")

    # chat with Peach!
    elif "let's talk" in command:
        from chatbot import chatgui
        chatgui.ChatGui()

    # to terminate the program
    elif 'bye' in command:
        peachResponse('Bye bye Sir. Have a nice day')
        sys.exit()
    # responding to thanks
    elif 'thanks' in command or 'thank you' in command:
        peachResponse("Your welcome!")
    else:
        if command != "":
            peachResponse("Sorry, I didn't understand!")


