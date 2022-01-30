import sys

from multiprocessing.connection import answer_challenge
import re
import os

import time
import emoji
import requests
from dotenv import load_dotenv
from curiosa import send_text, append_chat_log
from predict import predict_COV
from getNews import sendNews
from latestDataUtil import get_StatsbyCountry
from worldStatsUtil import get_WorldStats
from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route("/")
def hello():
    return "Nerdo Twilio Bot"


@app.route("/whatsapp", methods=['POST'])
def reply():

    # Initial Variables Defined
    sender = request.form.get('From')
    incoming_msg = request.form.get('Body')
    media_url = request.form.get('MediaUrl0')
    responded = False

    # Main Menu Logic
    if re.match(incoming_msg, "Hello", re.IGNORECASE):

        intro_response = emoji.emojize('''
        Hello ! I'm *Nerdo* :wave: \nA AI Powered ChatBot built for the Tri NIT Hack'22. If you are one of those Geeks who stick to the phone for the purpose of academia, I was built for you to serve in the times of pandemic. I was recently built so I come with a limited set of features for you to explore. Here's what you can ask me to do : \n
:black_small_square: Type <*news category*> to get Top 5 Headlines. For ex "news health"
:black_small_square: Type <*stats cntry_name*> to get Latest COVID Stats by CNTRY_NAME. For ex "stats india", "stats italy"
:black_small_square: Type <*world stats*> to get World COVID Stats
:black_small_square: Type <*covid chest xray*> to conduct Early Stage Prediction of COVID-19 from CT-Scan \n \nI am also aware of academia related to COVID-19. If you wanna have a chat about it, give me a call out by *Hello Nerdo* in the text box.\n\nP.S. : You can always come back here with a *Hello* if you feel lost :heart:
        ''', use_aliases=True)

        reply_text = MessagingResponse()
        reply_text.message(intro_response)
        responded = True
        return str(reply_text)

    # GPT-3 DeepSet Trained Bot Logic
    if re.match("Hello Nerdo", incoming_msg, re.IGNORECASE) or session.get('bot_State') == True:
        print(session.get('bot_State'))
        if session.get('bot_State') == True and re.match("exit", incoming_msg, re.IGNORECASE):
            bot_response = "Thank You for talking to Nerdo !"
            session['bot_State'] = False
            reply_text = MessagingResponse()
            reply_text.message(bot_response)
            responded = True
            return str(reply_text)

        chat_log = session.get('chat_log')
        bot_response = send_text(incoming_msg, chat_log)

        # Testing Utility
        # bot_response = "Dummy Bot Response"
        
        session['bot_State'] = True
        session['chat_log'] = append_chat_log(
            incoming_msg, bot_response, chat_log)

        reply_text = MessagingResponse()
        reply_text.message(bot_response)
        responded = True
        return str(reply_text)

    # Chest X-Ray COVID=19 Helper
    if re.match("covid chest xray", incoming_msg, re.IGNORECASE):
        reply_string = "Hey ! I hope you are doing well ! We have an early stage detection for your CT-Scan systems. Please upload your CT-Scan in PNG/JPEG format we'll be using it predict presence of COVID19.\n\n Please make sure to consult doctors to avoid False Negatives/Positives"
        reply_text = MessagingResponse()
        reply_text.message(reply_string)
        responded = True
        return str(reply_text)
    # Chest X-Ray COVID-19 Detection
    if media_url:
        r = requests.get(media_url)
        content_type = r.headers['Content-Type']
        username = sender.split(':')[1]
        if content_type == 'image/png':
            filename = f'media/XRay.png'
        elif content_type == 'image/jpg':
            filename = f'media/XRay.jpg'
        else:
            filename = None

        if filename:
            if not os.path.exists(f'media/'):
                os.mkdir(f'media/')
            with open(filename, 'wb') as f:
                f.write(r.content)
            filepath = f'media/XRay.png'
            covid_pred, cf_score = predict_COV()
            pred_reply = f'Xception Model predicts *{covid_pred}* for the provided image with a Confidence of {cf_score}'
            reply_text = MessagingResponse()
            reply_text.message(pred_reply)
            responded = True
            return str(reply_text)
        else:
            pred_reply = 'The file that you submitted is not a supported image type'
            reply_text = MessagingResponse()
            reply_text.message(pred_reply)
            responded = True
            return str(reply_text)

    # Handle News Query
    if re.match(incoming_msg.split()[0], "news", re.IGNORECASE):
        news_dict = sendNews(incoming_msg.split()[1])
        news_reply = f'*Here are the Top 5 Headlines Related to {incoming_msg.split()[1]}*' + \
            "\n"
        count = 1
        for title, url in news_dict.items():
            news_reply = news_reply + \
                str(count) + ". " + title + "\n" + url + "\n\n"
            count = count + 1
        reply_text = MessagingResponse()
        reply_text.message(news_reply)
        responded = True

        return str(reply_text)

    # Get Statistics by Country
    if re.match(incoming_msg.split()[0], "stats", re.IGNORECASE):
        stats_json = get_StatsbyCountry(incoming_msg.split()[1])
        country = stats_json[0]['country']
        confirmed = stats_json[0]['confirmed']
        recovered = stats_json[0]['recovered']
        critical = stats_json[0]['critical']
        deaths = stats_json[0]['deaths']
        lastUpdate = stats_json[0]['lastUpdate']

        stats_reply = f'*Here are the Stats for {country}*'
        stats_reply = stats_reply + "\n" + \
            emoji.emojize(''':black_small_square:''') + \
            "Confirmed Cases: " + str(confirmed)
        stats_reply = stats_reply + "\n" + \
            emoji.emojize(''':black_small_square:''') + \
            "Recovered Cases : " + str(recovered)
        stats_reply = stats_reply + "\n" + \
            emoji.emojize(''':black_small_square:''') + \
            "Critical Cases : " + str(critical)
        stats_reply = stats_reply + "\n" + \
            emoji.emojize(''':black_small_square:''') + \
            "Death Cases : " + str(deaths)
        stats_reply = stats_reply + "\n" + \
            emoji.emojize(''':black_small_square:''') + \
            "Last Updated : " + str(lastUpdate)
        stats_reply = stats_reply + "\n" + "\n" + "Stay Safe and Take Care " + \
            emoji.emojize(''':red_heart:''', use_aliases=True)

        reply_text = MessagingResponse()
        reply_text.message(stats_reply)
        responded = True

        return str(reply_text)

    # Get Total Stats
    if re.match(incoming_msg, "world stats", re.IGNORECASE):
        stats_json = get_WorldStats()
        confirmed = stats_json[0]['confirmed']
        recovered = stats_json[0]['recovered']
        critical = stats_json[0]['critical']
        deaths = stats_json[0]['deaths']
        lastUpdate = stats_json[0]['lastUpdate']

        stats_reply = f'*Here are the World Stats (~5 Mins Lag)*'
        stats_reply = stats_reply + "\n" + \
            emoji.emojize(''':black_small_square:''') + \
            "Confirmed Cases: " + str(confirmed)
        stats_reply = stats_reply + "\n" + \
            emoji.emojize(''':black_small_square:''') + \
            "Recovered Cases : " + str(recovered)
        stats_reply = stats_reply + "\n" + \
            emoji.emojize(''':black_small_square:''') + \
            "Critical Cases : " + str(critical)
        stats_reply = stats_reply + "\n" + \
            emoji.emojize(''':black_small_square:''') + \
            "Death Cases : " + str(deaths)
        stats_reply = stats_reply + "\n" + \
            emoji.emojize(''':black_small_square:''') + \
            "Last Updated : " + str(lastUpdate)
        stats_reply = stats_reply + "\n" + "\n" + "Stay Safe and Take Care " + \
            emoji.emojize(''':red_heart:''', use_aliases=True)

        reply_text = MessagingResponse()
        reply_text.message(stats_reply)
        responded = True

        return str(reply_text)
    if not responded:
        fallback_reply = "Hey ! I don't understand this command. Please type *hello* to checkout available commands"
        reply_text = MessagingResponse()
        reply_text.message(fallback_reply)
        return str(reply_text)

if __name__ == "__main__":
    app.run(debug=True)
