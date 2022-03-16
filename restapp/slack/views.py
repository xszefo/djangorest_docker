from django.shortcuts import render
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from slack_sdk import WebClient

from datetime import datetime

import subprocess
import random
import os

# Create your views here.
class Events(APIView):
    def post(self, request, *args, **kwargs):
        SLACK_VERIFICATION_TOKEN = settings.ENV('SLACK_VERIFICATION_TOKEN')
        SLACK_BOT_USER_TOKEN = os.environ['SLACK_BOT_USER_TOKEN']
        slack_message = request.data
        
        GREETINGS = ['hi', 'hello', "what's up"]

        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            print("Error! Wrong token\nOur: {}\nReceived: {}\n".format(SLACK_VERIFICATION_TOKEN, slack_message.get('token')))
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        # verification challenge
        if slack_message.get('type') == 'url_verification':
            return Response(data=slack_message, status=status.HTTP_200_OK)
        
        client = WebClient(token=SLACK_BOT_USER_TOKEN)

        # event handler
        if 'event' in slack_message:
            event_message = slack_message.get('event')

            # process user's message
            user = event_message.get('user')                      
            text = event_message.get('text')                      
            channel = event_message.get('channel')       

            print(f'''
            New message
            Time: {datetime.now()}
            User: {user}
            Text: {text}
            Channel: {channel}
            ''')
            # ignore bot's own message
            if event_message.get('subtype') == 'bot_message' or user == 'UU7ERFFNW': 
                return Response(status=status.HTTP_200_OK)        

            # message options
            if any([True for message in GREETINGS if message in text.lower()]):                              
                greeting = random.choice(GREETINGS)
                bot_text = '{} <@{}> :wave:'.format(greeting, user)           
            elif 'uptime' in text.lower():
                uptime = subprocess.check_output(['uptime'], shell=True)
                bot_text = uptime.decode('UTF-8')
            elif '@UU7ERFFNW' in text:
                bot_text='<@UU7ERFFNW> at your service, how can I help?'                   
            elif 'hostname' in text.lower():
                hostname = subprocess.check_output(['hostname'], shell=True)
                bot_text = hostname.decode('UTF-8')
            elif 'cpu' in text.lower():
                cpu = subprocess.check_output(["grep 'processor\|vendor\|name\|MHz' /proc/cpuinfo"], shell=True)
                bot_text = cpu.decode('UTF-8')
            else:
               bot_text = '{}? I do not understand.'.format(text)
                               
            client.chat_postMessage(method='chat.postMessage', channel=channel, text=bot_text)    

        return Response(status=status.HTTP_200_OK)