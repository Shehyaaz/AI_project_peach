
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model
model = load_model('./chatbot/chatbot_model.h5')
import json
import random
intents = json.loads(open('./chatbot/intents.json').read())
words = pickle.load(open('./chatbot/words.pkl','rb'))
classes = pickle.load(open('./chatbot/classes.pkl','rb'))


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


#Creating GUI with tkinter
import tkinter
from tkinter import *

class ChatGui:
    def __init__(self):
        base = Tk()
        base.title("Chat with Peach")
        base.geometry("600x600")
        base.resizable(width=FALSE, height=FALSE)

        #Create Chat window
        self.ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",wrap=WORD)

        self.ChatLog.config(state=DISABLED)

        #Bind scrollbar to Chat window
        scrollbar = Scrollbar(base, command=self.ChatLog.yview)
        self.ChatLog['yscrollcommand'] = scrollbar.set

        # Create Button to send message
        self.SendButton = Button(base, font=("Verdana", 12, 'bold'), text="Send", width="12", height=5,
                            bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff',
                            command=self.send)

        #Create the box to enter message
        self.EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
        self.EntryBox.bind("<Return>", self.send)


        #Place all components on the screen
        scrollbar.place(x=586,y=6, height=495)
        self.ChatLog.place(x=6,y=6, height=495, width=580)
        self.EntryBox.place(x=6, y=501, height=90, width=435)
        self.SendButton.place(x=441, y=501, height=90)

        base.mainloop()

    def send(self,event=None):
        msg = self.EntryBox.get("1.0",'end-1c').strip()
        self.EntryBox.delete("0.0",END)

        if msg != '':
            self.ChatLog.config(state=NORMAL)
            self.ChatLog.insert(END, "You: " + msg + '\n\n')
            self.ChatLog.config(foreground="#442265", font=("Verdana", 12 ))

            res = chatbot_response(msg)
            self.ChatLog.insert(END, "Bot: " + res + '\n\n')

            self.ChatLog.config(state=DISABLED)
            self.ChatLog.yview(END)