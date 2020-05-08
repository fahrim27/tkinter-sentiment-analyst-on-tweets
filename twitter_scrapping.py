import re
import matplotlib.pyplot as plt
import numpy as np
import tweepy
import textblob
from textblob import TextBlob
from tweepy import OAuthHandler
from tkinter import Tk, Label, Entry, Text, END, Button, PhotoImage
from tkinter.messagebox import showerror, showinfo

api_key = "eKfzeYoZWFUQ7g4ogx6KeZqRs"
api_secret_key = "suBMejO4npo3V5DjEGe3CiO3hYByPY37h4YVm7YqxqGpIMbOXn"

access_token = "1140296275755036672-zOAtEJ4uUD3jU7Xw0Lhugi8smm656m"
access_token_secret = "xhRYHDe9JjaJO9X2el2PW2caBX9SL1YisciOdvkZNplJY"

auth = OAuthHandler(api_key, api_secret_key)  # set access token and secret

auth.set_access_token(access_token, access_token_secret)  # create tweepy API object to fetch tweets

api = tweepy.API(auth)

root = Tk()  # main GUI window
root.title("Twitter Cyberbullying with Sentiment Analysis")
root.geometry('1000x800')
root.configure(bg="#E1E8ED")

icon = PhotoImage(file=r"E:\stki\1200px-Twitter_bird_logo_2012.svg.png")

icon1 = PhotoImage(file=r"E:\stki\1_sDa7Oqnh-zRXPPewKZid4g.png")

background = Label(root, image=icon,bg="#E1E8ED")
background.pack()
background1 = Label(root, image=icon1)
background1.pack(side="bottom", expand=True)

label1 = Label(root, text="Search", font="Helvetica 20 bold", bg="#E1E8ED")  # get data from the user

E1 = Entry(root, bd=5, font="Helvetica 15", bg="#F5F8FA")


def tweet():  # master code,here lies the main code for analysis

    topics = E1.get()
    showinfo("Silahkan tunggu", "proses scrapping data dari twitter masih berjalan")
    try:
        tweets = api.search(q=topics, count=1000)
        # print(tweets)
        positive = 0
        negative = 0
        neutral = 0
        for t in tweets:
            text = clean_data(t.text)
            # print(text)
            # print("\n")
            analysis = TextBlob(text)

            if analysis.sentiment.polarity > 0:
                positive += 1
            elif analysis.sentiment.polarity < 0:
                negative += 1
            elif analysis.sentiment.polarity == 0:
                neutral += 0

        total = positive + negative + neutral
        posperc = round((positive * 100) / total, 2)
        negperc = round((negative * 100) / total, 2)
        neuperc = round((neutral * 100) / total, 2)

        T = Text(root, height=9, width=50, bd=5, font="Helvetica 15", bg="#F5F8FA")
        T.pack()
        T.bell()
        T.insert(END, "********************************************************************" + "\n")
        T.insert(END, "Total positive tweets: " + str(positive) + " === " + str(posperc) + "%" + "\n")
        T.insert(END, "Total negative tweets: " + str(negative) + " === " + str(negperc) + "%" + "\n")
        T.insert(END, "Total neutral tweets: " + str(neutral) + " === " + str(neuperc) + "%" + "\n" + "\n")
        T.insert(END, "********************************************************************")
        T.config(state="disabled")
        showinfo("Info", "Click OK untuk melihat visualisasi data")
        graph(positive, negative, neutral, topics)  # graph() is defined after clean_data()
    except ZeroDivisionError:
        showerror("Error", "OOPS!!! topic twitter yang anda cari tidak ditemukan")
    except tweepy.error.TweepError:
        showerror("Error", "INTERNET PROBLEM!!! Periksa kembali jaringan internet anda")


def clean_data(tweets):  # cleaning up the data which is not required
    return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweets).split())


def graph(positive, negative, neutral, topics):  # plotting Graph
    # fig, ax = plt.subplots()
    index = np.arange(1)
    bar_width = 0.1
    opacity = 1

    plt.bar(index, positive, bar_width, alpha=opacity, color='g', edgecolor='w', label='positive')

    plt.bar(index + bar_width, negative, bar_width, alpha=opacity, color='r', edgecolor='w', label='negative')

    plt.bar(index + bar_width + bar_width, neutral, bar_width, alpha=opacity, color='b', edgecolor='w', label='neutral')

    plt.xticks(index + bar_width, [topics], family='fantasy')
    plt.xlabel('Topics', fontweight='bold', fontsize='10')
    plt.ylabel('Sentiments', fontweight='bold', fontsize='10')
    plt.title('Twitter Sentiment Analysis', fontweight='bold', color='white', fontsize='17',
              horizontalalignment='center', backgroundcolor='black')
    plt.legend()

    plt.tight_layout()
    plt.show()


submit = Button(root, text="Submit", command=tweet, font="Helvetica 16", bg="#E1E8ED", bd=5, relief="raised")
label1.pack()
E1.pack()

submit.pack()

root.mainloop()
